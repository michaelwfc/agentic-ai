from typing import List
from langchain.tools import tool
# from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage

"""
### 3.1. VLM Helper and Prompts

Prompts define structured VLM output with three components:
1. **Role definition** (e.g., "Chart Analysis specialist")
2. **Extraction fields** (chart type, axes, data points)
3. **JSON template** for consistent formatting
"""


def build_document_process_tools()->List[tool]:
    return [AnalyzeChart,AnalyzeTable]


# Tool prompts
CHART_ANALYSIS_PROMPT = """You are a Chart Analysis specialist. 
Analyze this chart/figure image and extract:

1. **Chart Type**: (line, bar, scatter, pie, etc.)
2. **Title**: (if visible)
3. **Axes**: X-axis label, Y-axis label, and tick values
4. **Data Points**: Key values (peaks, troughs, endpoints)
5. **Trends**: Overall pattern description
6. **Legend**: (if present)

Return a JSON object with this structure:
```json
{{
  "chart_type": "...",
  "title": "...",
  "x_axis": {{"label": "...", "ticks": [...]}},
  "y_axis": {{"label": "...", "ticks": [...]}},
  "key_data_points": [...],
  "trends": "...",
  "legend": [...]
}}
```
"""



TABLE_ANALYSIS_PROMPT = """You are a Table Extraction specialist. 
Extract structured data from this table image.

1. **Identify Structure**: 
    - Column headers, row labels, data cells
2. **Extract All Data**: 
    - Preserve exact values and alignment
3. **Handle Special Cases**: 
    - Merged cells, empty cells (mark as null), multi-line headers

Return a JSON object with this structure:
```json
{{
  "table_title": "...",
  "column_headers": ["header1", "header2", ...],
  "rows": [
    {{"row_label": "...", "values": [val1, val2, ...]}},
    ...
  ],
  "notes": "any footnotes or source info"
}}
```
"""


def call_vlm_with_image(image_base64: str, prompt: str) -> str:
    """Call VLM with an image and prompt."""
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_base64}"}
            }
        ]
    )
    response = vlm.invoke([message])
    return response.content




@tool
def AnalyzeChart(region_id: int) -> str:
    """Analyze a chart or figure region using VLM. 
    Use this tool when you need to extract data from charts, graphs, or figures.
    
    Args:
        region_id: The ID of the layout region to analyze (must be a chart/figure type)
    
    Returns:
        JSON string with chart type, axes, data points, and trends
    """
    if region_id not in region_images:
        return f"Error: Region {region_id} not found. Available regions: {list(region_images.keys())}"
    
    region_data = region_images[region_id]
    
    if region_data['type'] not in ['chart', 'figure']:
        return f"Warning: Region {region_id} is type '{region_data['type']}', not a chart/figure. Proceeding anyway."
    
    result = call_vlm_with_image(region_data['base64'], CHART_ANALYSIS_PROMPT)
    
    return result

# print("AnalyzeChart tool defined")

@tool
def AnalyzeTable(region_id: int) -> str:
    """
    Extract structured data from a table region using VLM.
    Use this tool when you need to extract tabular data 
    with headers and rows.
    
    Args:
        region_id: The ID of the layout region to analyze (must be a table type)
    
    Returns:
        JSON string with table headers, rows, and any notes
    """
    if region_id not in region_images:
        return f"Error: Region {region_id} not found. Available regions: {list(region_images.keys())}"
    
    region_data = region_images[region_id]
    
    if region_data['type'] != 'table':
        return f"Warning: Region {region_id} is type '{region_data['type']}', not a table. Proceeding anyway."
    
    result = call_vlm_with_image(region_data['base64'], TABLE_ANALYSIS_PROMPT)
    return result

# print("AnalyzeTable tool defined")

if __name__ == "__main__":
    print("VLM tools defined")
    # Test the tools
    print("Testing AnalyzeChart...")
    chart_regions = [r for r in layout_regions if r.region_type in ['chart', 'figure']]
    if chart_regions:
        test_result = AnalyzeChart.invoke({"region_id": chart_regions[0].region_id})
        print(f"Chart analysis result:\n{test_result[:500]}...")
    else:
        print("No chart regions found")


    # Test table tool
    print("Testing AnalyzeTable...")
    table_regions = [r for r in layout_regions if r.region_type == 'table']
    if table_regions:
        test_result = AnalyzeTable.invoke({"region_id": table_regions[0].region_id})
        print(f"Table analysis result:\n{test_result[:500]}...")
    else:
        print("No table regions found")
        