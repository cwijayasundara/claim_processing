import warnings
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from invoice_processor.invoice_data_extractor import extract_invoice_data
from pathlib import Path
from prompts.claim_prompts import claim_processing_prompt, cash_back_prompt, final_response_prompt
from langchain_openai import ChatOpenAI
from llama_index_rag_agent import search_policy_document

warnings.filterwarnings('ignore')
_ = load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'

policy_document_path = "docs/policy/pb116349-business-health-select-handbook-1024-pdfa.pdf"

llm = ChatOpenAI(model="gpt-4o-2024-08-06",
                 temperature=0)

claim_processing_prompt_str = ChatPromptTemplate.from_template(claim_processing_prompt)

claim_chain = claim_processing_prompt_str | llm

cashback_prompt_str = ChatPromptTemplate.from_template(cash_back_prompt)

cash_back_chain = cashback_prompt_str | llm

final_response_prompt_str = ChatPromptTemplate.from_template(final_response_prompt)

final_response_chain = final_response_prompt_str | llm

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
         "Make a Claim!",
         "ClaimGenius - Design")
    )

if add_radio == "Chat with your Policy Assistant":
    st.header("Chat with your Policy Assistant")

    st.write("Example questions you can ask:")
    st.write("What is the cashback amount for dental fees per year? ")
    st.write("What is the cashback amount for optical fees per?")

    request = st.text_area(f"How can I help you with the policy document knowledge base today?", height=100)
    submit = st.button("submit", type="primary")

    if request and submit:
        # chat_result = chroma_db_upload_verifier(request)
        # chat_result = retriever_with_reranker(request)
        chat_result = search_policy_document(policy_document_path, request)
        st.write(f"chat_result: :blue[{chat_result}]")

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
        # policy_section = chroma_db_upload_verifier(claim_section_prompt)
        # policy_section = retriever_with_reranker(claim_section_prompt)
        policy_section = search_policy_document(policy_document_path, claim_section_prompt)
        st.write(f"policy_section: :blue[{policy_section}]")

        claim_details_extracted = extracted_invoice_data.invoice_total + " " + extracted_invoice_data.treatment_type
        # print(claim_details_extracted)
        st.write(f"claim_details_extracted: :blue[{claim_details_extracted}]")

        # Process the claim
        claim_response = claim_chain.invoke({"POLICY_SECTION": policy_section,
                                 "CLAIM_DETAILS": claim_details_extracted})
        # write the response to the streamlit app
        st.write(f":blue[{claim_response.content}]")

        # Extract the cashback amount and treatment type from the claim response
        cash_back_amount = cash_back_chain.invoke({"text": claim_response.content})

        st.write(cash_back_amount.content)

        # Generate the final response
        final_response = final_response_chain.invoke({"invoice_data": extracted_invoice_data,
                                                      "claim_decision": claim_response.content})
        st.write(f":red[{final_response.content}]")
        
elif add_radio == "ClaimGenius - Design":

    st.header("ClaimGenius - Business Flow")
    st.image("images/business_flow.jpg")

    st.header("ClaimGenius - Design")
    st.image("images/claims-Page-2.jpg")

    st.write("ClaimGenius is an AI assistant that helps you with your insurance claims.")
    st.write("It can help you with your policy document knowledge base, help you with your claims, and more.")
    st.write("Feel free to chat with your Policy Assistant or make a claim to get started!")














