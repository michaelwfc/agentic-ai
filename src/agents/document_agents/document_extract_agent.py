
import os
from PIL import Image
import re
from typing import List
# from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.agents import AgentExecutor
# from langchain.agents import create_tool_calling_agent
from langchain.agents import create_agent 
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from document_agents.document_process import ocr_read_document
from document_agents.document_process_tools import AnalyzeTable,AnalyzeChart
from document_agents.document_process_tools import build_document_process_tools
from utils.qwen_api import init_qwen_with_langchain
from utils.format_utils import format_messages





# System prompt for the agent
SYSTEM_PROMPT = f"""You are a Document Intelligence Agent. 
You analyze documents by combining OCR text with visual analysis tools.

## Document Text (in reading order)
The following text was extracted using OCR and ordered using LayoutLM.

{ordered_text_str}

## Document Layout Regions
The following regions were detected in the document:

{layout_regions_str}

## Your Tools
- **AnalyzeChart(region_id)**: 
    - Use for chart/figure regions to extract data points, axes, and trends
- **AnalyzeTable(region_id)**: 
    - Use for table regions to extract structured tabular data

## Instructions
1. For TEXT regions: 
    - Use the OCR text provided above (it's already extracted)
2. For TABLE regions: 
    - Use the AnalyzeTable tool to get structured data
3. For CHART/FIGURE regions: 
    - Use the AnalyzeChart tool to extract visual data

When answering questions about the document, 
use the appropriate tools to get accurate information.
"""

  


#Prepare context for the agent
def format_ordered_text(ordered_text, max_items=50):
    """Format ordered text for the system prompt."""
    lines = []
    for item in ordered_text[:max_items]:
        lines.append(f"[{item['position']}] {item['text']}")
    
    if len(ordered_text) > max_items:
        lines.append(f"... and {len(ordered_text) - max_items} more text regions")
    
    return "\n".join(lines)

def format_layout_regions(layout_regions):
    """Format layout regions for the system prompt."""
    lines = []
    for region in layout_regions:
        lines.append(f"  - Region {region.region_id}: {region.region_type} (confidence: {region.confidence:.3f})")
    return "\n".join(lines)


class DocumentExtractAgent:
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name
        self.system_prompt = SYSTEM_PROMPT
        self.llm = init_qwen_with_langchain()
        self.tools = [AnalyzeTable,AnalyzeChart]
        self.agent_executor = self.create_agent_executor()

    def create_agent_executor(self):
      """Create an agent executor for document processing.
      Build the agent to orchestrate all components:
      1. Receive question about document
      2. Read system prompt with OCR text and layout info
      3. Decide whether to answer from text or use tools
      4. Call appropriate tools for visual content
      5. Combine information into coherent response`
      """      
      model = self.llm
      system_prompt = SYSTEM_PROMPT
      tools =  self.tools
      # state_schema = self.state_schema

      # Create agent
      agent = create_agent(             # updated for 1.0
          model,
          tools,
          system_prompt=system_prompt,  # updated for 1.0
          # state_schema=state_schema,
         
      ).with_config({"recursion_limit": 20})  #recursion_limit limits the number of steps the agent will run
      return agent
    
    def build_tools()->List[tool]:
        tools = build_document_process_tools()
        return tools
    
    def create_simple_agent_executor(self):
      # Create agent using create_agent directly
      SYSTEM_PROMPT = """You are a helpful assistant designed to extract information from documents.
                   You have access to this tool: OCR tool to extract raw text from images
                   """
      
      model = self.llm
      system_prompt = SYSTEM_PROMPT
      tools =  [ocr_read_document]
      # state_schema = self.state_schema

      # Create agent
      agent = create_agent(             # updated for 1.0
          model,
          tools,
          system_prompt=system_prompt,  # updated for 1.0
          # state_schema=state_schema,
         
      ).with_config({"recursion_limit": 20})  #recursion_limit limits the number of steps the agent will run
      return agent
    
    def create_agent_executor_v0(self, model_name: str = "gpt-3.5-turbo-0613"):
        """Create an agent executor for document processing."""
        # 3. Create the OpenAI-compatible prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant designed to extract information from documents." 
                    "You have access to this tool: "
                    "OCR tool to extract raw text from images "
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # 4. Create a proper tool-calling agent
        agent = create_tool_calling_agent(llm, tools, prompt)

        # 5. Set up the AgentExecutor to run the tool-enabled loop
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        return agent_executor
    
    def run(self, task:str):
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
      
    
      # Use .invoke() with a dictionary input for the agent_executor
      messages =  [
            {
                "role": "user", "content":task ,
            }
        ]
            
      response = self.agent_executor.invoke({"messages":messages})
      format_messages(response["messages"])
      return response
    

if __name__ == "__main__":
  
    # invoice_path = os.path.join("images","ocr_samples", "invoice.png")
    # ooc_text = ocr_read_document(invoice_path)


    agent = DocumentAgentExecutor()

    task = """
    Please process the document at 'invoice.png' under "images/ocr_samples" directory, using the OCR tool and extract the following information in JSON format:
    - tax
    - total
    """
    
    # task = """
    # Extract the Training Cost (FLOPs) for EN-DE for ALL methods from the table.png 
    # using the OCR tool.
    # Return as a list with model name and its training cost.
    # """

    # task = """
    # Please process the document at 'fill_in_the_blanks.jpg' using ocr 
    # and extract the following information in JSON format:
    # - `student name`
    # - `student answer to all the ten questions`
    # """
  
    # task = """
    # Please process the document at 'receipt.jpg' and evaluate the correctness 
    # of the total.
    # """


    result = agent.run(task)
    print(result)