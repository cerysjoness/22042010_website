from flask import Flask, flash, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'your_very_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
db = SQLAlchemy(app)

class Shirt(db.Model):
    __tablename__ = 'shirts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    price = db.Column(db.String(32))
    description = db.Column(db.Text)
    image = db.Column(db.String(128))
    detailedDescription = db.Column(db.Text)

class BasketItem(db.Model):
    __tablename__ = 'basket_items'
    id = db.Column(db.Integer, primary_key=True)
    shirt_id = db.Column(db.Integer, db.ForeignKey('shirts.id'))
    size = db.Column(db.String(16))
    quantity = db.Column(db.Integer, default=1)
    shirt = db.relationship('Shirt', backref=db.backref('basket_items', lazy='dynamic'))

class AddToBasketForm(FlaskForm):
    shirt_id = HiddenField('Shirt ID')
    selected_size = SelectField('Select Size', choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')])

class CheckoutForm(FlaskForm):
    card_number = StringField('Card Number', validators=[InputRequired(), Length(min=16, max=19), Regexp(r'^[0-9 -]+$')])
    expiration_date = StringField('Expiration Date', validators=[InputRequired(), Length(min=5, max=5), Regexp(r'^\d{2}/\d{2}$')])
    cvv = StringField('CVV', validators=[InputRequired(), Length(min=3, max=4)])
    submit = SubmitField('Submit Order')

@app.route('/', methods=['GET', 'POST'])
def galleryPage():
    form = AddToBasketForm()
    shirts = Shirt.query.all()
    sort_option = request.args.get('sort_option')
    if sort_option == 'price':
        shirts = sorted(shirts, key=lambda x: float(x.price.strip('£')))
    elif sort_option == 'name':
        shirts = sorted(shirts, key=lambda x: x.name)
    elif sort_option == 'environmental_impact':
        shirts = sorted(shirts, key=lambda x: float(x.description.split(' ')[0]))
    return render_template('index.html', shirts=shirts, form=form)

@app.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    shirt_id = request.form.get('shirt_id')
    selected_size = request.form.get('selected_size')
    quantity = request.form.get('quantity', type=int)

    if not shirt_id or not selected_size or quantity <= 0:
        flash('Invalid item details.')
        return redirect(request.referrer)

    try:
        shirt = Shirt.query.get_or_404(shirt_id)
        basket_item = {
            'id': shirt_id,
            'name': shirt.name,
            'price': shirt.price,
            'quantity': quantity,
            'size': selected_size,
            'image': shirt.image
        }

        basket = session.get('ShoppingBasket', [])
        if not isinstance(basket, list):
            flash('Basket error, please try again.')
            session['ShoppingBasket'] = []
            return redirect(url_for('galleryPage'))
        
        basket.append(basket_item)
        session['ShoppingBasket'] = basket
        flash('Item added to basket successfully!')
    except Exception as e:
        flash(str(e))
        return redirect(request.referrer)
        
    return redirect(url_for('galleryPage'))

@app.route('/product/<int:productId>')
def singleProductPage(productId):
    shirt = Shirt.query.get_or_404(productId)
    form = AddToBasketForm()
    return render_template('singleProduct.html', shirt=shirt, form=form)

@app.route('/view_basket')
def view_basket():
    basket = session.get('ShoppingBasket', [])
    if not basket:
        flash('Your basket is empty.', 'info')
        return render_template('basket.html', basket=[], total_price=0.0)

    try:
        total_price = sum(float(item['price'].strip('£')) * item['quantity'] for item in basket)
        return render_template('basket.html', basket=basket, total_price=total_price)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        # Ensure a response is returned even in the case of an error
        return render_template('basket.html', basket=basket, total_price=0.0)

@app.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    item_id = request.form.get('item_id')
    if not item_id:
        flash('No item specified!', 'error')
        return redirect(url_for('view_basket'))

    basket = session.get('ShoppingBasket', [])
    new_basket = [item for item in basket if item['id'] != item_id]

    session['ShoppingBasket'] = new_basket
    flash('Item removed successfully.', 'success')
    return redirect(url_for('view_basket'))

@app.route('/clear_basket', methods=['POST'])
def clear_basket():
    # Check if the basket session key exists and clear it
    if 'ShoppingBasket' in session:
        session.pop('ShoppingBasket', None)  # Remove the basket from session
        flash('Your basket has been cleared.', 'success')
    else:
        flash('Your basket is already empty.', 'info')

    return redirect(url_for('view_basket'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Add your payment processing logic here
            session.pop('ShoppingBasket', None)
            flash('Checkout successful! Thank you for your purchase.')
            return redirect(url_for('payment_confirmation'))
        else:
            flash('Please correct the errors in the form.')
    return render_template('checkout.html', form=form)

@app.route('/payment_confirmation')
def payment_confirmation():
    return render_template('payment_confirmation.html')

if __name__ == "__main__":
    app.run(debug=True)

