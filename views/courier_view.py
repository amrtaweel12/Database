import mysql.connector
import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from helpers import db_helper

courier = Blueprint('courier', __name__)

# ==========================================
# WEB FORM ROUTES (Browser Interaction)
# ==========================================

@courier.route('/login')
def courier_login():
    """Renders the courier login HTML page."""
    return render_template("courier_login.html")

@courier.route('/submit_login', methods=['POST'])
def courier_submit_login():
    """Handle courier login"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not email or not password:
        return "Email and password are required", 400
    
    # Database lookup
    db = db_helper.get_db_connection("localhost", "root", "123654", "term_project")
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM Courier WHERE email = %s", (email,))
        courier_data = cursor.fetchone()
        
        if courier_data and bcrypt.checkpw(password.encode("utf-8"), courier_data['password'].encode("utf-8")):
            # Login successful
            session['user_id'] = courier_data['c_id']
            session['user_name'] = courier_data['name']
            session['user_type'] = 'courier'
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

@courier.route('/logout')
def courier_logout():
    """Courier logout"""
    session.clear()
    return redirect(url_for('home_page.home_page'))

@courier.route('/signup')
def courier_signup():
    """Renders the signup HTML page."""
    return render_template("courier_signup.html") 

@courier.route('/submit_signup', methods=['POST'])
def submit_signup():
    """Handles the HTML Form submission."""
    # 1. Get Data from HTML Form
    name = request.form.get("first_name")  # Updated to match template
    surname = request.form.get("last_name")  # Updated to match template
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    city = request.form.get("city")
    phone = request.form.get("phone")
    
    # 2. Get Courier Specific Data
    experience = request.form.get("experience", 0)
    expected_payment = request.form.get("expected_payment", 100)

    # 3. Hash Password
    if password:
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    else:
        return "Password required", 400

    # 4. Calculate Payment Range (Logic: Max is 20% higher than min preference)
    expected_min = float(expected_payment)
    expected_max = expected_min * 1.2 

    # 5. Database Operation
    db = db_helper.get_db_connection("localhost", "root", "123654","term_project")
    cursor = db.cursor()

    query = """
        INSERT INTO Courier 
        (name, surname, email, password, Age, experience, expected_payment_min, expected_payment_max, 
         rating, ratingCount, taskCount) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0.0, 0, 0)
    """
    
    values = (name, surname, email, password_hash, age, experience, expected_min, expected_max)

    try:
        cursor.execute(query, values)
        db.commit()
        print("Courier Registered Successfully via Form")
    except Exception as e:
        print(f"Error registering courier: {e}")
        db.rollback()
        return f"Registration Failed: {e}", 500
    finally:
        cursor.close()
        db.close()

    # Redirect to Home Page after success
    return redirect(url_for("home_page.home_page"))


# ==========================================
# API ROUTES (JSON - For Mobile/External Apps)
# ==========================================

@courier.route("/", methods=["GET"])
def get_all_couriers():
    """Fetches all couriers as JSON."""
    db = db_helper.get_db_connection("localhost", "root", "123654","term_project")
    if not db:
        return jsonify({"error": "Database connection failed"}), 500
    
    mycursor = db.cursor(dictionary=True) 
    try:
        mycursor.execute("SELECT * FROM Courier")
        couriers = mycursor.fetchall()
        return jsonify(couriers)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        mycursor.close()
        db.close()

@courier.route("/<int:courier_id>", methods=["GET"])
def get_courier(courier_id):
    """Fetches a single courier by c_id."""
    db = db_helper.get_db_connection("localhost", "root", "123654","term_project")
    if not db:
        return jsonify({"error": "Database connection failed"}), 500
        
    mycursor = db.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Courier WHERE c_id = %s"
        mycursor.execute(query, (courier_id,))
        courier_data = mycursor.fetchone()
        
        if courier_data:
            return jsonify(courier_data)
        else:
            return jsonify({"error": "Courier not found"}), 404
            
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        mycursor.close()
        db.close()

@courier.route("/", methods=["POST"])
def create_courier_api():
    """Creates a new courier via JSON (API style)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    # Extracting data
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')
    age = data.get('age')
    gender = data.get('gender')
    marital_status = data.get('marital_status')
    experience = data.get('experience', 0)
    expected_payment = data.get('expected_payment', 100)
    r_id = data.get('r_id', None)

    # Validations
    if not email or not password or not name:
        return jsonify({"error": "Missing required fields: email, password, or name"}), 400

    # Hashing
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    # Calc Payment
    expected_min = float(expected_payment)
    expected_max = expected_min * 1.2

    db = db_helper.get_db_connection("localhost", "root", "123654","term_project")
    if not db:
        return jsonify({"error": "Database connection failed"}), 500
        
    mycursor = db.cursor()
    try:
        query = """
            INSERT INTO Courier 
            (r_id, name, surname, email, password, Age, Gender, 
             Marital_Status, experience, expected_payment_min, expected_payment_max, rating, ratingCount, taskCount) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0.0, 0, 0)
        """
        values = (
            r_id, name, surname, email, password_hash, age, gender,
            marital_status, experience, expected_min, expected_max
        )
        mycursor.execute(query, values)
        db.commit()
        new_courier_id = mycursor.lastrowid
        
    except mysql.connector.Error as err:
        db.rollback() 
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        mycursor.close()
        db.close()

    return jsonify({
        "message": "Courier created successfully",
        "c_id": new_courier_id
    }), 201