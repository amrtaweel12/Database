from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, jsonify, flash
import uuid
from helpers import db_helper

def find_available_courier(m_id):

    db = db_helper.get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)
        
    try:
        cursor.execute("""
            SELECT c_id
            FROM Courier 
            WHERE m_id = %s
        """, (m_id,))
        c_id = cursor.fetchone()
        return c_id
    
    except Exception as e:
        print(f"Dashboard error: {e}")
        return f"Error: {e}", 500
    finally:
        cursor.close()
        db.close()