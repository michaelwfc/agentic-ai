"""
# Lab 4: Document Understanding with Agentic Document Extraction

In this lab, you will use LandingAI's Agentic Document Extraction (ADE) framework to parse documents and extract key-value pairs using a single API. Note that Lab 4 has two parts. Here in the first part, we cover Exercise 1: Extract Key-Value Pairs from a Utility Bill and Exercise 2: ADE on Difficult Documents. In the second part, we cover Exercise 3: Automated Pipeline for Loan Applications.   

**Learning Objectives:**
- Use the Parse API to convert documents into structured markdown with visual grounding
- Define JSON schemas to extract specific fields from documents
- Use the Extract API to pull key-value pairs with source location references

Initialize the ADE client. The API key is loaded automatically from the environment variable `VISION_AGENT_API_KEY`.

To use ADE outside this course, you can generate a free API key at [va.landing.ai](https://va.landing.ai).
"""
import json
from enum import Enum
from pydantic import BaseModel, Field
from landingai_ade.lib import pydantic_to_json_schema
from landingai_ade import LandingAIADE
from landingai_ade.types import ParseResponse, ExtractResponse
from document_agents.helper import print_document, draw_bounding_boxes, draw_bounding_boxes_2
from document_agents.helper import create_cropped_chunk_images


bill_schema_dict = {
    "type": "object",
    "title": "Utility Bill Field Extraction Schema",
    "properties": {
    "account_summary": {
      "type": "object",
      "title": "Account Summary",
      "properties": {
        "current_charges": {
          "type": "number",
          "description": "The charges incurred during the current billing "
            "period."
        },
        "total_amount_due": {
          "type": "number",
          "description": "The total amount currently due."
        }
      }
    },
    "gas_summary": {
      "type": "object",
      "title": "Gas Usage Summary",
      "properties": {
        "total_therms_used": {
          "type": "number",
          "description": "Total therms of gas used in the billing period."
        },
        "gas_current_charges": {
          "type": "number",
          "description": "The gas charges incurred during the current "
            "billing period."
        },
        "gas_usage_chart": {
          "type": "boolean",
          "description": "Does the document contain a chart of historical "
            "gas usage?"
        },
        "gas_max_month": {
          "type": "string",
          "description": "Which month has the highest historical gas usage? "
            "Return month name only."
        }
      }
    },
    "electric_summary": {
      "type": "object",
      "title": "Electric Usage Summary",
      "properties": {
        "total_kwh_used": {
          "type": "number",
          "description": "Total kilowatt hours of electricity used in the "
            "billing period."
        },
        "electric_current_charges": {
          "type": "number",
          "description": "The gas charges incurred during the current "
            "billing period."
        },
        "electric_usage_chart": {
          "type": "boolean",
          "description": "Does the document contain a chart of historical "
            "electric usage?"
        },
        "electric_max_month": {
          "type": "string",
          "description": "Which month has the highest historical electric "
            "usage? Return month name only."
        }
      }
    }
  }
}


class DocumentType(str, Enum):
    ID = "ID"
    W2 = "W2"
    pay_stub = "pay_stub"
    bank_statement = "bank_statement"
    investment_statement = "investment_statement"

    # Descriptions for each value
    def describe(self) -> str:
        descriptions = {
            "ID": "An official government identification such as a "
            "passport or driver's license.",
            "W2": "A year-end W-2 form reporting annual taxable wages "
            "and withholdings.",
            "pay_stub": "A periodic employee earnings statement.",
            "bank_statement": "A checking or savings account statement "
            "with balances and transactions.",
            "investment_statement": "A brokerage or investment account "
            "statement showing holdings, value, and transactions.",
        }
        return descriptions[self.value]

class DocType(BaseModel):
    type: DocumentType = Field(
        description="The type of document being analyzed.",
        title="Document Type",
    )


