from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# On charge la base
db = Chroma(persist_directory="./chroma_db", embedding_function=OllamaEmbeddings(model="llama3.2"))

# On récupère tout le contenu
content = db.get()

print(f"Nombre de chunks stockés : {len(content['ids'])}")
for i in range(min(5, len(content['documents']))):
    print(f"\n--- Chunk {i+1} (Source: {content['metadatas'][i]['source']}) ---")
    print(content['documents'][i][:200] + "...") # Affiche les 200 premiers caractères