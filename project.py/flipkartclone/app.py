from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------------ DATABASE MODELS ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username=None, password=None, **kwargs):
        super(User, self).__init__(**kwargs)
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    image = db.Column(db.String(300))
    
    def __init__(self, name=None, price=None, image=None, **kwargs):
        super(Product, self).__init__(**kwargs)
        if name is not None:
            self.name = name
        if price is not None:
            self.price = price
        if image is not None:
            self.image = image

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    def __init__(self, user_id=None, product_id=None, **kwargs):
        super(Cart, self).__init__(**kwargs)
        if user_id is not None:
            self.user_id = user_id
        if product_id is not None:
            self.product_id = product_id

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

@app.route("/remove/<int:id>")
def remove_from_cart(id):
    if "user" not in session:
        return redirect("/login")

    item = Cart.query.filter_by(user_id=session["user"], product_id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()

    return redirect("/cart")

@app.route("/checkout")
def checkout():
    if "user" not in session:
        return redirect("/login")

    # Clear user's entire cart to simulate order placed
    items = Cart.query.filter_by(user_id=session["user"]).all()
    for item in items:
        db.session.delete(item)
    db.session.commit()

    return render_template("checkout.html")

@app.route("/search")
def search():
    query = request.args.get('q', '').strip()
    if not query:
        products = Product.query.all()
    else:
        products = Product.query.filter(
            Product.name.contains(query)
        ).all()
    
    return render_template("index.html", products=products, search_query=query)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Seed dummy products if empty
        if not Product.query.first():
            dummy_products = [
                Product(name="Apple iPhone 15 (Black, 128 GB)", price=72999, image="https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/h/d/9/-original-imagtc2qzpzcdgns.jpeg"),
                Product(name="SAMSUNG Galaxy S23 Ultra 5G", price=104999, image="https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/t/b/r/-original-imagpgy2tzkuh4w2.jpeg"),
                Product(name="SONY PlayStation 5 Console", price=54990, image="https://rukminim2.flixcart.com/image/312/312/kqqykcw0/gamingconsole/y/r/q/cfi-1008a01r-825-sony-original-imag4p56fcfkchhk.jpeg"),
                Product(name="MacBook Air M2 (8GB RAM, 256GB SSD)", price=99990, image="https://rukminim2.flixcart.com/image/312/312/xif0q/computer/2/v/v/-original-imagfdeqter4sj2j.jpeg")
            ]
            db.session.add_all(dummy_products)
            db.session.commit()
    app.run(debug=True)