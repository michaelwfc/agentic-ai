# Big Idea

OCR + Layout Detection + visual llm

|  | Applications | Limitations |
|-----------|----------|------------|
| **OCR** | Good at parsing simple text | Bad at tables, handwriting, low-quality scans |
| **Regex** | Good at pattern matching | Bad at handling variations in text |
| **Agent** | Can adapt to variations in text | Dependent on OCR quality; otherwise may hallucinate |

- PaddleOCR : Use PaddleOCR for text parsing and layout detection
- LayoutReader ： Want et al. 2021 ,Use LayoutReader for sorting parsed text into reading order
- Vision-Language Model (VLM): build VLM tools for chart and table analysis

## LayoutReader
LayoutReader is a model for determining reading order. By sorting information on each page, the model captures the logical sequence of text parsed from the document. For documents with multiple columns, floating captions, margin annotations, etc the reading order can be complex.

Input: Bounding boxes normalized to 0-1000 range
Output: Reading order position for each box

LayoutReader uses LayoutLMv3 which was developed by Microsoft on the ReadingBank dataset (500,000+ annotated pages).

## hybrid approach

Our hybrid approach breaks documents into separate regions of text, charts or tables. The LangChain agent uses different tools for each region. 


| Component | Purpose | Output |
|-----------|---------|--------|
| **PaddleOCR** | Text Parsing | Text + bounding boxes|
| **LayoutReader** | Reading order prediction | Sorted sequence of regions |
| **PaddleOCR** | Layout Detection | Region types (table, chart, text) |
| **VLM** | Analysis of charts/tables | JSON (title, legend,... / headers, rows,...) |


In the next lesson, you will study the **Agentic Document Extraction (ADE)** framework from LandingAI. It will handle text parsing, layout detection, reading order, multimodal reasoning, and schema-based extraction in unified API's. This will address several limitations of PaddleOCR on real-world documents. 





# References
- [Document AI: From OCR to Agentic Doc Extraction](https://learn.deeplearning.ai/courses/document-ai-from-ocr-to-agentic-doc-extraction/lesson/60su3505/introduction)
- [OCR to Agentic Document Extraction: A look into the Evolution of Document Intelligence](https://landing.ai/blog/ocr-to-agentic-document-extraction-a-look-into-the-evolution-of-document-intelligence)







