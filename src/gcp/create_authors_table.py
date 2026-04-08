from google.cloud import bigquery
client = bigquery.Client()
table_id = "llm-studies.blog.posts_authors_mar_2026"
schema = [
    bigquery.SchemaField("blog_id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("post_id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("baseline_id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("log_date", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField(
        "post_authors",
        "STRING",
        mode="REPEATED"),
    bigquery.SchemaField("model_version", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("total_token_count", "INT64", mode="REQUIRED"),
    bigquery.SchemaField(
        "safety_ratings",
        "RECORD",
        mode="REPEATED",
        fields=[
            bigquery.SchemaField("category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("probability", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("blocked", "BOOLEAN"),
            bigquery.SchemaField("probability_score", "FLOAT64", mode="REQUIRED"),
            bigquery.SchemaField("severity", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("severity_score", "FLOAT64", mode="REQUIRED"),
        ],
    ),
    bigquery.SchemaField("finish_reason", "STRING", mode="REQUIRED"),
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