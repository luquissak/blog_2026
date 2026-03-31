from google.cloud import bigquery
client = bigquery.Client()
table_id = "llm-studies.blog.posts_mar_2026"
schema = [
    bigquery.SchemaField("blog_id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("post_id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("log_date", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("post_date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("post_url", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("post_title", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("post_content_html", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("post_content", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("post_replies", "INT64", mode="REQUIRED"),
    bigquery.SchemaField(
        "post_labels",
        "STRING",
        mode="REPEATED"),
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