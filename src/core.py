# Langchain componenets
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents.base import Document
# providing the AstraDB integration with langchain
import cassio
# read the pdfs
from PyPDF2 import PdfReader
from typing_extensions import Concatenate
# load env vars
import os
from dotenv import load_dotenv
load_dotenv()

def get_keys():
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
    OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
    return ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_ID, OPENAI_API_KEY

def input_pdf(path):
    return PdfReader(path)

def extract_text(pdfreader):
    # extract all text from pdf
    raw_text = ''
    for i, page in enumerate(pdfreader.pages):
        content= page.extract_text()
        if content:
            raw_text += content
    return raw_text

def init_connection(ASTRA_DB_APPLICATION_TOKEN,ASTRA_DB_ID):
    # Conncetion with the AstraDB
    cassio.init(token= ASTRA_DB_APPLICATION_TOKEN, database_id= ASTRA_DB_ID)
    return

def init_llm(openai_api_key):
    llm = OpenAI(openai_api_key = openai_api_key)
    return llm

def init_embedding(openai_api_key):
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    return embedding

def create_vector_store(embedding, table_name= "qa_table"):
    # Create Langchain Vector Store
    astra_vector_store = Cassandra(
        embedding= embedding,
        table_name=table_name,
        session= None,
        keyspace=None,
    )
    return astra_vector_store

def split_text(raw_text, chunk_size=800, chunk_overlap=200):
    # Split text into chuncks to not increase the token size
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function= len,
    )
    texts = text_splitter.split_text(raw_text)
    return texts

def texts_to_document(texts):
    return Document(page_content=texts)

def add_text_into_db(astra_vector_store, texts):
    text_id= astra_vector_store.add_texts(texts)
    astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)
    return astra_vector_index, text_id

