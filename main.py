from flask import Flask, request, redirect, render_template 
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2
import cgi

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader (template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buildablog:asdf@localhost:3306/buildablog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class buildablog (db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    completer = db.Column(db.Boolean)

    def __ini__(self, name):
        self.name = name
        self.compleated = False

blog = []

@app.route("/")
def index():
    template = jinja_env.get_template("Home.html")
    return template.render()

blog = []

@app.route("/addblog", methods= ['POST','GET'])
def add_blog():       
    
    if request.methods == 'POST':
         title = request.form["blogtitlle"]
         entry = request.form["blogentry"]
         title_error = ''
         entry_error = ''
         if len(title) >= 100 and len(title)<0:
            title_error = "text range must be (1-150)"
         if len(entry) >= 1000 and len(entry) < 0:
            entry_error = "text range must be (1-1000)" 
         else:
            blog.append(title)
            blog.append(entry)
            
    template = jinja_env.get_template("Home.html")
    return template.render(blog=blog)

if __name__ == '__main__':
    app.run()