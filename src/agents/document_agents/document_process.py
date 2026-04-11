"""
transformers
torch
paddlepaddle==3.0.0
paddleocr
landingai-ade

"""
from typing import List, Dict, Any
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import matplotlib.patches as patches
import cv2
from dataclasses import dataclass
from langchain.tools import tool
import base64
from io import BytesIO
import pytesseract
# Add this after importing pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path accordingly
from paddleocr import PaddleOCR
from paddleocr import LayoutDetection
from transformers import LayoutLMv3ForTokenClassification
from layoutreader.v3.helpers import prepare_inputs, boxes2inputs, parse_logits




@tool
def ocr_read_document(image_path: str) -> str:
    """Reads an image from the given path and returns extracted text using OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error reading image: {e}"



class DocumentProcessor:
  def __init__(self):
    # Initialize English OCR model
    self.ocr = PaddleOCR(lang='en')

  def run_ocr(self,image_path):
      # Run OCR
      result = self.ocr.predict(image_path)
      page = result[0]
      texts = page['rec_texts'] # recognized text strings
      scores = page['rec_scores'] # confidence scores for each text line
      boxes  = page['rec_polys'] #  bounding box coordinates

      for text, score, box in zip(texts, scores, boxes):
          # box is a numpy array like [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
          coords = box.astype(int).tolist()  # convert to normal list of ints
          print(f"{text:25} | {score:.3f} | {coords}")
      return texts, scores, boxes
  
  def run(self, image_path):
      """
       Workflow Outline
      - [1. Text Extraction with PaddleOCR + LayoutLM Ordering](#1)
        - [1.1. Running OCR on the Document](#1-1)
        - [1.2. Visualizing OCR Bounding Boxes](#1-2)
        - [1.3. Structuring OCR Results with a Dataclass](#1-3)
        - [1.4. LayoutLM Reading Order](#1-4)
        - [1.5. Visualizing the Reading Order](#1-5)
        - [1.6. Creating the Ordered Text Output](#1-6)
      - [2. Layout Detection with PaddleOCR](#2)
        - [2.1. Processing Document Layout](#2-1)
        - [2.2. Structuring Layout Results](#2-2)
        - [2.3. Visualizing Layout Detection](#2-3)
        - [2.4. Cropping Regions for Agent Tools](#2-4)
      - [3. Agent Tools](#3)
        - [3.1. VLM Helper and Prompts](#3-1)
        - [3.2. Creating the AnalyzeChart Tool](#3-2)
        - [3.3. Creating the AnalyzeTable Tool](#3-3)
        - [3.4. Testing the Tools](#3-4)
      - [4. LangChain Agent](#4)
        - [4.1. Formatting Context for the Agent](#4-1)
        - [4.2. Creating the System Prompt](#4-2)
        - [4.3. Assembling the Agent](#4-3)
        - [4.4. Testing the Agent](#4-4)
      """
      # 1. Text Extraction with PaddleOCR + LayoutLM Ordering
      # 1.1. Running OCR on the Document
      texts, scores, boxes = self.run_ocr(image_path=image_path)
      # 1.2. Visualizing OCR Bounding Boxes
      visualize_ocr_reuslt(texts=texts, boxes=boxes)
      # 1.3. Structuring OCR Results with a Dataclass
      ocr_regions = get_ocr_regions(texts, scores, boxes)

      # 1.4. LayoutLM Reading Order
      # Get reading order
      reading_order = get_reading_order(ocr_regions)
      print(f"Reading order determined for {len(reading_order)} regions")
      print(f"First 20 positions: {reading_order[:20]}")
      # 1.5. Visualizing the Reading Order
      visualize_reading_order(ocr_regions, processed_img, 
                            reading_order, "LayoutLM Reading Order")
      # 1.6. Creating the Ordered Text Output
      ordered_text = get_ordered_text(ocr_regions, reading_order)
      print("Text in reading order:")
      print("=" * 70)
      ordered_text[:5]


      # 2. Layout Detection with PaddleOCR
      # 2.1. Processing Document Layout
      layout_results = process_document_layout(image_path)
      print(f"Detected {len(layout_results)} layout regions:")
      for r in layout_results:
          print(f"  {r['label']:20} score: {r['score']:.3f}  bbox: {[int(x) for x in r['bbox']]}")
      # 2.2. Structuring Layout Results
      layout_regions =  get_layout_regions(layout_results)
      print(f"Stored {len(layout_regions)} layout regions")
      # 2.3. Visualizing Layout Detection
      visualize_layout(image_path, layout_regions, 
                    min_confidence=0.5, title="PaddleOCR Layout Detection")
      # 2.4. Cropping Regions for Agent Tools
      # Load image for cropping
      region_images,full_image_base64 = get_layout_region_images(image_path,layout_regions)
      print(f"Cropped {len(region_images)} regions")
      visualize_cropped_regions(region_images)



  

def visualize_ocr_reuslt(img, texts, boxes):
    img_plot = img.copy()

    for text, box in zip(texts, boxes):
        pts = np.array(box, dtype=int)
        cv2.polylines(img_plot, [pts], True, (0, 255, 0), 2)
        x, y = pts[0]
        cv2.putText(img_plot, text, (x, y - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    plt.figure(figsize=(8, 10))
    plt.imshow(cv2.cvtColor(img_plot, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title("Aligned Bounding Boxes (Processed Image)")
    plt.show()


def run_ocr_and_show(ocr, image_path, show_text = True):
    """This helper function runs OCR and visualizes results with bounding boxes."""

    # display(Image.open(image_path))
    result = ocr.predict(image_path)
    
    page = result[0]
    texts  = page['rec_texts'] 
    scores = page['rec_scores'] 
    boxes  = page['rec_polys'] 
    
    for text, score, box in zip(texts, scores, boxes):
        coords = box.astype(int).tolist()  
        print(f"{text:25} | {score:.3f} | {coords}")
        
    img = page['doc_preprocessor_res']['output_img'] 
    img_plot = img.copy()

    image_path = Path(image_path)
    output_path = image_path.with_stem(image_path.stem + "_output")  
    cv2.imwrite(str(output_path), img)
    
    for text, box in zip(texts, boxes):
        pts = np.array(box, dtype=int)
        cv2.polylines(img_plot, [pts], True, (0, 255, 0), 2)
        x, y = pts[0]
        if show_text:
            cv2.putText(img_plot, text, 
                        (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (255, 0, 0), 2)
    
    plt.figure(figsize=(8, 10))  
    plt.imshow(cv2.cvtColor(img_plot, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title("Aligned Bounding Boxes (Processed Image)")
    plt.show()


@tool
def paddle_ocr_read_document(image_path: str) -> List[Dict[str, Any]]:
    """
    Reads an image from the given path and returns extracted text 
    with bounding boxes.
    
    Returns a list of dictionaries, each containing:
    - 'text': the recognized text string
    - 'bbox': bounding box coordinates [x_min, y_min, x_max, y_max]
    - 'confidence': recognition confidence score (if available)
    """
    try:
        ocr = PaddleOCR(lang='en')
        result = ocr.predict(image_path)
        page = result[0]
        
        texts = page['rec_texts'] 
        boxes = page['dt_polys']         
        scores = page.get('rec_scores', [None] * len(texts))  
        
        extracted_items = []
        for text, box, score in zip(texts, boxes, scores):
            x_coords = [point[0] for point in box]
            y_coords = [point[1] for point in box]
            bbox = [min(x_coords), min(y_coords), max(x_coords), 
                    max(y_coords)]
            
            item = {
                'text': text,
                'bbox': bbox,
            }
            if score is not None:
                item['confidence'] = score
                
            extracted_items.append(item)
        
        return extracted_items
    
    except Exception as e:
        return [{"error": f"Error reading image: {e}"}]


# Store OCR results in a structured format
@dataclass
class OCRRegion:
    text: str
    bbox: list  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    confidence: float
    
    @property
    def bbox_xyxy(self):
        """Return bbox as [x1, y1, x2, y2] format."""
        x_coords = [p[0] for p in self.bbox]
        y_coords = [p[1] for p in self.bbox]
        return [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]



def get_ocr_regions(texts, scores, boxes)->List[OCRRegion]:
    """
    ### 1.3. Structuring OCR Results with a Dataclass
    Structure OCR output using an `OCRRegion` dataclass for cleaner code:
    - Typed structure for each text region
    - `bbox_xyxy` property converts 4-point polygons to `[x1, y1, x2, y2]` format
    """
    ocr_regions: List[OCRRegion] = []
    for text, score, box in zip(texts, scores, boxes):
        ocr_regions.append(OCRRegion(
            text=text, 
            bbox=box.astype(int).tolist(), 
            confidence=score
        ))

    print(f"Stored {len(ocr_regions)} OCR regions")
    return ocr_regions



def process_document_layout(image_path):
    """Get layout regions from document.

    ## 2. Layout Detection with PaddleOCR

    Beyond text extraction, identify **content types** using layout detection.

    PaddleOCR's `LayoutDetection` identifies document structure. Each region includes:
    - **label**: Content type (text, table, chart, figure, etc.)
    - **score**: Confidence score
    - **bbox**: Bounding box in XYXY format

    ### 2.1. Processing Document Layout

    Run layout detection to identify content types (text blocks, charts, titles, tables, etc.).
    """
    # Initialize layout detection 
    layout_engine = LayoutDetection()

    # Get layout regions
    layout_result = layout_engine.predict(image_path)
    
    # Parse the boxes
    regions = []
    for box in layout_result[0]['boxes']:
        regions.append({
            'label': box['label'],
            'score': box['score'],
            'bbox': box['coordinate'],  # [x1, y1, x2, y2]
        })
    
    # Sort by confidence
    regions = sorted(regions, key=lambda x: x['score'], reverse=True)
    
    return regions


def visualize_layout(image_path, min_confidence=0.5):
    # Initialize layout detection 
    layout_engine = LayoutDetection()

    layout_result = layout_engine.predict(image_path)
    
    img = cv2.imread(image_path)
    img_plot = img.copy()
    
    # Get all unique labels
    labels = list(set(box['label'] for box in layout_result[0]['boxes']))
    
    # Generate colors dynamically from colormap
    cmap = colormaps.get_cmap('tab20') 
    color_map = {}
    for i, label in enumerate(labels):
        rgba = cmap(i % 20)
        # Convert to BGR (0-255) for OpenCV
        color_map[label] = (int(rgba[2]*255), int(rgba[1]*255), int(rgba[0]*255))
    
    for box in layout_result[0]['boxes']:
        if box['score'] < min_confidence:
            continue
            
        label = box['label']
        score = box['score']
        coords = box['coordinate']
        
        color = color_map[label]
        
        x1, y1, x2, y2 = [int(c) for c in coords]
        pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=int)
        
        cv2.polylines(img_plot, [pts], True, color, 2)
        text = f"{label} ({score:.2f})"
        cv2.putText(img_plot, text, (x1, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    return img_plot


@dataclass
class LayoutRegion:
    region_id: int
    region_type: str
    bbox: list  # [x1, y1, x2, y2]
    confidence: float

def get_layout_regions(layout_results)->List[LayoutRegion]:
        
    # Store layout regions in structured format
    layout_regions: List[LayoutRegion] = []
    for i, r in enumerate(layout_results):
        layout_regions.append(LayoutRegion(
            region_id=i,
            region_type=r['label'],
            bbox=[int(x) for x in r['bbox']],
            confidence=r['score']
        ))
    return layout_regions

def get_reading_order(ocr_regions):
    """
    Use LayoutReader to determine reading order of OCR regions.
    Returns list of reading order positions for each region index.

    ### 1.4. LayoutLM Reading Order
    Simple ordering (eg top-to-bottom, left-to-right) does not apply to our complex document. We will use LayoutReader which itself uses LayoutLMv3 model. Hugging Face contains the LayoutLMv3 model. Additionally we use helper functions for LayoutReader available at this [repository](https://github.com/ppaanngggg/layoutreader.git). 

    Now implement a reading order function called `get_reading_order`: 

    1. **Calculate image dimensions** - Estimate size from bounding boxes with 10% padding
    2. **Normalize coordinates** - Scale boxes to 0-1000 range for LayoutLM
    3. **Prepare inputs** - Convert to transformer format
    4. **Run inference** - Get model predictions
    5. **Parse results** - Extract reading order from output logits

    """

    # Load LayoutReader model
    print("Loading LayoutReader model...")
    model_slug = "hantian/layoutreader"
    layout_model = LayoutLMv3ForTokenClassification.from_pretrained(model_slug)
    print("Model loaded successfully!")


    # 1. Calculate image dimensions from bounding boxes (with padding)
    max_x = max_y = 0
    for region in ocr_regions:
        x1, y1, x2, y2 = region.bbox_xyxy
        max_x = max(max_x, x2)
        max_y = max(max_y, y2)

    image_width = max_x * 1.1   # Add 10% padding
    image_height = max_y * 1.1

    # 2. Convert bboxes to LayoutReader format (normalized to 0-1000)
    boxes = []
    for region in ocr_regions:
        x1, y1, x2, y2 = region.bbox_xyxy
        # Normalize to 0-1000 range
        left = int((x1 / image_width) * 1000)
        top = int((y1 / image_height) * 1000)
        right = int((x2 / image_width) * 1000)
        bottom = int((y2 / image_height) * 1000)
        boxes.append([left, top, right, bottom])

    # 3. Prepare inputs
    inputs = boxes2inputs(boxes)
    inputs = prepare_inputs(inputs, layout_model)
    
    # 4. Run inference
    logits = layout_model(**inputs).logits.cpu().squeeze(0)
    
    # 5. Parse the model's outputs to get reading order
    reading_order = parse_logits(logits, len(boxes))

    return reading_order


def visualize_reading_order(ocr_regions, image_array, reading_order, title="Reading Order"):
    """
    Visualize OCR regions with their reading order numbers using matplotlib.
    """
    
    fig, ax = plt.subplots(1, figsize=(10, 14))
    ax.imshow(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
    
    # Create order mapping: index -> reading order position
    order_map = {i: order for i, order in enumerate(reading_order)}
    
    for i, region in enumerate(ocr_regions):
        bbox = region.bbox
        if bbox and len(bbox) >= 4:
            # Draw polygon
            ax.add_patch(patches.Polygon(bbox, linewidth=2, 
                                         edgecolor='blue',
                                         facecolor='none', alpha=0.7))
            # Add reading order number at center
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            ax.text(sum(xs)/len(xs), sum(ys)/len(ys), 
                    str(order_map.get(i, i)),
                    fontsize=13, color='red', 
                    ha='center', va='center', fontweight='bold')
    
    ax.set_title(title, fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.show()


# Create ordered text content
def get_ordered_text(ocr_regions, reading_order):
    """
    Return OCR regions sorted by reading order
    with their text and confidence.

    ### 1.6. Creating the Ordered Text Output
    Combine OCR text with reading order:
    1. Pair each region with its reading position
    2. Sort by position
    3. Return structured list with position, text, confidence, and bbox

    This ordered text provides agent context for answering text-based questions without VLM calls.

    """
    # 1. Create (reading_position, index, region) tuples and sort
    indexed_regions = [(reading_order[i], 
                        i, 
                        ocr_regions[i]) for i in range(len(ocr_regions))]
    
    # 2. Sort by reading position
    indexed_regions.sort(key=lambda x: x[0])  
    
    # 3. Extract ordered text info
    ordered_text = []
    for position, original_idx, region in indexed_regions:
        ordered_text.append({
            "position": position,
            "text": region.text,
            "confidence": region.confidence,
            "bbox": region.bbox_xyxy
        })
    
    return ordered_text



def visualize_layout(image_path, layout_regions, min_confidence=0.5, 
                     title="Layout Detection"):
    """
    Visualize layout detection results using cv2 (same pattern as L2).
    """
    img = cv2.imread(image_path)
    img_plot = img.copy()
    
    # Get unique labels and generate colors
    labels = list(set(r.region_type for r in layout_regions))
    cmap = colormaps.get_cmap('tab20')
    color_map = {}
    for i, label in enumerate(labels):
        rgba = cmap(i % 20)
        color_map[label] = (int(rgba[2]*255), int(rgba[1]*255), int(rgba[0]*255))
    
    for region in layout_regions:
        if region.confidence < min_confidence:
            continue
            
        color = color_map[region.region_type]
        x1, y1, x2, y2 = region.bbox
        
        # Draw rectangle
        pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=int)
        cv2.polylines(img_plot, [pts], True, color, 2)
        
        # Add label
        text = f"{region.region_id}: {region.region_type} ({region.confidence:.2f})"
        cv2.putText(img_plot, text, (x1, y1-8), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    plt.figure(figsize=(12, 16))
    plt.imshow(cv2.cvtColor(img_plot, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title(title)
    plt.show()
    
    return img_plot



# Crop and save layout regions for agent tools
def crop_region(image, bbox, padding=10):
    """Crop a region from image with optional padding."""
    x1, y1, x2, y2 = bbox
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(image.width, x2 + padding)
    y2 = min(image.height, y2 + padding)
    return image.crop((x1, y1, x2, y2))

def image_to_base64(img):
    """Convert PIL Image to base64 string."""
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def visualize_cropped_regions(region_images):
    # Show cropped regions
    fig, axes = plt.subplots(5, 3, figsize=(15, 10))
    axes = axes.flatten()

    for i, (region_id, data) in enumerate(list(region_images.items())[:14]):
        axes[i].imshow(data['image'])
        axes[i].set_title(f"Region {region_id}: {data['type']}")
        axes[i].axis('off')

    # Hide unused subplots
    for j in range(i+1, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


def get_layout_region_images(image_path, layout_regions)-> List[Dict]:
    pil_image = Image.open(image_path)

    # Store cropped regions in dictionary
    region_images = {}
    for region in layout_regions:
        cropped = crop_region(pil_image, region.bbox)
        region_images[region.region_id] = {
            'image': cropped,
            'base64': image_to_base64(cropped),
            'type': region.region_type,
            'bbox': region.bbox
        }

    # Also store full image
    full_image_base64 = image_to_base64(pil_image)

    return region_images ,full_image_base64 

if __name__ == "__main__":

  image_path =None

  document_processor = DocumentProcessor()
  document_processor.run(image_path)
  
