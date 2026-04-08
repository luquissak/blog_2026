query_new_posts_for_authors = """
    SELECT t1.blog_id, t1.post_id, t1.post_title, t1.post_content
    FROM `llm-studies.blog.posts_mar_2026` AS t1
    WHERE NOT EXISTS (
        SELECT 1 
        FROM `llm-studies.blog.posts_authors_mar_2026` AS t2 
        WHERE t1.post_id = t2.post_id
    )
    """