from flask import Blueprint, render_template

# Defining the blueprint with the name 'home_page'
main = Blueprint('home_page', __name__)

@main.route('/')
def home_page():
    cart_count = 0  # logic to pull from session later
    return render_template("home_page.html", active_page="home", cart_count=cart_count)

@main.route('/restaurants')
def restaurants():
    return render_template("restaurants.html")