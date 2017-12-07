import sqlite3 as lite
import sys

conn = lite.connect('blog_posts.db')


def create_table():
    with conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE posts (date TEXT, title TEXT PRIMARY KEY, content TEXT);")
        conn.commit()


def insert_post(date, title, filename):
    with conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts VALUES('{0}','{1}', '{2}')".format(date, title, filename))
        conn.commit()


def run_select_title_query(title):
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM posts WHERE title=?", (title,))
        content = cursor.fetchall()
        content = str(content).strip("[('',)]")
        print(content)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "create":
            create_table()
    # insert_post("July 29th 2017", "Hello World, Version 2", "blog_posts/hello_world.html")
    # insert_post("August 9th 2017", "Google Analytics for your website", "blog_posts/google_analytics.html")
    #insert_post("August 15th 2017", "Create a website tour using bootstrap-tour", "blog_posts/bootstrap_tour.html")
    # insert_post("August 23rd 2017", "Vivegam movie review", "blog_posts/vivegam_movie_review.html")
    insert_post("September 20th 2017", "Hosting Flask website on Digital Ocean", "blog_posts/flask_on_digital_ocean.html")
    run_select_title_query("Hello World")
    conn.close()