import os
import pandas as pd
from google.cloud import bigquery
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

# 1. Configurações Iniciais
client = bigquery.Client()
table_id = "llm-studies.blog.posts_mar_2026"
output_dir = "nuvens_filosoficas"
os.makedirs(output_dir, exist_ok=True)

# 2. Stopwords (Palavras que a IA deve ignorar)
# Adicionei termos comuns em português e ruídos do html2text
stop_words_pt = [
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", 
    "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi", 
    "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito", 
    "nos", "já", "está", "eu", "também", "pelo", "pela", "até", "isso", "ela", 
    "entre", "era", "depois", "sem", "mesmo", "aos", "ter", "seus", "quem", 
    "nas", "me", "esse", "eles", "estão", "você", "tinha", "foram", "essa", 
    "num", "nem", "suas", "meu", "minha", "numa", "pelos", "elas", "havia", 
    "seja", "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", 
    "pelas", "este", "fosse", "uma", "tal", "post", "comentários", "http", "https", "são", "há", "sobre"
]
# Unindo com as default do wordcloud
final_stopwords = set(list(STOPWORDS) + stop_words_pt)

def gerar_nuvem_por_ano():
    # 3. Query para buscar o conteúdo
    query = f"""
        SELECT 
            EXTRACT(YEAR FROM post_date) as ano, 
            STRING_AGG(post_content, ' ') as texto_completo
        FROM `{table_id}`
        GROUP BY ano
        ORDER BY ano
    """
    
    print("Buscando dados no BigQuery...")
    df = client.query(query).to_dataframe()

    for index, row in df.iterrows():
        ano = row['ano']
        texto = row['texto_completo']
        
        print(f"Gerando nuvem para o ano: {ano}...")
        
        # 4. Configuração da Nuvem
        wc = WordCloud(
            width=1200, 
            height=800, 
            background_color='white',
            stopwords=final_stopwords,
            colormap='viridis', # Estilo de cores 'bonitão'
            max_words=100
        ).generate(texto)

        # 5. Salvar a Imagem
        plt.figure(figsize=(15, 10))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Reflexões Filosóficas - {ano}", fontsize=30)
        
        file_path = os.path.join(output_dir, f"nuvem_{ano}.png")
        plt.savefig(file_path, bbox_inches='tight')
        plt.close()

    print(f"\nSucesso! As nuvens foram salvas na pasta '{output_dir}'.")

if __name__ == "__main__":
    gerar_nuvem_por_ano()