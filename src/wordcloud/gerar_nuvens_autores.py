import os
import pandas as pd
from google.cloud import bigquery
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

# 1. Configurações e Caminhos
PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'llm-studies')
TABLE_POSTS = "llm-studies.blog.posts_mar_2026"
TABLE_AUTHORS = "llm-studies.blog.posts_authors_mar_2026"
CACHE_FILE = "blog_authors_cache.csv" 
OUTPUT_DIR = "nuvens_por_autor"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Stopwords (Lista expandida para limpar melhor os termos técnicos)
stop_words_pt = [
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", 
    "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi", 
    "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito", 
    "nos", "já", "está", "eu", "também", "pelo", "pela", "até", "isso", "ela", 
    "entre", "era", "depois", "sem", "mesmo", "aos", "ter", "seus", "quem", 
    "nas", "me", "esse", "eles", "estão", "você", "tinha", "foram", "essa", 
    "num", "nem", "suas", "meu", "minha", "numa", "pelos", "elas", "havia", 
    "seja", "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", 
    "pelas", "este", "fosse", "uma", "tal", "post", "comentários", "http", "https", "são", "há", "sobre", "porque"
]
final_stopwords = set(list(STOPWORDS) + stop_words_pt)

def obter_dados():
    if os.path.exists(CACHE_FILE):
        print(f"--- Carregando cache de autores ({CACHE_FILE}) ---")
        return pd.read_csv(CACHE_FILE)
    
    print("--- Cruzando posts e autores no BigQuery ---")
    client = bigquery.Client(project=PROJECT_ID)
    
    # A Query Mágica: Une o conteúdo do post com a lista de autores extraída pelo Gemini
    query = f"""
        SELECT 
            author, 
            STRING_AGG(t1.post_content, ' ') as texto_completo
        FROM `{TABLE_POSTS}` AS t1
        INNER JOIN `{TABLE_AUTHORS}` AS t2 ON t1.post_id = t2.post_id,
        UNNEST(t2.post_authors) AS author
        WHERE author != 'Luis Quissak'
        GROUP BY author
        HAVING COUNT(*) > 1  -- Opcional: gera nuvens apenas para quem aparece mais de uma vez
    """
    try:
        df = client.query(query).to_dataframe()
        df.to_csv(CACHE_FILE, index=False)
        return df
    except Exception as e:
        print(f"Erro ao acessar BigQuery: {e}")
        return None

def gerar_nuvens():
    df = obter_dados()
    if df is None: return

    for index, row in df.iterrows():
        autor = row['author']
        texto = str(row['texto_completo'])
        
        # Limpeza rápida para remover o nome do próprio autor da nuvem (evita redundância)
        final_stopwords.update([autor.lower(), autor.split()[-1].lower()])

        print(f"Gerando nuvem para: {autor}...")
        
        wc = WordCloud(
            width=1200, height=800, 
            background_color='white',
            stopwords=final_stopwords,
            colormap='magma', # Tom mais acadêmico/escuro para autores
            max_words=80
        ).generate(texto)

        plt.figure(figsize=(15, 10))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Léxico Filosófico: {autor}", fontsize=30, pad=20)
        
        # Nome do arquivo seguro
        safe_name = autor.replace(" ", "_").replace(".", "").lower()
        file_path = os.path.join(OUTPUT_DIR, f"nuvem_{safe_name}.png")
        plt.savefig(file_path, bbox_inches='tight')
        plt.close()

    print(f"\nSucesso! As nuvens estão em '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    gerar_nuvens()