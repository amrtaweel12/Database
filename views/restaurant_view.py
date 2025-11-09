import mysql.connector
from flask import Blueprint, request, jsonify
from helpers.db_helper import get_db_connection

restaurant = Blueprint("restaurant", __name__)

@restaurant.route("/", methods=["POST"])
def create_restaurant():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    id = data.get("id")
    name = data.get("name")
    city = data.get("city")
    rating = data.get("rating")
    rating_count = data.get("rating_count")
    cost = data.get("cost")
    cuisine = data.get("cuisine")
    lic_no = data.get("lic_no")
    link = data.get("link")
    address = data.get("address")
    menu = data.get("menu")

    if id is None:
        return jsonify({"error": "Missing field: id"}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    cur = db.cursor()
    try:
        cur.execute(
            """
            INSERT INTO Restaurant (id, name, city, rating, rating_count, cost, cuisine, lic_no, link, address, menu)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (id, name, city, rating, rating_count, cost, cuisine, lic_no, link, address, menu),
        )
        db.commit()
    except mysql.connector.Error as err:
        db.rollback()
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cur.close()
        db.close()

    return jsonify({
        "message": "Restaurant created successfully",
        "id": id
    }), 201


@restaurant.route("/", methods=["GET"])
def get_all_restaurants():
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM Restaurant")
        rows = cur.fetchall()
        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cur.close()
        db.close()


@restaurant.route("/<int:r_id>", methods=["GET"])
def get_restaurant(r_id):
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM Restaurant WHERE id = %s", (r_id,))
        row = cur.fetchone()
        if row:
            return jsonify(row)
        return jsonify({"error": "Restaurant not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cur.close()
        db.close()


@restaurant.route("/by-city/<string:city>", methods=["GET"])
def get_restaurants_by_city(city):
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM Restaurant WHERE city = %s", (city,))
        rows = cur.fetchall()
        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cur.close()
        db.close()
