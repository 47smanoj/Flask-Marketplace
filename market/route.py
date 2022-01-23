#from crypt import methods
#import email
#from crypt import methods
from unicodedata import category
from market import app
from flask import flash, render_template, redirect, url_for, flash, request
from market.model import item, user
from market.forms import LoginForm, RegisterForms, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if(request.method=='POST'):
        #purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = item.query.filter_by(name=purchased_item).first()
        if(p_item_object):
            if(current_user.can_purchase(p_item_object)):
                p_item_object.buy(current_user)
                flash(f'Congratulation you purchased {p_item_object.name} for ${p_item_object.price}', category='success')
            else:
                flash(f'You have unsufficient funds', category='danger')
        #sell item logic
        sold_item = request.form.get('sold_item')
        s_item_object = item.query.filter_by(name=sold_item).first()
        if(s_item_object):
            s_item_object.sell(current_user)
            flash(f'Congratulation you sold {s_item_object.name} for ${s_item_object.price}', category='success')


        return redirect(url_for('market_page'))
    if(request.method=="GET"):
        items = item.query.filter_by(owner=None)
        owned_items = item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForms()
    if form.validate_on_submit():
        user_to_create = user(username=form.username.data,
                              email = form.email.data,
                              password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
 
        login_user(user_to_create)
        flash(f"Account created successfully. You are now logged in as {user_to_create.username}", category='success')        
        
        return redirect(url_for('market_page'))
    if form.errors != {}: #if there are errors from the validation
        for err_msg in form.errors.values():
            flash(f"There was an error in form field validation: {err_msg}", category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = user.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password not matched! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logout successfully", category='info')
    return redirect(url_for('home_page'))