# 📱 EMSI RAG Assistant & Auth — Flutter & FastAPI

[![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B?logo=flutter&logoColor=white)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Supabase-Auth-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com)
[![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-FF6F61)](https://www.trychroma.com)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000?logo=ollama&logoColor=white)](https://ollama.ai)

Application mobile intelligente développée avec **Flutter**, couplée à un backend **FastAPI** implémentant une architecture **RAG (Retrieval-Augmented Generation)** locale et sécurisée. L'application intègre l'authentification gérée par **Supabase**, l'interrogation en streaming d'un LLM local (Ollama) sur la base de connaissances documentaire de l'**EMSI**, ainsi que la visualisation 2D/3D de la base vectorielle **ChromaDB**.

---

## 📑 Table des Matières

- [Aperçu de l'Architecture](#-aperçu-de-larchitecture)
- [Fonctionnalités Principales](#-fonctionnalités-principales)
- [Structure du Projet](#-structure-du-projet)
- [Stack Technique](#-stack-technique)
- [Prérequis](#-prérequis)
- [Installation & Démarrage](#-installation--démarrage)
  - [1. Configuration d'Ollama](#1-configuration-dollama)
  - [2. Backend RAG (FastAPI + ChromaDB)](#2-backend-rag-fastapi--chromadb)
  - [3. Frontend Mobile (Flutter)](#3-frontend-mobile-flutter)
  - [4. Visualiseur 3D (Streamlit - Optionnel)](#4-visualiseur-3d-streamlit---optionnel)
- [Variables d'Environnement](#-variables-denvironnement)
- [Endpoints API](#-endpoints-api)

---

## 🏛 Aperçu de l'Architecture

```mermaid
flowchart TD
    subgraph Client["📱 Mobile Client (Flutter)"]
        UI[Interface Flutter Material 3]
        AuthGate[AuthGate / Session Manager]
        ChatScreen[Écran Chat RAG avec Streaming SSE]
        VizScreen[Écran In-App WebView ChromaDB]
    end

    subgraph CloudAuth["☁️ Cloud Backend"]
        Supa[(Supabase Auth Service)]
    end

    subgraph Backend["⚙️ Backend RAG (FastAPI)"]
        API[FastAPI Server :8000]
        VectorStore[(ChromaDB Vector Store)]
        StreamlitApp[Streamlit 3D Projector]
    end

    subgraph LocalAI["🦙 Moteur Local (Ollama)"]
        EmbedModel["Embeddings : nomic-embed-text"]
        LLMModel["LLM : qwen3.5:4b"]
    end

    UI --> AuthGate
    AuthGate <-->|Auth Tokens / Session| Supa
    ChatScreen -->|POST /ask (Streaming SSE)| API
    VizScreen -->|GET /visualize (HTML)| API
    VizScreen -.->|Visualisation 3D t-SNE| StreamlitApp

    API -->|Similarity Search k=NN| VectorStore
    API <-->|Embeddings & Completion| LocalAI
```

---

## ✨ Fonctionnalités Principales

- **🔐 Authentification Supabase complète** :
  - Inscription, connexion, réinitialisation de mot de passe et déconnexion.
  - Persistance de session sécurisée et écoute réactive du flux d'authentification (`AuthGate`).
- **🤖 Assistant IA conversationnel RAG (EMSI)** :
  - Indexation automatique des brochures et programmes académiques de l'EMSI.
  - Recherche vectorielle de similarité sémantique via **ChromaDB**.
  - Génération de réponses contextuelles strictly grounded sans hallucinations.
  - Streaming temps réel token par token (**Server-Sent Events - SSE**).
- **📊 Visualisation de la base vectorielle** :
  - Vue tabulaire embarquée directement dans l'application mobile via **WebView**.
  - Visualiseur interactif 3D propulsé par **Streamlit**, **t-SNE** et **Plotly** pour explorer les embeddings vectoriels dans l'espace latent.
- **🎨 UI/UX Moderne** : Interface soignée conforme à **Material Design 3**, Drawer ergonomique, gestion des statuts de chargement et retours utilisateur optimisés.

---

## 📂 Structure du Projet

```text
aitlahcen_app/
├── backend_rag/                  # Backend FastAPI & Pipeline RAG
│   ├── data/                     # Documents sources (Brochure-EMSI.pdf, Option-IIR.pdf)
│   ├── src/
│   │   ├── main.py               # Serveur FastAPI (endpoints /ask et /visualize)
│   │   ├── ingestion.py          # Script d'ingestion et découpage de documents (chunking)
│   │   └── chroma_viz.py         # Visualiseur 3D interactif Streamlit & Plotly
│   ├── utils/
│   │   ├── check_db.py           # Vérification de l'intégrité de ChromaDB
│   │   └── inspect_db.py         # Inspection détaillée des segments
│   ├── .env.example              # Modèle des variables d'environnement backend
│   ├── pyproject.toml            # Dépendances Python (uv / pip)
│   └── requirements.txt          # Dépendances pip
│
├── chroma_db/                    # Base de données vectorielle persistante Chroma
│
├── frontend/                     # Application mobile Flutter
│   ├── lib/
│   │   ├── screens/
│   │   │   ├── login_page.dart              # Écran de connexion
│   │   │   ├── register_page.dart           # Écran d'inscription
│   │   │   ├── home_page.dart               # Tableau de bord & navigation
│   │   │   ├── rag_chat_screen.dart         # Chatbot RAG avec streaming SSE
│   │   │   └── chroma_visualizer_screen.dart# Visualiseur webview intégré
│   │   ├── supabase_config.dart # Configuration du client Supabase
│   │   └── main.dart            # Point d'entrée de l'application
│   ├── assets/images/           # Ressources graphiques
│   ├── .env.example             # Modèle des variables d'environnement frontend
│   └── pubspec.yaml             # Dépendances Flutter
│
└── README.md                     # Documentation globale
```

---

## 🛠 Stack Technique

| Domaine | Technologies |
| :--- | :--- |
| **Mobile (Frontend)** | Flutter, Dart, Supabase Flutter SDK, Flutter Dotenv, InAppWebView, HTTP Streaming |
| **Backend API** | Python, FastAPI, Uvicorn, Pydantic, AsyncIO |
| **Pipeline RAG** | LangChain (`langchain-ollama`, `langchain-community`, `PyMuPDF`) |
| **Base Vectorielle** | ChromaDB |
| **Moteur IA Local** | Ollama (`qwen3.5:4b` pour le chat, `nomic-embed-text` pour les embeddings) |
| **Data Viz** | Streamlit, Scikit-learn (t-SNE), Plotly Express |
| **Authentification** | Supabase Auth (PostgreSQL / GoTrue) |

---

## ⚙️ Prérequis

- [Flutter SDK](https://docs.flutter.dev/get-started/install) (version `>= 3.3.0`)
- [Python](https://www.python.org/) (version `>= 3.10`)
- [Ollama](https://ollama.ai/) installé et exécuté localement
- Un projet actif sur [Supabase](https://supabase.com/)

---

## 🚀 Installation & Démarrage

### 1. Configuration d'Ollama

Téléchargez les modèles requis en ligne de commande :

```bash
# Modèle d'embeddings
ollama pull nomic-embed-text

# Modèle de langage (LLM)
ollama pull qwen3.5:4b
```

Assurez-vous que le service Ollama est actif sur `http://localhost:11434`.

---

### 2. Backend RAG (FastAPI + ChromaDB)

1. **Accédez au répertoire backend :**
   ```bash
   cd backend_rag
   ```

2. **Créez et activez un environnement virtuel :**
   ```bash
   python -m venv .venv
   # Windows :
   .venv\Scripts\activate
   # Linux / macOS :
   source .venv/bin/activate
   ```

3. **Installez les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurez les variables d'environnement :**
   Créez un fichier `.env` dans `backend_rag/` (voir section [Variables d'Environnement](#-variables-denvironnement)).

5. **Indexez les documents dans ChromaDB :**
   Placez vos PDFs dans `backend_rag/data/` puis exécutez le script d'ingestion :
   ```bash
   python src/ingestion.py
   ```

6. **Démarrez le serveur FastAPI :**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   L'API sera disponible sur `http://localhost:8000` (Documentation Swagger accessible sur `/docs`).

---

### 3. Frontend Mobile (Flutter)

1. **Accédez au répertoire frontend :**
   ```bash
   cd ../frontend
   ```

2. **Installez les packages Flutter :**
   ```bash
   flutter pub get
   ```

3. **Configurez le fichier d'environnement :**
   Créez un fichier `.env` à la racine de `frontend/` :
   ```env
   # Pour un émulateur Android utilisez http://10.0.2.2:8000
   # Pour un appareil physique utilisez l'adresse IP de votre machine (ex: http://192.168.1.X:8000)
   RAG_API_URL=http://10.0.2.2:8000

   # Identifiants Supabase
   SUPABASE_URL=https://votre-projet.supabase.co
   SUPABASE_PUBLISHABLE_KEY=votre_cle_publique_supabase
   ```

4. **Lancez l'application mobile :**
   ```bash
   flutter run
   ```

---

### 4. Visualiseur 3D (Streamlit - Optionnel)

Pour explorer l'espace latent vectoriel des chunks de documents en 3D :

```bash
cd backend_rag
streamlit run src/chroma_viz.py
```
L'interface interactive 3D s'ouvrira dans votre navigateur sur `http://localhost:8501`.

---

## 📡 Endpoints API

| Méthode | Route | Description | Format Retour |
| :--- | :--- | :--- | :--- |
| `POST` | `/ask` | Pose une question au RAG avec recherche vectorielle | `text/event-stream` (SSE) |
| `GET` | `/visualize` | Liste l'intégralité des segments et métadonnées indexés | `text/html` |
| `GET` | `/docs` | Documentation interactive OpenAPI / Swagger | `HTML / JSON` |

---

## 👤 Auteur

- **Achraf Ait Lahcen** — Élève Ingénieur en 5ème année à l'EMSI (5DSIG2)

