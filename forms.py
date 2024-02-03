from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField, URLField, BooleanField, IntegerRangeField
from wtforms.validators import DataRequired, URL, NumberRange, Optional

##WTForm

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    zipcode = IntegerField("Zip code", validators=[DataRequired()])
    phone = IntegerField("Phone", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class NewProductForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()])
    pic_url = URLField("URL for picture*", validators=[DataRequired()])
    colour = StringField("Colour*", validators=[DataRequired()])
    product_id = StringField("Product ID*", validators=[DataRequired()])
    category = StringField("Category*", validators=[DataRequired()])
    price = IntegerField("Price*", validators=[DataRequired()])
    on_sale = BooleanField("Product on sale?", default=False)
    sale_price = IntegerField("Price on sale", validators=[Optional()])
    stars = IntegerRangeField("Stars*", validators=[NumberRange(min=0, max=5)])
    description = StringField("Description", validators=[Optional()], default="Lorem ipsum dolor sit amet consectetur adipisicing elit. Praesentium at dolorem quidem modi. Nam sequi consequatur obcaecati excepturi alias magni, accusamus eius blanditiis delectus ipsam minima ea iste laborum vero?")


    submit = SubmitField("Add product")
    #TODO: add product category
