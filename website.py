from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3 as lite
import requests

import os
app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('index.html')


@app.route("/education")
def show_education():
    return render_template('education.html')


@app.route("/experience")
def show_experience():
    return render_template('experience.html')


@app.route("/films")
def show_films():
    return render_template('films.html')


@app.route("/photography")
def show_photography():
    return render_template('photography.html')


@app.route('/projects')
def show_projects():
    return render_template('projects.html')


@app.route("/skills")
def show_skills():
    return render_template('skills.html')


@app.route('/visual_resume')
def show_visual_resume():
    return render_template('visual_resume.html')


@app.route('/favorite_quotes')
def show_favorite_quotes():
    favorite_quotes = {}
    favorite_quotes["Avvaiyar, an ancient tamil poetess"] = "Known is a drop, unknown is an ocean"
    favorite_quotes["Dr.A.P.J.Abdul Kalam"] = "Man needs his difficulties because they are necessary to enjoy success"
    favorite_quotes["Swami Vivekananda"] = "Arise! Awake! and stop not until the goal is reached"
    favorite_quotes["Sri Ramakrishna Paramahamse"] = "The tree laden with fruits always bends low. If you wish to be"  \
     "great, be lowly and meek"
    favorite_quotes["Mahatma Gandhi"] = "You must be the change you want to see in the world"
    favorite_quotes["Mother Teresa"] = "The biggest problem in the world today is not poverty or disease but the lack" \
    "of love and charity and the feeling of being unwanted"

    favorite_quotes["Albert Einstein"] = "You never fail until you stop trying"
    favorite_quotes["Walt Disney"] = "If you can dream it, you can do it"
    favorite_quotes["Charlie Chaplin"] = "My pain may be the reason for somebody's laugh, but my laugh must never be " \
    "the reason for somebody's pain"
    favorite_quotes["Bruce Lee"] = "Knowledge will give you power, but character will give you respect"
    favorite_quotes["Winston Churchill"] = "To improve is to change, to be perfect is to change often"
    favorite_quotes["Bill Gates"] = "Success is a lousy teacher, it seduces smart people into thinking they can't lose"
    return render_template('favorite_quotes.html', favorite_quotes=favorite_quotes)


@app.route('/pingMe')
def contact_me():
    return render_template('contact_me.html')


@app.route('/send_email', methods=['POST', 'GET'])
def send_email():

    fromaddr = request.form["email"]
    if 'GMAIL_ADDRESS' not in os.environ:
        os.environ["GMAIL_ADDRESS"] = "srikkanthswebsite@gmail.com"
    toaddr = os.environ["GMAIL_ADDRESS"]

    if 'GMAIL_PASSWORD' not in os.environ:
        path = "/Users/srikkanthgovindaraajan/PycharmProjects/flaskPersonalWebsite"
        with open(path + "/file.txt", 'r') as file:
            content = file.readline().replace("\n", "")
            os.environ["GMAIL_PASSWORD"] = content
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Email from {0} : Website".format(fromaddr)

    body = "From : {0} {1}".format(request.form["first"], request.form["last"])
    body += "\nEmail: {0}".format(request.form["email"])
    body += "\nMessage: {0}".format(request.form["message"])
    print(body)

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(toaddr, os.environ["GMAIL_PASSWORD"])
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return render_template('email_sent.html')


@app.route('/posts')
def blog_posts():
    conn = lite.connect('blog_posts.db')
    post_details = []
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title from posts")
        rows = cursor.fetchall()
        for detail in rows:
            detail = str(detail).strip("('',)")
            if detail.startswith("u'"):
                detail = detail.replace("u'","")
            print(detail)
            post_details.append(detail)
        print(post_details)
    return render_template('blog_posts.html', post_details=post_details)


@app.route('/show_post/<title>')
def show_post(title):
    conn = lite.connect('blog_posts.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content from posts where title=? ", (title,))
        content = cursor.fetchall()
        filename = str(content).strip("[('',)]")
        filename = filename.replace("u'", "")

        cursor.execute("SELECT date from posts where title=? ", (title,))
        result = cursor.fetchall()
        date = str(result).strip("[('',)]")
        print(date)

        print(filename)

    return render_template(filename, date=date, title=title)


@app.route('/show_gists')
def show_public_gists():
    gists = requests.get(url="https://api.github.com/users/govindsh/gists").json()
    print(gists)
    return render_template('show_public_gists.html', gists=gists)


@app.route('/api')
def show_api():
    return render_template('show_api.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host="0", threaded=True)
    app.secret_key = "my_own_website"