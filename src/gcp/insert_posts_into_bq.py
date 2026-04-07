import os
from dotenv import load_dotenv
import sys
from datetime import datetime
from google.cloud import bigquery
from googleapiclient import sample_tools
import html2text
import requests
import json


load_dotenv()
BLOG_ID = os.getenv('BLOG_ID')
KEY = os.getenv('KEY')
print("BLOG_ID", BLOG_ID)
REPLY_URL = "https://www.googleapis.com/blogger/v3/blogs/" + \
    BLOG_ID+"/posts/POST_ID/comments?key="+KEY
date_format = '%d/%m/%Y'

table_id = "llm-studies.blog.posts_mar_2026"
client = bigquery.Client()
log_date = datetime.now()



def get_post_date(post):
    # This handles almost any ISO 8601 string Blogger throws at it
    dt = datetime.fromisoformat(post["published"].replace('Z', '+00:00'))
    return dt.date().strftime('%Y-%m-%d')


def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv,
        "blogger",
        "v3",
        __doc__,
        __file__,
        scope="https://www.googleapis.com/auth/blogger",
    )

    blogs_list = service.blogs().listByUser(userId="self").execute()
    all_rows = []

    for blog in blogs_list.get("items", []):
        print("The posts for %s:" % blog["name"])
        blog_id = blog["id"]
        request = service.posts().list(blogId=blog_id)

        while request is not None:
            posts_doc = request.execute()            
            for post in posts_doc["items"]:

                content_text = html2text.html2text(post["content"])

                try:
                    comments_resp = service.comments().list(blogId=blog_id, postId=requests.post["id"]).execute()
                    comments_list = [c['content'] for c in comments_resp.get('items', [])]
                    comment_text = "\nComentários: " + "\n".join(comments_list) if comments_list else ""
                except:
                    comment_text = ""
                    comments_list = []

                row = {
                    "blog_id": int(blog_id),
                    "post_id": int(post["id"]),
                    "log_date": datetime.now().isoformat(),
                    "post_date": get_post_date(post),
                    "post_url": post["url"],
                    "post_title": post["title"],
                    "post_content_html": post["content"],
                    "post_content": content_text + comment_text,
                    "post_replies": len(comments_list),
                    "post_labels": post.get("labels", [])
                }
                all_rows.append(row)
                print(f"Prepared: {post['title']}")
            request = service.posts().list_next(request, posts_doc)

    # Insert everything at once (much faster!)


    if all_rows:

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


        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition="WRITE_APPEND", # Or "WRITE_TRUNCATE" to refresh the table
        )

        try:
            load_job = client.load_table_from_json(
                all_rows, 
                table_id, 
                job_config=job_config
            )
            
            load_job.result()  # Waits for the job to complete
            print(f"Successfully loaded {len(all_rows)} rows into {table_id}.")

        except Exception as e:
            print(f"Load job failed: {e}")

        return len(all_rows)



if __name__ == "__main__":
    total = main(sys.argv)
    print("Inseridos: %s" % total)