from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ------------------ DATABASE MODELS ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    image = db.Column(db.String(300))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username,password=password).first()

        if user:
            session["user"] = user.id
            return redirect("/")

    return render_template("login.html")

@app.route("/add/<int:id>")
def add_to_cart(id):
    if "user" in session:
        item = Cart(user_id=session["user"], product_id=id)
        db.session.add(item)
        db.session.commit()

    return redirect("/")

@app.route("/cart")
def cart():
    if "user" not in session:
        return redirect("/login")

    items = Cart.query.filter_by(user_id=session["user"]).all()

    products = []
    for i in items:
        p = Product.query.get(i.product_id)
        products.append(p)

    return render_template("cart.html", products=products)

# ------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)