import warnings
import os

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from unstructured.staging.base import dict_to_elements
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

warnings.filterwarnings('ignore')
_ = load_dotenv()

DLAI_API_KEY = os.environ.get("DLAI_API_KEY")
DLAI_API_URL = os.environ.get("DLAI_API_URL")

unstructured_client = UnstructuredClient(
    api_key_auth=DLAI_API_KEY,
    server_url=DLAI_API_URL,
)

file_path = "../docs/CoT.pdf"

# read the content of a pdf file using the unstructured client
def get_pdf_content(pdf_file_path):

    pdf_elements=[]

    with open(pdf_file_path, "rb") as f:
        files = shared.Files(
            content=f.read(),
            file_name=pdf_file_path,
        )

    req = shared.PartitionParameters(
        files=files,
        strategy="hi_res",
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

embeddings = OpenAIEmbeddings()

pdf_documents = get_pdf_content(file_path)

vectorstore = Chroma.from_documents(pdf_documents, embeddings)

# retriever

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 6}
)

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

template = """You are an AI assistant for answering questions about the Chain of thought documents.
You are given the following extracted parts of a long document and a question. Provide a conversational answer.
If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
If the question is not about Donut, politely inform them that you are tuned to only answer questions about Donut.
Question: {question}
=========
{context}
=========
Answer in Markdown:"""

prompt = PromptTemplate(template=template, input_variables=["question", "context"])

llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0)

doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")

question_generator_chain = LLMChain(llm=llm, prompt=prompt)

qa_chain = ConversationalRetrievalChain(
    retriever=retriever,
    question_generator=question_generator_chain,
    combine_docs_chain=doc_chain,
)

response = qa_chain.invoke({
    "question": "Whats the GSM8K  value of the GPT-3 175B model?",
    "chat_history": []
})["answer"]

print(response)