# ---------------------------------------------------------
# Schema for ID
# ---------------------------------------------------------
class IDSchema(BaseModel):
    name: str = Field(description="Full name of the person", 
                      title="Full Name")
    issuer: str = Field(description="The state or country issuing the "
                        "identification.", title="Issuer")
    issue_date: str = Field(description="The issue date for the "
                            "identification.", title="Issue Date")
    identifier: str = Field(description="The unique identifier such as a "
                            "drivers license number or passport number", 
                            title="Identifier")

# ---------------------------------------------------------
# Schema for W2
# ---------------------------------------------------------
class W2Schema(BaseModel):
    employee_name: str = Field(description="The name of the employee.", 
                               title="Employee Name")
    employer_name: str = Field(description="The name of the employer "
                               "organization issuing the W2.", 
                               title="Employer Name")
    w2_year: int = Field(description="The year of the W2 form.", 
                         title="W2 Year")
    wages_box_1: float = Field(description="The total wages shown in box 1 "
                               "of the form", title="Box 1")

# ---------------------------------------------------------
# Schema for Pay Stubs
# ---------------------------------------------------------
class PaymentStubSchema(BaseModel):
    employee_name: str = Field(description="The name of the employee.", 
                               title="Employee Name")
    employer_name: str = Field(description="The name of the employer "
                               "organization.", title="Employer Name")
    pay_period: str = Field(description="The pay period for the stub.",
                            title="Pay Period")
    gross_pay: float = Field(description="The gross pay amount.",
                             title="Gross Pay")
    net_pay: float = Field(description="The net pay amount after "
                           "deductions.", title="Net Pay")
    
# ---------------------------------------------------------
# Schema for Bank Statements
# ---------------------------------------------------------
class BankStatementSchema(BaseModel):
    account_owner: str = Field(description="The name of the account "
                               "owner(s).", title="Account Owner")
    bank_name: str = Field(description="The name of the bank.", 
                           title="Bank Name")
    account_number: str = Field(description="The bank account number.", 
                                title="Account Number")
    end_date: str = Field(description="The ending date for the statement.", 
                          title="End Date")
    balance: float = Field(description="The current balance of the bank "
                           "account.", title="Bank Balance")

# ---------------------------------------------------------
# Schema for Investment Statements
# ---------------------------------------------------------
class InvestmentStatementSchema(BaseModel):
    account_owner: str = Field(description="The name of the account owner(s)."
                               , title="Account Owner")
    institution_name: str = Field(description="The name of the financial "
                                  "institution.", title="Institution Name")
    investment_year: int = Field(description="The year of the investment "
                                 "statement.", title="Investment Year")
    investment_value: float = Field(description="The total value of the "
                                    "account as of the statement end date.", 
                                    title="Investment Balance")

# ---------------------------------------------------------
# Map document types to their corresponding schemas
# ---------------------------------------------------------
schema_per_doc_type = {
    "bank_statement": BankStatementSchema,
    "investment_statement": InvestmentStatementSchema,
    "pay_stub": PaymentStubSchema,
    "ID": IDSchema,
    "W2": W2Schema,
}


