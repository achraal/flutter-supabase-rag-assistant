# ⚙️ EMSI RAG Backend — FastAPI & ChromaDB

Ce dossier contient le service backend du système RAG pour l'application **EMSI RAG**.

## 🚀 Composants
- **FastAPI (`src/main.py`)** : API REST avec endpoint `/ask` en streaming SSE et endpoint `/visualize` pour le contenu ChromaDB.
- **Ingestion (`src/ingestion.py`)** : Extraction de texte de PDFs (PyMuPDF), découpage en chunks (RecursiveCharacterTextSplitter) et génération d'embeddings vectoriels vers ChromaDB.
- **Visualiseur 3D (`src/chroma_viz.py`)** : Application Streamlit avec réduction t-SNE et graphiques 3D Plotly.

Pour les instructions d'installation et de configuration, consultez le [README principal à la racine du projet](../README.md).

