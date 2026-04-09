import sys
from dotenv import load_dotenv
from google.cloud import bigquery
import time
import json
import src.prompts as prompts
import src.model_config as model_config
import src.gcp.baseline as baseline
import src.gcp.bq_inserts as bq_inserts
import src.gcp.bq_queries as bq_queries

client = bigquery.Client()
TASK = "ner"
MODEL_NAME = "gemini-2.5-flash"
TEMP = 0



def main(argv):
    print("starting with google-genai SDK...")
    
    # Inicializa o cliente novo
    client_genai = model_config.get_client()
    
    # Registra Baseline
    baselineId = baseline.create_baseline(client, # BQ Client
        TASK, prompts.authors_prompt, MODEL_NAME, TEMP)
    
    rows = client.query_and_wait(bq_queries.query_new_posts_for_authors)
    print(f"rows to be checked... {rows.total_rows}")
    
    for row in rows:
        print(f"post={row['post_title']}")
        
        # Chama o modelo usando o cliente novo
        modelResp = model_config.call_model(
            client_genai, 
            MODEL_NAME, 
            TEMP, 
            prompts.authors_prompt, 
            row["post_content"]
        )
        
        # Parse e Insert permanecem quase idênticos
        try:
            modelResp_json = json.loads(modelResp.text)
            authors_l = [a["author"] for a in modelResp_json.get("authors", [])]
        except:
            authors_l = ["ERRO_PARSING"]
            
        print(f"authors={authors_l}")
        
        bq_inserts.insert_authors(
            client, # BQ Client
            row["blog_id"], row["post_id"], baselineId, authors_l,
            modelResp.modelVersion, modelResp.totalTokenCount, 
            modelResp.safetyRatings, modelResp.finish_reason
        )
        
        time.sleep(10) # Increased delay to avoid quota exhaustion

if __name__ == "__main__":
    main(sys.argv)