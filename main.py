from flask import Flask, render_template, redirect, url_for, flash, jsonify, request, session
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, NewProductForm
from functools import wraps
import os
import stripe
import json
from uuid import uuid4


stripe.api_key = os.environ["STRIPE_API_KEY_TEST1"]

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
bootstrap = Bootstrap5(app)

YOUR_DOMAIN = 'http://localhost:4242'

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create application object for LoginManager
login_manager = LoginManager()
# configure it for login
login_manager.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    zipcode = db.Column(db.Integer)
    phone = db.Column(db.Integer)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    pic_url = db.Column(db.String(200), nullable=False)
    on_sale = db.Column(db.Boolean, nullable=False)
    sale_price = db.Column(db.Float, nullable=True)
    stars = db.Column(db.Integer)
    colour = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    stripe_product_id = db.Column(db.String(100), nullable=True)


class ShoppingCart(db.Model):
    __tablename__ = "shopping_cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    user = db.relationship("User", backref=db.backref("shopping_cart", lazy=True))
    product = db.relationship("Product", backref=db.backref("shopping_cart", lazy=True))



with app.app_context():
    db.create_all()


def admin_only(function):
    # The @wraps decorator ensures that the decorated function maintains its original name and docstring.
    @wraps(function)
    def decorated_function(*args, **kwargs):
        # Check if the current user is authenticated.
        if current_user.is_authenticated:
            # Check if the current user's id is 1 (assuming 1 is the admin user's id).
            if current_user.id == 1:
                # If the user is authenticated and is an admin (id == 1),
                # call and execute the original view function with the provided arguments and keyword arguments.
                return function(*args, **kwargs)
        # If the user is not authenticated or is not an admin (id != 1),
        # redirect the user to the "main" endpoint.
        return redirect(url_for("main"))

    # Return the decorated function.
    return decorated_function

@app.route('/')
def main():
    all_products = Product.query.all()
    return render_template("index.html", products=all_products)

@app.route('/products-by-category/<string:category>')
def products_by_category(category):
    products_in_category = Product.query.filter_by(category=category)
    return render_template("index.html", products=products_in_category)

@app.route('/about')
def about():
    return render_template("about.html")


def get_cart_items():
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        # Check if the anonymous user ID is stored in the session
        if 'anonymous_user_id' in session:
            user_id = session['anonymous_user_id']
        else:
            # If no anonymous user ID is found, return an empty list or handle it as needed
            return []

    cart_items = db.session.query(ShoppingCart, Product).join(Product, Product.id == ShoppingCart.product_id).filter(ShoppingCart.user_id == user_id).all()
    return cart_items

@app.route('/cart')
def cart():
    cart_items = get_cart_items()
    # Calculate total price
    normal_price = sum(cart_item.quantity * product.price for cart_item, product in cart_items)
    # Calculate total price and sale price
    total_price = sum(cart_item.quantity * (product.sale_price if product.on_sale else product.price) for cart_item, product in cart_items)
    savings = normal_price - total_price

    return render_template("cart.html", cart_items=cart_items,
                           subtotal=total_price, savings=savings)



@app.route('/add-to-cart/<int:product_id>', methods=["POST"])
def add_to_cart(product_id):
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        # Generate a unique identifier for anonymous users
        if 'anonymous_user_id' not in session:
            session['anonymous_user_id'] = str(uuid4())
        user_id = session['anonymous_user_id']

    existing_item = ShoppingCart.query.filter_by(user_id=user_id, product_id=product_id).first()

    if existing_item:
        # If the item already exists in the cart, increase its quantity
        existing_item.quantity += 1
    else:
        # If the item is not in the cart, create a new entry
        new_item = ShoppingCart(product_id=product_id, user_id=user_id, quantity=1)
        db.session.add(new_item)

    db.session.commit()

    # Return a JSON response indicating success
    return jsonify({'success': True})

@app.route('/change-item-quantity/<int:product_id>', methods=["GET", "POST"])
def change_item_quantity(product_id):
    new_quantity = int(request.form['quantity-input'])
    print(f"new_quantity {new_quantity}")
    with app.app_context():
        quantity_to_update = ShoppingCart.query.filter_by(product_id=product_id).first()
        if new_quantity > 0:
            quantity_to_update.quantity = new_quantity
        else:
            db.session.delete(quantity_to_update)
        db.session.commit()

    return redirect(url_for("cart"))

@app.route('/get-cart-count')
def get_cart_count():
    # Get the current user's cart
    cart_items = get_cart_items()
    # and count from the database
    cart_count = sum(cart_item.quantity for cart_item, product in cart_items)

    return jsonify({'cart_count': cart_count})


@app.route('/empty-cart', methods=['POST'])
def empty_cart():
    # Code to empty the cart goes here
    # For example:
    # delete all items from the shopping cart for the current user
    print(f"in empty cart {current_user.id}")
    ShoppingCart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return jsonify({'success': True})


def add_all_products_to_stripe():
    # Get list of product names from Stripe and put them in a list
    products_in_stripe = stripe.Product.list()
    stripe_prod_names = []
    [stripe_prod_names.append(product["name"]) for product in products_in_stripe.data if product["name"] not in stripe_prod_names]

    # Query products from database
    with app.app_context():
        all_products = Product.query.all()

    # Then add product to Stripe if it does not already exist there
    for product in all_products:
        #product = all_products
        if product.name not in stripe_prod_names:
            if product.on_sale:
                product_price = int(product.sale_price)
            else:
                product_price = int(product.price)
            new_product = stripe.Product.create(
                name=product.name,
                images=[product.pic_url],
                description=product.description,
                default_price_data={
                    "currency":"EUR",
                    "unit_amount":product_price * 100,
                }
            )


