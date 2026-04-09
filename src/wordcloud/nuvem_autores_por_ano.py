import os
import pandas as pd
from google.cloud import bigquery
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

# 1. Configurações
PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'llm-studies')
TABLE_POSTS = "llm-studies.blog.posts_mar_2026"
TABLE_AUTHORS = "llm-studies.blog.posts_authors_mar_2026"
OUTPUT_DIR = "nuvens_temporal_autores"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def obter_frequencias_por_ano():
    client = bigquery.Client(project=PROJECT_ID)
    
    # Esta query já faz o "trabalho pesado" de contagem no BigQuery
    query = f"""
        SELECT 
            EXTRACT(YEAR FROM t1.post_date) as ano,
            author,
            COUNT(*) as frequencia
        FROM `{TABLE_POSTS}` AS t1
        INNER JOIN `{TABLE_AUTHORS}` AS t2 ON t1.post_id = t2.post_id,
        UNNEST(t2.post_authors) AS author
        WHERE author != 'Luis Quissak'
        GROUP BY ano, author
        ORDER BY ano, frequencia DESC
    """
    print("--- Extraindo frequências de autores por ano do BigQuery ---")
    return client.query(query).to_dataframe()

def gerar_nuvens_temporais():
    df = obter_frequencias_por_ano()
    
    if df.empty:
        print("Nenhum dado encontrado. O pipeline de extração já terminou?")
        return

    # Agrupamos por ano para gerar uma imagem por grupo
    anos = df['ano'].unique()

    for ano in anos:
        print(f"Processando ano: {ano}...")
        
        # Filtra os dados do ano atual e cria um dicionário {Nome: Frequência}
        df_ano = df[df['ano'] == ano]
        frequencias = dict(zip(df_ano['author'], df_ano['frequencia']))

        # Configuração da Nuvem (Ajustada para nomes)
        wc = WordCloud(
            width=1200, height=800,
            background_color='black', # Fundo preto dá um ar mais "galeria"
            colormap='cool',          # Tons de azul/ciano para um look moderno
            max_words=50,
            prefer_horizontal=0.7     # Deixa a maioria dos nomes na horizontal
        ).generate_from_frequencies(frequencias)

        # Renderização
        plt.figure(figsize=(15, 10))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Principais Influências - {int(ano)}", fontsize=40, color='white', pad=20)
        plt.gcf().set_facecolor('black') # Garante que a borda externa seja preta

        file_path = os.path.join(OUTPUT_DIR, f"autores_{int(ano)}.png")
        plt.savefig(file_path, bbox_inches='tight', facecolor='black')
        plt.close()

    print(f"\nFeito! As nuvens temporais estão em '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    gerar_nuvens_temporais()