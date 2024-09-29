import warnings
from dotenv import load_dotenv
from invoice_processor.invoice_data_extractor import extract_invoice_data
from chroma_retriever import chroma_db_upload_verifier

warnings.filterwarnings('ignore')
_ = load_dotenv()


# load the invoice data
invoice_location = "invoices/sample_invoice_1.pdf"
invoice_data = extract_invoice_data(invoice_location)

#  extract the invoice_number from the invoice_data dictionary
invoice_number = invoice_data.invoice_number
patient_name = invoice_data.patient_name
patient_address = invoice_data.patient_address
treatment_type = invoice_data.treatment_type
invoice_total = invoice_data.invoice_total
clinic_name = invoice_data.clinic_name

response = chroma_db_upload_verifier(f"Please provide the cashback amount for {treatment_type} fees per year.")
print(response)
