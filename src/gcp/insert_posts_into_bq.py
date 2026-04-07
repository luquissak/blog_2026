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

table_id = "llm-studies.blog.posts_dez_2024"
client = bigquery.Client()
log_date = datetime.now()


def get_comments(postId):
    response = requests.request("GET", REPLY_URL.replace(
        "POST_ID", postId), headers={}, data={})
    json_obj = json.loads(response.text)
    comments = "Comentários: "
    i = 0
    try:
        for comment in json_obj['items']:
            comments = comments + comment['content'] + "\n"
            i = i+1
    except:
        return "", 0    
    return comments, i


def get_post_date(post):
    try:
        return datetime.strptime(
            post["published"], '%Y-%m-%dT%H:%M:%S-03:00').date().strftime('%Y-%m-%d')
    except:
        return datetime.strptime(
            post["published"], '%Y-%m-%dT%H:%M:%S-02:00').date().strftime('%Y-%m-%d')


def insert_post(blogId, post):
    blog_id = blogId
    post_id = post["id"]
    post_date = get_post_date(post)
    post_url = post["url"]
    post_title = post["title"]
    post_content_html = post["content"]
    post_content = html2text.html2text(post["content"])
    post_replies, post_replies_total = get_comments(post_id)
    post_content = post_content + " " + post_replies
    try:
        post_labels = post["labels"]
    except:
        post_labels = []
    rows_to_insert = [
        {"blog_id": blog_id, "post_id": post_id, "log_date": str(log_date), "post_date": str(post_date), "post_url": post_url,
            "post_title": post_title, "post_content_html": post_content_html, "post_content": post_content, "post_replies": int(post_replies_total),
            "post_labels": post_labels}
    ]
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors != []:
        print("Encountered errors while inserting rows: {}".format(errors))
        exit()
    else:
        return 1


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
    print("logged!")

    users = service.users()
    thisuser = users.get(userId="self").execute()
    print("This user's display name is: %s" % thisuser["displayName"])
    blogs = service.blogs()
    thisusersblogs = blogs.listByUser(userId="self").execute()
    for blog in thisusersblogs["items"]:
        print("The blog named '%s' is at: %s" % (blog["name"], blog["url"]))

    posts = service.posts()
    total = 0
    for blog in thisusersblogs["items"]:
        print("The posts for %s:" % blog["name"])
        blogId = blog["id"]
        request = posts.list(blogId=blogId)
        while request != None:
            posts_doc = request.execute()
            if "items" in posts_doc and not (posts_doc["items"] is None):
                for post in posts_doc["items"]:
                    inserted = insert_post(blogId, post)
                    total = total + inserted
                    print("%s (%s)... %s" % (post["title"], get_post_date(post), total))
                    exit(0)
            request = posts.list_next(request, posts_doc)
    return total



if __name__ == "__main__":
    total = main(sys.argv)
    print("Inseridos: %s" % total)