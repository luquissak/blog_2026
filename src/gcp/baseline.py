from google.cloud import bigquery

def create_baseline(client, task, prompt, model_name, temp):
    # 1. Busca o próximo ID de forma mais limpa
    # COALESCE garante que se a tabela estiver vazia, retorne 0
    id_query = "SELECT COALESCE(MAX(baseline_id), 0) + 1 as next_id FROM `llm-studies.blog.model_baseline_2026`"
    results = client.query_and_wait(id_query)
    baseline_id = next(results).next_id

    # 2. Prepara a inserção usando Parâmetros (Query Parameters)
    # Isso protege contra aspas e caracteres especiais no prompt
    insert_query = """
    INSERT INTO `llm-studies.blog.model_baseline_2026` 
    (baseline_id, task, log_date, prompt, model, temperature)
    VALUES (@baseline_id, @task, CURRENT_DATETIME(), @prompt, @model, @temp)
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("baseline_id", "INT64", baseline_id),
            bigquery.ScalarQueryParameter("task", "STRING", task),
            bigquery.ScalarQueryParameter("prompt", "STRING", prompt),
            bigquery.ScalarQueryParameter("model", "STRING", model_name),
            bigquery.ScalarQueryParameter("temp", "FLOAT64", temp),
        ]
    )

    client.query_and_wait(insert_query, job_config=job_config)
    print(f"--- Baseline #{baseline_id} registrado com sucesso ({model_name}) ---")
    return baseline_id