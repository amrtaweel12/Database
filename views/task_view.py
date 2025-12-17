# views/task_view.py
from flask import Blueprint
from helpers.db_helper import get_db_connection

task = Blueprint('task', __name__)

# ... existing routes ...

def create_task(cursor, o_id, c_id, user_id, m_id):
    """
    Creates a delivery task.
    Uses the SHARED cursor to remain in the same transaction as the Order.
    """
    # 1. Get User Address
    cursor.execute("SELECT address FROM User WHERE user_id = %s", (user_id,))
    user_row = cursor.fetchone()
    
    if not user_row:
        raise ValueError(f"User {user_id} not found, cannot create task.")

    # 2. Insert Task
    cursor.execute("""
        INSERT INTO Task 
        (o_id, c_id, user_id, m_id, user_address, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (o_id, c_id, user_id, m_id, user_row["address"], 0))
    
    return cursor.lastrowid