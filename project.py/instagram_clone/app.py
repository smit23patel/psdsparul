from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user,login_required
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))


class Post(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    image = db.Column(db.String(100))

    caption = db.Column(db.String(200))

    user_id = db.Column(db.Integer)



@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route('/')
@login_required
def feed():

    posts = Post.query.all()

    return render_template('feed.html',posts=posts)



@app.route('/login',methods=['GET','POST'])
def login():

    if request.method=="POST":

        username=request.form['username']

        password=request.form['password']

        user=User.query.filter_by(username=username,password=password).first()

        if user:

            login_user(user)

            return redirect('/')

    return render_template('login.html')



@app.route('/register',methods=['GET','POST'])
def register():

    if request.method=="POST":

        username=request.form['username']

        password=request.form['password']

        user=User(username=username,password=password)

        db.session.add(user)

        db.session.commit()

        return redirect('/login')

    return render_template('register.html')



@app.route('/upload',methods=['GET','POST'])
@login_required
def upload():

    if request.method=="POST":

        file=request.files['image']

        caption=request.form['caption']

        filepath=os.path.join(app.config['UPLOAD_FOLDER'],file.filename)

        file.save(filepath)

        post=Post(image=file.filename,
                  caption=caption,
                  user_id=current_user.id)

        db.session.add(post)

        db.session.commit()

        return redirect('/')

    return render_template('upload.html')


@app.route('/logout')
def logout():

    logout_user()

    return redirect('/login')


@app.route('/profile')
@login_required
def profile():

    posts=Post.query.filter_by(user_id=current_user.id).all()

    return render_template('profile.html',posts=posts)



if __name__=="__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)