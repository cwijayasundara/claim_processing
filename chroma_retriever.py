import warnings
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain.chains import RetrievalQA

warnings.filterwarnings('ignore')
_ = load_dotenv()

persistent_dir = 'vectorstore'

vectorstore = Chroma(persist_directory=persistent_dir,
                     embedding_function=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

llm = ChatOpenAI(model="gpt-4o-2024-08-06",
                 temperature=0,
                 timeout=None,
                 streaming=True)

compressor = CohereRerank(model="rerank-english-v3.0")

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)

chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=compression_retriever
)

def chroma_db_upload_verifier(query):

    template = """Answer the question based only on the following context, which can include text and tables:
    {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # RAG pipeline
    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    return chain.invoke(query)

def retriever_with_reranker(query):
    response_with_rerank = chain.invoke({"query": query})
    return response_with_rerank

# query_1 = "What is the cashback amount for optical fees per year?"
# query_2 = "Whats the cashback amount for dental fees per year? "
#
# response_plain_1 = chroma_db_upload_verifier(query_1)
# print("plain response 1", response_plain_1)
# response_plain_2 = chroma_db_upload_verifier(query_2)
# print("plain response 2", response_plain_2)
#
# response_rerank_1 = retriever_with_reranker(query_1)
# print("response with rerank 1", response_rerank_1['result'])
# response_rerank_2 = retriever_with_reranker(query_2)
# print("response with rerank 2", response_rerank_2['result'])


