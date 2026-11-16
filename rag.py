import os
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

load_dotenv()

folder = os.path.dirname(os.path.abspath(__file__))
pdf_file = os.path.join(folder, "products_catalog.pdf")
db_folder = os.path.join(folder, "chroma_db")

chroma_client = chromadb.PersistentClient(path=db_folder)

embedding_function = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small",
)

collection = chroma_client.get_or_create_collection(
    name="products",
    embedding_function=embedding_function,
)

if collection.count() == 0:
    reader = PdfReader(pdf_file)
    full_text = ""
    for page in reader.pages:
        full_text = full_text + page.extract_text() + "\n"

    parts = full_text.split("Product Name:")
    chunks = []
    for part in parts:
        if part.strip() != "":
            chunks.append("Product Name:" + part.strip())

    chunks[0] = parts[0].strip()

    ids = []
    for i in range(len(chunks)):
        ids.append("chunk_" + str(i))

    collection.add(documents=chunks, ids=ids)
