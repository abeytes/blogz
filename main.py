
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2
import cgi
autoescape = True
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader (template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:asdf@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blogz(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    qtitle = db.Column(db.String(100))
    qentry = db.Column(db.String(1000))
    Username = db.Column(db.String(30))


    def __init__(self, qtitle , qentry, username, password ):
        self.qtitle = qtitle
        self.qentry = qentry
        self.username = username
        self.password = password
    

endpoints_without_login = ['login', 'register', 'index', 'main_page']

@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if (not username) or (username.strip() == ""):
            flash("Please enter a username." , 'danger')
            return redirect ('/register')
        if password != verify:
            flash('passwords do not match', 'danger')
            return redirect('/register')

        if len(username)<3 or len(username)>20:
            flash("Valid usernames must have between 3 and 20 characters", 'danger')
            return redirect('/register')

        if len(password)<3 or len(password)>20:
            flash('Valid passwords must have between 3 and 20 characters', 'danger') 
            return redirect('/register')      

        existing_user = Blogz.query.filter_by(username=username).first()
        if not existing_user:
            new_user = Blogz(username, password)
            db.session.add(new_user)
            db.session.commit()
            user = new_user
            session['user'] = user.username
            
            return redirect('/blog')
        else:
            flash('That username is already in use', 'danger')
            return redirect('/register')
    else:
        return render_template('register.html')     

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = Blogz.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user'] = user.username
                flash('welcome back, '+ user.username, 'success')
                return redirect("/blog")
        flash('bad username or password', 'danger')
        return redirect("/login") 

    blogtask = Blogz.query.all()
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
            blogs = Blogz(title, entry)
            db.session.add(blogs)
            db.session.commit()
            return redirect("/blog?id="+ str(blogs.id) )


    return render_template("addblog.html", title_error=title_error, entry_error=entry_error)


if __name__ == '__main__':
    app.run()
