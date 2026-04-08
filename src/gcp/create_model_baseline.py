from google.cloud import bigquery
client = bigquery.Client()
table_id = "llm-studies.blog.model_baseline_2026"
schema = [
    bigquery.SchemaField("baseline_id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("task", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("log_date", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("prompt", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("model", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("temperature", "FLOAT64", mode="REQUIRED"),
]

try:
    table = bigquery.Table(table_id, schema=schema)
    table = client.delete_table(table)
    print(
        "Deleted table {}.{}.{}".format(
            table.project, table.dataset_id, table.table_id)
    )
except:
    pass

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)
print(
    "Created table {}.{}.{}".format(
        table.project, table.dataset_id, table.table_id)
)