class LandingAIADEAgent:
  def __init__(self):
    # Initialize the client
    self.client = LandingAIADE()
    print("Authenticated client initialized")

  
  def extract_key_value_pairs(self, image_path: str) -> ExtractResponse:
      """
      ## 3. Exercise 1: Extract Key-Value Pairs from a Utility Bill
      Parse a utility bill and extract specific fields like current charges, gas usage, and electric usage. The workflow:
      1. Preview the document
      2. Parse with DPT-2 to get structured markdown and chunks
      3. Extract key-value pairs using a JSON schema
      """
      parse_result = self._parse(file_path)
      # Convert the dictionary into a JSON-formatted string
      schema_json = json.dumps(bill_schema_dict)


      print("⚡ Calling API to extract from the document...")

      # Using the Extract() API to extract structured data using the schema
      extraction_result: ExtractResponse = client.extract(
                  schema=schema_json,
                  markdown=parse_result.markdown, # Notice that the input used is the top-level markdown from the parse step
                  model="extract-latest"
      )

      print(f"Extraction completed.")

      # View all extracted values
      extraction_result.extraction
      return extraction_result
  
  def _parse(self, file_path):
    """
    ### 3.2 Parse the Document

    The Parse API converts the document into structured markdown with:
    - Chunks: Semantic regions (text, tables, figures, logos, marginalia)
    - Bounding boxes: Coordinates for each chunk
    - Markdown: Text representation with embedded chunk IDs

    Using `dpt-2-latest` provides the most current version of the DPT-2 model.
    """
    # Specify the file path to the document
    document_path = Path("utility_example/utility_bill.pdf")

    print("⚡ Calling API to parse document...")

    # Parse the document using the Parse() API
    parse_result: ParseResponse = client.parse(
        document=document_path,
        model="dpt-2-latest"
    )

    print(f"Parsing completed.")
    print(f"job_id: {parse_result.metadata.job_id}")
    print(f"Filename: {parse_result.metadata.filename}")
    print(f"Total time (ms): {parse_result.metadata.duration_ms}")
    print(f"Total pages: {len(parse_result.splits)}")
    print(f"Total markdown characters: {len(parse_result.markdown)}")
    print(f"Total chunks: {len(parse_result.chunks)}")


    # Create and view an annotated version
    draw_bounding_boxes(parse_result, document_path)

    print(f"The first chunk has an id: {parse_result.chunks[0].id}")
    print(f"The first chunk is type: {parse_result.chunks[0].type}")
    print(f"The first chunk is on page: {parse_result.chunks[0].grounding.page}")
    print(f"The first chunk is at box coordinates: {parse_result.chunks[0].grounding.box}")


    # Chunk-level markdown rendered
    display(HTML(parse_result.chunks[9].markdown))
    return parse_result
  

  def parse_document(self, parse_filename: str, model = "dpt-2-latest", 
                   display_option = "HTML") -> ParseResponse:
    """
    Parse a document with ADE and display the result in the desired format.

    Args:
        parse_filename: Path to the document to parse.
        display_option: One of:
            - "Raw Markdown" : print the markdown as plain text
            - "HTML"         : render the markdown as HTML in the notebook

    Returns:
        ParseResponse: The full parse response object.
    """

    document_path = Path(parse_filename)
    
    print("⚡ Calling API to parse document...")
    
    full_parse_result: ParseResponse = client.parse(  
        #send document to Parse API
        document=document_path, 
        model=model
    )

    _ = draw_bounding_boxes(full_parse_result, document_path=document_path)

    print(f"Parsing completed.")
    print(f"job_id: {full_parse_result.metadata.job_id}")
    print(f"Total pages: {len(full_parse_result.splits)}")
    print(f"Total time (ms): {full_parse_result.metadata.duration_ms}")
    print(f"Total markdown characters: {len(full_parse_result.markdown)}")
    print(f"Number of chunks: {len(full_parse_result.chunks)}")
    print(f" ")
    print("Complete Markdown:")

    if display_option == "Raw Markdown":
        print("Complete Markdown (raw):")
        print(full_parse_result.markdown)

    elif display_option == "HTML":
        print("Rendering markdown as HTML...")
        display(HTML(full_parse_result.markdown))

    else:
        print(
            f"[Unknown display_option '{display_option}'; "
            "valid options are 'Raw Markdown' or 'HTML'. "
            "Defaulting to HTML.]"
        )
        display(HTML(full_parse_result.markdown))


  def _parse_on_directory(self, directory_path: str, display_option: str = "HTML"):
      input_folder = Path("input_folder")

      # Convert the document type schema to JSON format for API calls
      doc_type_json_schema = pydantic_to_json_schema(DocType)

      # Dictionary to store document types and parse results
      document_types = {}

      # Process each document in the folder
      for document in input_folder.iterdir():

          # 🔥 Skip directories so ADE doesn't try to parse them
          if document.is_dir():
              continue
              
          print(f"Processing document: {document.name}")

          # Step 1: Parse the document to extract layout and content
          parse_result: ParseResponse = client.parse(
              document=document,
              split="page",  #Notice that each document is being split by page.
              model="dpt-2-latest"
          )
          print("Parsing completed.")
          print(" ")
          
          # Notice that we only use the first page to determine the document type
          first_page_markdown = parse_result.splits[0].markdown  
          
          # Step 2: Extract document type using the categorization schema
          print("Extracting Document Type...")
          extraction_result: ExtractResponse = client.extract(
              schema=doc_type_json_schema,
              markdown=first_page_markdown
          )
          doc_type = extraction_result.extraction["type"]
          print(f"Document Type Extraction: {doc_type}\n")
          print("       ----------         ")
          print(" ")
          
          # Store results for later use
          document_types[document] = {
              "document_type": doc_type,
              "parse_result": parse_result
          }
      return document_types
  

  def extract_multiple_documents(self):
    """
    # Lab 4: Document Understanding with Agentic Document Extraction II

    In this lab, you will process multiple documents, categorize their types, and extract specific fields according to their respective schemas.

    **Learning Objectives:**
    - Specify extraction schemas with Pydantic 
    - Implement categorization of documents by type
    - Build validation logic into extracted information

    ## Background

    Banks receive loan application documents with arbitrary filenames (eg "uploadA.pdf", "image456.jpg"). The workflow must:
    1. Identify each document type (pay stub, W2, bank statement, etc.)
    2. Extract relevant fields based on a schema pertaining to that document type
    3. Validate that all documents belong to the same applicant


    ## 3. Full Document Processing Pipeline: Loan Automation

    Imagine you work at a bank reviewing loan applications. Applicants upload various financial documents with arbitrary names. Your pipeline needs to:

    1. **Parse** all documents to understand their content
    2. **Categorize** each document (Is it a pay stub? Bank statement? ID?)
    3. **Extract** the relevant fields based on document type
    4. **Validate** that all documents belong to the same person
    """
    document_types =self._parse_dir()
    # Dictionary to store extraction results
    document_extractions = {}

    # Extract financial data from each document using its specific schema
    for document, extraction in document_types.items():
        print(f"Processing document: {document.name}")

        # Get the appropriate schema for this document type
        json_schema = pydantic_to_json_schema(
            schema_per_doc_type[extraction["document_type"]]
        )

        # Extract structured data using the schema
        extraction_result: ExtractResponse = client.extract(
            schema=json_schema,
            markdown=extraction["parse_result"].markdown
        )
        print("Detailed Extraction:", extraction_result.extraction)

        # Store extraction results
        document_extractions[document] = {
            "extraction": extraction_result.extraction,
            "extraction_metadata": extraction_result.extraction_metadata,
        }

    print(document_extractions)


    # Combine all extraction data
    final_extractions = {}

    for document, extraction in document_extractions.items():
        final_extractions[document] = {
            **extraction,
            **document_types[document],
        }

    # Visualize all parsed chunks for each document
    for document, extraction in final_extractions.items():
        print(f"Visualizing document: {document.name}")
        base_path = f"results/{document.stem}"
        os.makedirs(base_path, exist_ok=True)
        draw_bounding_boxes_2(
            extraction["parse_result"].grounding,
            document,
            base_path=base_path
        )

    # 3.7 Visualize Extracted Fields Only
    # For human-in-the-loop systems, highlight only the extracted fields to show reviewers where values originated.
    for document, extraction in final_extractions.items():
      print(f"Visualizing extracted fields for: {document.name}")
      base_path = f"results_extracted/{document.stem}"

      parse_result = extraction["parse_result"]
      document_grounds = {}

      for label, metadata_value in extraction["extraction_metadata"].items():
          chunk_id = metadata_value["references"][0]
          grounding = parse_result.grounding[chunk_id]
          document_grounds[chunk_id] = grounding

      draw_bounding_boxes_2(
          document_grounds,  # dict of chunk_id -> grounding
          document,
          base_path=base_path
      )


      # Collect all the fields into a summary dataframe
      rows = []

      for document, info in document_extractions.items():
          extraction = info["extraction"]
          doc_type = document_types[document]["document_type"]  # from your classification step

          input_folder = document.parent.name
          document_name = document.name

          for field, value in extraction.items():
              rows.append({
                  "applicant_folder": input_folder,
                  "document_name": document_name,
                  "document_type": doc_type,
                  "field": field,
                  "value": value,
              })

      df = pd.DataFrame(rows)

  def validate_extraction(self, extraction):
      """
      ### 3.9 Validation Logic

      Apply business logic to validate the submission:
      - **Name matching**: Verify all documents belong to the same person
      - **Year verification**: Check all documents are from recent years
      - **Asset totals**: Calculate the applicant's total net worth
      """
      chech_name_matching(df)
      check_year()
      check_totol_asserts()
  
