import warnings
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from unstructured.staging.base import dict_to_elements
from unstructured_client import UnstructuredClient
from unstructured_client.models.errors import SDKError
from langchain_core.documents import Document
from unstructured_client.models import shared
from langchain_openai import OpenAIEmbeddings

warnings.filterwarnings('ignore')
_ = load_dotenv()

DLAI_API_KEY = os.environ.get("DLAI_API_KEY")
DLAI_API_URL = os.environ.get("DLAI_API_URL")

unstructured_client = UnstructuredClient(
    api_key_auth=DLAI_API_KEY,
    server_url=DLAI_API_URL,
)

# read the content of a pdf file using the unstructured client
def get_pdf_content(pdf_file_path):

    with open(pdf_file_path, "rb") as f:
        files = shared.Files(
            content=f.read(),
            file_name=pdf_file_path,
        )

    req = shared.PartitionParameters(
        files=files,
        strategy="hi_res",
        chunking_strategy="by_title",
        hi_res_model_name="yolox",
        skip_infer_table_types=[],
        pdf_infer_table_structure=True,
    )

    try:
        resp = unstructured_client.general.partition(req)
        pdf_elements = dict_to_elements(resp.elements)
    except SDKError as e:
        print(e)

    documents = []
    for element in pdf_elements:
        metadata = element.metadata.to_dict()
        del metadata["languages"]
        metadata["source"] = metadata["filename"]
        print("content in the element", element.text)
        documents.append(Document(page_content=element.text, metadata=metadata))

    return documents


# upload the content of a pdf file to the vector database
def upload_pdf_file_to_vector_db(pdf_file_path, persistent_dir):
    documents = get_pdf_content(pdf_file_path)
    Chroma.from_documents(documents,
                          OpenAIEmbeddings(),
                          persist_directory=persistent_dir)