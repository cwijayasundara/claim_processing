import warnings
import ssl
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_community.document_loaders import UnstructuredPDFLoader
ssl._create_default_https_context = ssl._create_unverified_context

warnings.filterwarnings('ignore')
_ = load_dotenv()

# GPT model that supports structured output
llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0)

class Invoice(BaseModel):
    """Information about the items on an invoice"""
    invoice_number:str = Field(description="The invoice number on the invoice")
    invoice_date:str = Field(description="The date on the invoice. Format: DD/MM/YYYY HH:MM. Example: 09/07/2024 12:47")
    patient_name:str = Field(description="The patient name given on the invoice")
    patient_address:str = Field(description="The patient address given on the invoice")
    treatment_type:str = Field(description="The type of treatment given to the patient. dental, optical, etc.")
    invoice_total:str = Field(description="The total of the invoice that the patient has to pay")
    clinic_name:str = Field(description="The name of the clinic that issued the invoice")
    clinic_address:str = Field(description="The address of the clinic that issued the invoice")


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert in extracting information from invoices. "
            "Only extract invoice information in JSON and nothing else."
        ),
        ("human", "{text}"),
    ]
)

structured_llm = llm.with_structured_output(Invoice)

def get_invoice_content(file_path):
    loader = UnstructuredPDFLoader(file_path)
    data = loader.load()
    return data[0].page_content

def extract_invoice_data_by_str(invoice_content: str) -> dict:
    response = structured_llm.invoke(invoice_content)
    print(response)
    return response

#  write a function to extract the invoice data
def extract_invoice_data(invoice_location_str: str) -> dict:
    invoice_content = get_invoice_content(invoice_location_str)
    response = structured_llm.invoke(invoice_content)
    print(response)
    return response

# test the invoice data extraction function
# invoice_location = "../invoices/sample_invoice_1.pdf"
# invoice_data = extract_invoice_data(invoice_location)
# print(invoice_data)
# invoice_number = invoice_data["invoice_number"]
# print(f"Invoice Number: {invoice_number}")