def chech_name_matching(df):
    # Check 1: Name Matching
    # Verify that all name fields across documents match to catch mismatched submissions.

    # Logic check to determine whether the five name fields extracted 
    # from five documents match each other.

    name_fields = {"account_owner", "employee_name", "name"}
    df_names = df[df["field"].isin(name_fields)].copy()
    all_names_match = df_names["value"].nunique() == 1

    if all_names_match:
        print("✅ All 5 name fields match!")
    else:
        print("❌ The name fields do NOT match.")
        print("Values found:")
        print(df_names[["document_name", "field", "value"]])

    
 

def check_year(df):
    # 1. Fields that may contain a year
    year_fields = {
        "w2_year",
        "investment_year",
        "issue_date",
        "end_date",
        "pay_period",
    }

    # 3. Build a table of years per document
    year_rows = []

    for doc_name in df["document_name"].unique():
        doc_df = df[df["document_name"] == doc_name]

        # Only rows whose field is one of our year-related fields
        doc_year_fields = doc_df[doc_df["field"].isin(year_fields)]

        for _, row in doc_year_fields.iterrows():
            year_value = extract_year(row["value"])
            year_rows.append({
                "document_name": doc_name,
                "field": row["field"],
                "value": row["value"],
                "year_extracted": year_value,
            })

    df_years = pd.DataFrame(year_rows)

    print("Per-document year info:")
    print(df_years)

# 2. Helper to pull a 4-digit year out of a string/number
def extract_year(value):
    """
    Return a 4-digit year (1900–2099) from a value, or None if none found.
    """
    if value is None:
        return None
    match = re.search(r"\b(19|20)\d{2}\b", str(value))
    return int(match.group(0)) if match else None

def check_totol_asserts():
    # Logic to sum all bank balances and all investment balances from your extraction

    # Define fields
    bank_balance_field = "balance"
    investment_balance_field = "investment_value"

    # Filter rows
    df_bank = df[df["field"] == bank_balance_field].copy()
    df_invest = df[df["field"] == investment_balance_field].copy()

    # Ensure numeric
    df_bank["value"] = pd.to_numeric(df_bank["value"], errors="coerce")
    df_invest["value"] = pd.to_numeric(df_invest["value"], errors="coerce")

    # Compute totals
    total_bank = df_bank["value"].sum()
    total_investments = df_invest["value"].sum()
    total_assets = total_bank + total_investments

    # Print
    print(f"Total Bank Balances: ${total_bank:,.2f}")
    print(f"Total Investment Balances: ${total_investments:,.2f}")
    print(f"Total Assets: ${total_assets:,.2f}")