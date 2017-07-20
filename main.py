from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2
import cgi

autoescape = True
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader (template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blogtask(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    qtitle = db.Column(db.String(100))
    qentry = db.Column(db.String(1000))

    def __init__(self, qtitle , qentry):
        self.qtitle = qtitle
        self.qentry = qentry


@app.route('/blog')
def show_blog():

    blogtask = Blogtask.query.all()
    return render_template('Home.html', blogtask=blogtask)
@app.route("/", methods = ["GET","POST"])
def index():

    return redirect('/blog')

@app.route("/addblog", methods=['POST', 'GET'])
def add_blog():

    title_error = ''
    entry_error = ''
    title = ''
    entry = ''
    if request.method == 'POST':

        title = request.form["blogtitle"]
        if not title:
            title_error = "Please fill the title"
            if len(title) > 100:
                title_error = "text length range must be (1-100)"

            return render_template("addblog.html", title_error=title_error, entry_error=entry_error)

        entry = request.form["blogentry"]
        if not entry:
            entry_error = "Empty, text on top box"
            # return redirect("/a")
            if len(entry) > 1000:
                entry_error =  "text lenght range must be (1-1000)"
            return render_template("addblog.html", title_error=title_error, entry_error=entry_error)
        else:
            # return render_template("addblog.html")
            blogs = Blogtask(title, entry)
            db.session.add(blogs)
            db.session.commit()

            return redirect("/blog?id="+ str(blogs.id) )


    return render_template("addblog.html", title_error=title_error, entry_error=entry_error)


if __name__ == '__main__':
    app.run()
