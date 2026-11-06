from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# 1. Charger la base existante
vectorstore = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=OllamaEmbeddings(model="llama3.2")
)

# 2. Extraire les données
data = vectorstore.get()

print(f"Nombre de segments (chunks) dans la base : {len(data['ids'])}")
print("\n--- Aperçu des 3 premiers segments ---")

for i in range(min(3, len(data['documents']))):
    print(f"\nID: {data['ids'][i]}")
    print(f"Source: {data['metadatas'][i]['source']}")
    print(f"Contenu: {data['documents'][i][:100]}...") # Affiche les 100 premiers caractères