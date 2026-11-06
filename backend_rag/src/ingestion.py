import os, shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Charge les configurations
load_dotenv()
db_dir = os.getenv("CHROMA_DB_DIR")
model_name = os.getenv("EMBEDDING_MODEL")

# 0. Nettoyage
if os.path.exists(db_dir):
    shutil.rmtree(db_dir)
    print(f"Ancienne base supprimée dans {db_dir}.")

# 1. Charger les PDF
# Utilisation d'une liste dynamique basée sur le dossier data
pdf_files = ["Brochure-EMSI.pdf", "Option-IIR.pdf"]
docs = []
for pdf in pdf_files:
    path = os.path.join("data", pdf)
    print(f"Chargement de : {path}")
    loader = PyMuPDFLoader(path)
    docs.extend(loader.load())

# 2. Découper le texte
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", "!", "?", " ", ""]
)
splits = text_splitter.split_documents(docs)
print(f"Nombre de segments créés : {len(splits)}")

# 3. Créer la Vector DB
print(f"Indexation avec le modèle : {model_name}...")
vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=OllamaEmbeddings(model=model_name),
    persist_directory=db_dir
)
print("Base de données vectorielle créée avec succès !")