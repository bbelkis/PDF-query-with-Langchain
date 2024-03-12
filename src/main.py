from fastapi import FastAPI, UploadFile
import src.core as core
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

# Create FastAPI instance
app = FastAPI()

# Load OpenAI API key, AstraDB API key and the AstraDB ID
ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_ID, OPENAI_API_KEY= core.get_keys()

# Init openAI models
LLM = core.init_llm(OPENAI_API_KEY)
EMBEDDING = core.init_embedding(openai_api_key=OPENAI_API_KEY)

# Establish database connection
core.init_connection(ASTRA_DB_APPLICATION_TOKEN,ASTRA_DB_ID)

# Create the vector store
ASTRA_VECTOR_STORE= core.create_vector_store(EMBEDDING, table_name= "pdf_table")


# Define route to process uploaded files
@app.post("/uploadfile/")
async def process_pdf(file: UploadFile):
    # Read the pdf
    pdfreader = core.input_pdf(file.file)
    # Extract text from pdf
    raw_text = core.extract_text(pdfreader)
    # Chunck text
    texts = core.split_text(raw_text, chunk_size=800, chunk_overlap=200)
    astra_vector_index, text_id = core.add_text_into_db(ASTRA_VECTOR_STORE, texts)
    return texts[:3]

# Define route for question answering
@app.post("/qa/")
def qa(question:str):
    astra_vector_index = VectorStoreIndexWrapper(vectorstore=ASTRA_VECTOR_STORE)
    # Query for the answer
    answer = astra_vector_index.query(question, llm=LLM).strip()
    similarity=[]
    # Iterate over similar documents
    for doc, score in ASTRA_VECTOR_STORE.similarity_search_with_score(question, k=3):
            sim=dict()
            sim['score']=score
            sim['text']=doc.page_content[:300]
            similarity.append(sim)
    return answer, similarity





