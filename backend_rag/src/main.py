from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, HTMLResponse
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from fastapi.middleware.cors import CORSMiddleware
import os, asyncio
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="EMSI RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation
embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL")
)

vectorstore = Chroma(
    persist_directory=os.getenv("CHROMA_DB_DIR"),
    embedding_function=embeddings
)

llm = ChatOllama(
    model=os.getenv("LLM_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL")
)

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_pdf(query: Query):
    k_value = int(os.getenv("RAG_K_NEIGHBORS", 4))

    # Exécution asynchrone non-bloquante pour la recherche vectorielle
    docs = await asyncio.to_thread(vectorstore.similarity_search, query.question, k=k_value)
    context = "\n".join([f"Extrait {i+1}: {d.page_content}" for i, d in enumerate(docs)])

    prompt = f"""Tu es l'assistant IA expert de l'EMSI (École Marocaine des Sciences de l'Ingénieur).
Ta mission est d'aider les utilisateurs en utilisant EXCLUSIVEMENT les documents fournis.

CONSIGNES DE RÉPONSE :
1. Utilise les extraits ci-dessous pour répondre à la question. 
2. Tu as le droit de synthétiser les informations si elles sont éparpillées dans plusieurs extraits.
3. Si la question ne concerne PAS l'EMSI ou ses filières, réponds : "Je suis programmé pour répondre uniquement aux questions concernant l'EMSI."
4. Si l'information est introuvable dans les documents, réponds : "Désolé, je ne trouve pas cette information précise dans les brochures de l'EMSI."

CONTEXTE :
{context}

QUESTION : 
{query.question}

RÉPONSE : """

    async def generate_stream():
        async for chunk in llm.astream(prompt):
            if chunk.content:
                # Nettoyage des tokens de fin
                text_chunk = chunk.content.replace("[/INST]", "").replace("</s>", "")
                if text_chunk:
                    yield text_chunk

    # Headers indispensables pour forcer les proxys/clients à ne pas tamponner le stream
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }

    return StreamingResponse(generate_stream(), media_type="text/event-stream", headers=headers)

@app.get("/visualize", response_class=HTMLResponse)
async def visualize_db():
    data = vectorstore.get(include=['documents', 'metadatas'])      # On récupère tout le contenu
    rows = ""       # On génère un petit tableau HTML
    for i in range(len(data['ids'])):
        content = data['documents'][i][:200] + "..." # On coupe le texte pour la lisibilité
        metadata = data['metadatas'][i]
        rows += f"<tr><td>{data['ids'][i]}</td><td>{content}</td><td>{metadata}</td></tr>"

    html_content = f"""
    <html>
        <head><title>ChromaDB Viewer</title></head>
        <body style="font-family: sans-serif; padding: 20px;">
            <h1>Contenu de la base de données ({len(data['ids'])} segments)</h1>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr style="background: #f4f4f4;">
                    <th>ID</th><th>Extrait du document</th><th>Métadonnées</th>
                </tr>
                {rows}
            </table>
        </body>
    </html>
    """
    return html_content