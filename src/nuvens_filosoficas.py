import os
import pandas as pd
from google.cloud import bigquery
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

# 1. Configurações e Caminhos
PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'llm-studies')
TABLE_ID = "llm-studies.blog.posts_mar_2026"
CACHE_FILE = "blog_posts_cache.csv" # Arquivo local para testes
OUTPUT_DIR = "nuvens_filosoficas"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Stopwords (Mantive sua lista atualizada)
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
    # Verifica se já temos o arquivo local
    if os.path.exists(CACHE_FILE):
        print(f"--- Carregando dados do CACHE LOCAL ({CACHE_FILE}) ---")
        return pd.read_csv(CACHE_FILE)
    
    # Se não existir, busca no BigQuery
    print("--- Buscando dados no BigQuery (isso pode demorar um pouco) ---")
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT 
            EXTRACT(YEAR FROM post_date) as ano, 
            STRING_AGG(post_content, ' ') as texto_completo
        FROM `{TABLE_ID}`
        GROUP BY ano
        ORDER BY ano
    """
    try:
        df = client.query(query).to_dataframe()
        # Salva para a próxima vez
        df.to_csv(CACHE_FILE, index=False)
        print(f"--- Dados salvos localmente em {CACHE_FILE} ---")
        return df
    except Exception as e:
        print(f"Erro ao acessar BigQuery: {e}")
        return None

def gerar_nuvens():
    df = obter_dados()
    if df is None: return

    for index, row in df.iterrows():
        ano = row['ano']
        texto = str(row['texto_completo']) # Garante que é string
        
        print(f"Gerando nuvem para o ano: {ano}...")
        
        # Configuração da Nuvem
        wc = WordCloud(
            width=1200, height=800, 
            background_color='white',
            stopwords=final_stopwords,
            colormap='viridis',
            max_words=100
        ).generate(texto)

        # Plot e Save
        plt.figure(figsize=(15, 10))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Reflexões Filosóficas - {ano}", fontsize=30)
        
        file_path = os.path.join(OUTPUT_DIR, f"nuvem_{ano}.png")
        plt.savefig(file_path, bbox_inches='tight')
        plt.close()

    print(f"\nSucesso! Nuvens salvas em '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    gerar_nuvens()