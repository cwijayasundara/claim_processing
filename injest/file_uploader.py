from pdf_loader import upload_pdf_file_to_vector_db

policy_file_path = "../docs/policy/pb116349-business-health-select-handbook-1024-pdfa.pdf"

# upload the content of a pdf file to the vector database
upload_pdf_file_to_vector_db(policy_file_path, "../vectorstore")