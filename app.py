import warnings
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from chroma_retriever import chroma_db_upload_verifier, retriever_with_reranker
from invoice_processor.invoice_data_extractor import extract_invoice_data
from pathlib import Path
from prompts.claim_prompts import claim_processing_prompt
from langchain_openai import ChatOpenAI

warnings.filterwarnings('ignore')
_ = load_dotenv()

llm = ChatOpenAI(model="gpt-4o-2024-08-06",
                 temperature=0)

claim_processing_prompt_str = ChatPromptTemplate.from_template(claim_processing_prompt)

claim_chain = claim_processing_prompt_str | llm

st.title("ClaimGenius : Your AI Assistant for Insurance Claims")

def sanitize_filename(filename):
    """
    Sanitize the filename to prevent path traversal attacks and remove unwanted characters.
    """
    # Remove any directory components
    filename = os.path.basename(filename)
    # Remove any characters that are not alphanumeric, dot, underscore, or hyphen
    filename = "".join(c for c in filename if c.isalnum() or c in (" ", ".", "_", "-")).rstrip()
    return filename

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image("images/img_1.png")
    add_radio = st.radio(
        "What can I do for you today?",
        ("Chat with your Policy Assistant",
         "Make a Claim!",)
    )

if add_radio == "Chat with your Policy Assistant":
    st.header("Chat with your Policy Assistant")

    request = st.text_area(f"How can I help you with the policy document knowledge base today?", height=100)
    submit = st.button("submit", type="primary")

    st.write("Example questions you can ask:")
    st.write("What is the cashback amount for dental fees per year? ")
    st.write("What is the cashback amount for optical fees per?")

    if request and submit:
        chat_result = chroma_db_upload_verifier(request)
        # chat_result = retriever_with_reranker(request)
        st.write(chat_result)

elif add_radio == "Make a Claim!":
    st.header("Make a Claim!")
    st.write("Please upload your invoice to get started")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        upload_dir = Path.cwd() / "uploaded_invoices"
        upload_dir.mkdir(parents=True, exist_ok=True)
        original_filename = Path(uploaded_file.name).name  # Extract the filename
        sanitized_filename = sanitize_filename(original_filename)
        save_path = upload_dir / sanitized_filename
        # convert the same path to string
        save_path = str(save_path)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved successfully to: {save_path}")

        extracted_invoice_data = extract_invoice_data(save_path)
        st.write(extracted_invoice_data)

        # Extract the policy section based on the treatment type
        treatment_type = extracted_invoice_data.treatment_type
        claim_section_prompt = f"""What is the cashback amount for {treatment_type} fees per year?"""
        policy_section = chroma_db_upload_verifier(claim_section_prompt)
        # policy_section = retriever_with_reranker(claim_section_prompt)
        st.write(policy_section)

        claim_details_extracted = extracted_invoice_data.invoice_total + " " + extracted_invoice_data.treatment_type
        print(claim_details_extracted)

        # Process the claim
        claim_response = claim_chain.invoke({"POLICY_SECTION": policy_section,
                                 "CLAIM_DETAILS": claim_details_extracted})

        st.write(claim_response.content)