# add_all_products_to_stripe()

def add_stripe_ids_to_products():
    # Get list of product names from Stripe and put them in a dictionary "name":"id"
    products_in_stripe = stripe.Product.list()
    stripe_prod_dict = {product["name"]:product["default_price"] for product in products_in_stripe.data}

    # Query products from database to check if the product is existing
    # if it is existing query the product by name, update the stripe_product_id
    with app.app_context():
        all_products = Product.query.all()
        for prod_name, id in stripe_prod_dict.items():
            if any(product.name == prod_name for product in all_products):
                product_to_update = Product.query.filter_by(name=prod_name).first()
                product_to_update.stripe_product_id = id
                db.session.commit()

add_stripe_ids_to_products()

@app.route('/checkout.html')
def checkout():
    return render_template('checkout.html')

@app.route('/return.html')
def return_page():
    return render_template('return.html')



@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    # Get items from the cart of the current user
    cart_items = get_cart_items()

    # Iterate over each tuple (cart_item) in cart_items
    # Each cart_item is a tuple containing a ShoppingCart object and a Product object
    product_id_list = [
        # Constructing a dictionary for each cart_item
        {
            # Accessing the stripe_product_id attribute of the Product object within the tuple
            "price": cart_item[1].stripe_product_id,
            # Accessing the quantity attribute of the ShoppingCart object within the tuple
            "quantity": cart_item[0].quantity
        }
        # Iterating over each tuple (cart_item) in cart_items
        for cart_item in cart_items
    ]

    try:
        session = stripe.checkout.Session.create(
            ui_mode = 'embedded',
            line_items=product_id_list,
            mode='payment',
            return_url=YOUR_DOMAIN + '/return.html?session_id={CHECKOUT_SESSION_ID}',
        )
    except Exception as e:
        return str(e)

    return jsonify(clientSecret=session.client_secret)

@app.route('/session-status', methods=['GET'])
def session_status():
  session = stripe.checkout.Session.retrieve(request.args.get('session_id'))

  return jsonify(status=session.status, customer_email=session.customer_details.email,
                 customer_name=session.customer_details.name)

@app.route("/product/<int:product_id>", methods=["GET", "POST"])
def product(product_id):
    selected_product = Product.query.get(product_id)
    selected_product_category = selected_product.category
    category_count = len(Product.query.filter_by(category=selected_product_category).all())
    all_products = Product.query.all()
    return render_template("product.html", product=selected_product, category_count=category_count,
                           all_products=all_products)

@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        password = generate_password_hash(register_form.password.data,
                           method="pbkdf2",
                           salt_length=16)
        name = register_form.name.data
        address = register_form.address.data
        city = register_form.city.data
        zipcode = register_form.zipcode.data
        phone = register_form.phone.data

        if User.query.filter_by(email=email).first():
            flash("you have already registered with the given email, login instead", "error")
            return redirect(url_for("login"))
        else:
            with app.app_context():
                new_user = User(email=email, password=password, name=name, address=address,
                                city=city, zipcode=zipcode, phone=phone)
                db.session.add(new_user)
                db.session.commit()
                # authenticate the user with Flask-Login
                login_user(new_user)

            return redirect(url_for("main"))
    return render_template("register.html", form=register_form)

@app.route('/add-new-product', methods=["GET", "POST"])
@admin_only
def add_new_product():
    new_product_form = NewProductForm()
    if new_product_form.validate_on_submit():
        name = new_product_form.name.data
        price = new_product_form.price.data
        pic_url = new_product_form.pic_url.data
        on_sale = new_product_form.on_sale.data
        sale_price = new_product_form.sale_price.data
        stars = new_product_form.stars.data
        colour = new_product_form.colour.data
        product_id = new_product_form.product_id.data
        description = new_product_form.description.data
        category = new_product_form.category.data


        if User.query.filter_by(name=name).first():
            flash("you have already registered product with the given name", "error")
            return render_template("add_new_product.html")
        else:
            with app.app_context():
                new_product = Product(name=name, price=price, pic_url=pic_url,
                                      on_sale=on_sale, stars=stars, sale_price=sale_price,
                                      colour=colour, product_id=product_id, description=description,
                                      category=category)
                db.session.add(new_product)
                db.session.commit()

                if on_sale:
                    product_price = int(sale_price)
                else:
                    product_price = int(price)
                print(f"name: {name}, images: {pic_url}, description: {description}, product_price: {product_price}")
                new_product_to_stripe = stripe.Product.create(
                    name=name,
                    images=[pic_url],
                    description=description,
                    default_price_data={
                        "currency": "EUR",
                        "unit_amount": product_price * 100,
                    }
                )

                product_to_update = Product.query.filter_by(name=name).first()
                product_to_update.stripe_product_id = new_product_to_stripe.default_price
                db.session.commit()

            return redirect(url_for("main"))
    return render_template("add_new_product.html", form=new_product_form)

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        if User.query.filter_by(email=email).first():
            user = User.query.filter_by(email=email).first()
            if check_password_hash(user.password, password):
                login_user(user)

                return redirect(url_for("main"))
            else:
                flash("wrong password, please try again", "error")
                return render_template("login.html", form=login_form)
        else:
            flash("The given email is not found in database, please try again", "error")
            return render_template("login.html", form=login_form)
    return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

@login_manager.user_loader
def load_user(user_id):
    print(f"in load_user {user_id}")
    return User.query.get(int(user_id))

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5050, debug=True)
    app.run(port=4242, debug=True)


