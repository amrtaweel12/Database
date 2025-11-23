# views/user_view.py
from flask import Blueprint, render_template, request, redirect, url_for, session
import bcrypt
from helpers import db_helper

user = Blueprint('user', __name__)

@user.route('/login')
def user_login():
    """User login page"""
    return render_template('user_login.html')

@user.route('/submit_login', methods=['POST'])
def user_submit_login():
    """Handle user login"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not email or not password:
        return "Email and password are required", 400
    
    # Database lookup
    db = db_helper.get_db_connection("localhost", "root", "123654", "term_project")
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        
        if user_data and bcrypt.checkpw(password.encode("utf-8"), user_data['password'].encode("utf-8")):
            # Login successful
            session['user_id'] = user_data['user_id']
            session['user_name'] = user_data['name']
            session['user_type'] = 'user'
            print("Giriş başarılı")
            return redirect(url_for('home_page.home_page'))
        else:
            print("Giriş başarısız")
            return "Invalid email or password", 401
    except Exception as e:
        print(f"Login error: {e}")
        return f"An error occurred: {e}", 500
    finally:
        cursor.close()
        db.close()

@user.route('/logout')
def user_logout():
    """User logout"""
    session.clear()
    return redirect(url_for('home_page.home_page'))

@user.route('/signup')
def user_signup():
    """User signup page"""
    return render_template('user_signup.html')

@user.route('/submit_form', methods=['POST'])
def user_submit_signup_form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")
    address = request.form.get("address")
    city = request.form.get("city")
    email = request.form.get("email")
    gender = request.form.get("gender")
    salary = request.form.get("salary")
    status = request.form.get("martial_status")
    occupation = request.form.get("occupation")
    age = request.form.get("age")

    # Hash password
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # DB Insert
    db = db_helper.get_db_connection("localhost", "root", "123654","term_project")
    cursor = db.cursor()
    
    query = """
        INSERT INTO User 
        (name, email, password, Age, Gender, Marital_Status, Occupation, Monthly_Income, city, address) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Combining First/Last name because DB has 'name' column
    full_name = f"{first_name} {last_name}"
    
    values = (full_name, email, password_hash, age, gender, status, occupation, salary, city, address)
    
    try:
        cursor.execute(query, values)
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return f"Registration failed: {e}", 500
    finally:
        cursor.close()
        db.close()

    return redirect(url_for("home_page.home_page"))