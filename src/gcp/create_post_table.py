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
    bigquery.SchemaField("post_labels", "STRING", mode="REPEATED"),
]

# 1. Cleaner deletion
client.delete_table(table_id, not_found_ok=True)
print(f"Deleted table {table_id} (if it existed).")

# 2. Add partitioning and clustering
table = bigquery.Table(table_id, schema=schema)

table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="post_date",  # Partitions the data by day based on post_date
)

table.clustering_fields = ["blog_id"] # Keeps data for the same blog physically close

table = client.create_table(table)
print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")