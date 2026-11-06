import streamlit as st
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
import plotly.express as px
import os, chromadb
from dotenv import load_dotenv

load_dotenv() # Charge les variables du .env
st.set_page_config(page_title="Chroma Projector 3D", layout="wide")
st.title("🌌 Visualiseur d'Espace Vectoriel")

# Récupération des variables avec des valeurs par défaut
#host = os.getenv("CHROMA_HOST")
#port = int(os.getenv("CHROMA_PORT"))
#client = chromadb.HttpClient(host=host, port=port)
db_dir = os.getenv("CHROMA_DB_DIR", "../chroma_db")
client = chromadb.PersistentClient(path=db_dir)

try:
    # On force la récupération de TOUTES les collections
    collections = client.list_collections()
    
    if not collections:
        st.error("Chroma répond mais aucune collection n'est listée. Vérifie le nom de ta collection dans ton code source.")
    else:
        selected_name = st.sidebar.selectbox("Sélectionnez votre collection", [c.name for c in collections])
        col = client.get_collection(selected_name)
        
        # CRUCIAL : On demande explicitement les embeddings et les documents
        data = col.get(include=['embeddings', 'documents', 'metadatas'])
        
        nb_items = len(data['ids'])
        st.sidebar.write(f"Nombre d'éléments trouvés : {nb_items}")

        if nb_items > 0:
            if data['embeddings'] is not None:
                embeddings = np.array(data['embeddings'])
                
                # t-SNE pour le rendu style Tensorflow Projector
                # On ajuste la perplexité car tu as 106 segments
                perplex = min(30, nb_items - 1)
                tsne = TSNE(n_components=3, perplexity=perplex, init='pca', random_state=42)
                projections = tsne.fit_transform(embeddings)

                df = pd.DataFrame({
                    "x": projections[:, 0],
                    "y": projections[:, 1],
                    "z": projections[:, 2],
                    "document": [d[:100] + "..." if d else "Sans texte" for d in data['documents']],
                    "id": data['ids']
                })

                fig = px.scatter_3d(
                    df, 
                    x='x', y='y', z='z',
                    hover_name='id',             # L'ID s'affiche en gras en haut
                    hover_data={'x':False, 'y':False, 'z':False, 'document':True}, # On cache les coordonnées brutes
                    color='x',                   # Gradient basé sur la position
                    color_continuous_scale=px.colors.sequential.Viridis, 
                    opacity=0.7,
                    template="seaborn"
                )

                # Personnalisation avancée des marqueurs et de la scène
                fig.update_traces(
                    marker=dict(
                        size=5,                  # Points légèrement plus gros
                        line=dict(width=0.5, color='DarkSlateGrey'), # Bordure fine pour le relief
                    ),
                    selector=dict(mode='markers')
                )

                fig.update_layout(
                    scene=dict(
                        xaxis=dict(showbackground=False, showgrid=True, gridcolor="rgba(255, 255, 255, 0.1)"),
                        yaxis=dict(showbackground=False, showgrid=True, gridcolor="rgba(255, 255, 255, 0.1)"),
                        zaxis=dict(showbackground=False, showgrid=True, gridcolor="rgba(255, 255, 255, 0.1)"),
                        bgcolor="black",         # Fond totalement noir pour le contraste
                    ),
                    margin=dict(l=0, r=0, b=0, t=0),
                    coloraxis_showscale=False,    # On cache la barre de couleur pour un look plus clean
                    hoverlabel=dict(
                        bgcolor="rgba(33, 33, 33, 0.9)", 
                        font_size=13, 
                        font_family="Inter, sans-serif"
                    )
                )

                st.plotly_chart(fig, use_container_width=True)
                
                st.write("### Liste des segments")
                st.dataframe(df[['id', 'document']])
            else:
                st.warning("Les IDs sont là, mais les vecteurs (embeddings) sont vides ou non récupérés.")
        else:
            st.info("La collection est sélectionnée mais elle ne contient aucun ID.")

except Exception as e:
    st.error(f"Erreur de connexion : {e}")