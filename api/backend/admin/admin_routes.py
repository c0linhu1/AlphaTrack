from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

admin = Blueprint("admin", __name__)


# Get all users
# [Gregory-1]
@admin.route("/users", methods=["GET"])
def get_users():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM User")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Create a new user
# [Gregory-1]
@admin.route("/users", methods=["POST"])
def create_user():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json(silent=True) or {}
        required = ["first_name", "last_name", "email"]

        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor.execute("""
            INSERT INTO User (first_name, last_name, email, status)
            VALUES (%s, %s, %s, 'active')
        """, (data["first_name"], data["last_name"], data["email"]))
        get_db().commit()

        return jsonify({"message": "User created", "user_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Deactivate a user
# [Gregory-3]
@admin.route("/users/<int:user_id>", methods=["PUT"])
def deactivate_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            UPDATE User
            SET status = 'inactive', deactivated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """, (user_id,))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User deactivated"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Reactivate a user
# [Gregory-3]
@admin.route("/users/<int:user_id>/reactivate", methods=["PUT"])
def reactivate_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            UPDATE User
            SET status = 'active', deactivated_at = NULL
            WHERE user_id = %s
        """, (user_id,))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User reactivated"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Delete a user
# [Gregory-3]
@admin.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM User WHERE user_id = %s", (user_id,))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User deleted"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get all roles
# [Gregory-1]
@admin.route("/roles", methods=["GET"])
def get_roles():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Role")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Create a new role
# [Gregory-1]
@admin.route("/roles", methods=["POST"])
def create_role():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json(silent=True) or {}
        required = ["role_name"]

        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor.execute("""
            INSERT INTO Role (role_name, role_description, is_active)
            VALUES (%s, %s, TRUE)
        """, (data["role_name"], data.get("role_description")))
        get_db().commit()

        return jsonify({"message": "Role created", "role_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Delete a role
# [Gregory-1]
@admin.route("/roles/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM Role WHERE role_id = %s", (role_id,))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Role not found"}), 404

        return jsonify({"message": "Role deleted"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Update or assign a user's role
# [Gregory-2]
@admin.route("/users/<int:user_id>/roles", methods=["PUT"])
def update_user_role(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json(silent=True) or {}

        if "role_id" not in data:
            return jsonify({"error": "Missing role_id"}), 400

        cursor.execute("SELECT user_id FROM User WHERE user_id = %s", (user_id,))
        user_exists = cursor.fetchone()

        if not user_exists:
            return jsonify({"error": "User not found"}), 404

        cursor.execute("SELECT role_id FROM Role WHERE role_id = %s", (data["role_id"],))
        role_exists = cursor.fetchone()

        if not role_exists:
            return jsonify({"error": "Role not found"}), 404

        cursor.execute("SELECT user_role_id FROM User_Role WHERE user_id = %s", (user_id,))
        existing_assignment = cursor.fetchone()

        if existing_assignment:
            cursor.execute("""
                UPDATE User_Role
                SET role_id = %s
                WHERE user_id = %s
            """, (data["role_id"], user_id))
            get_db().commit()
            return jsonify({"message": "User role updated"}), 200
        else:
            cursor.execute("""
                INSERT INTO User_Role (user_id, role_id)
                VALUES (%s, %s)
            """, (user_id, data["role_id"]))
            get_db().commit()
            return jsonify({"message": "User role assigned"}), 201

    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get system activity logs
# [Gregory-4]
@admin.route("/activity-logs", methods=["GET"])
def get_activity_logs():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT u.first_name, u.last_name, al.event_type, al.event_category,
                   al.event_description, al.ip_address, al.created_at
            FROM Activity_Log al
            JOIN User u ON al.user_id = u.user_id
            ORDER BY al.created_at DESC
        """)
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get all backups
# [Gregory-6]
@admin.route("/backups", methods=["GET"])
def get_backups():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Backup ORDER BY created_at DESC")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Create a new backup
# [Gregory-6]
@admin.route("/backups", methods=["POST"])
def create_backup():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json(silent=True) or {}
        required = ["backup_name", "storage_location", "backup_size_gb"]

        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor.execute("""
            INSERT INTO Backup (backup_name, backup_status, storage_location, backup_size_gb)
            VALUES (%s, 'complete', %s, %s)
        """, (data["backup_name"], data["storage_location"], data["backup_size_gb"]))
        get_db().commit()

        return jsonify({"message": "Backup created", "backup_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Delete a backup
# [Gregory-6]
@admin.route("/backups/<int:backup_id>", methods=["DELETE"])
def delete_backup(backup_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM Backup WHERE backup_id = %s", (backup_id,))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Backup not found"}), 404

        return jsonify({"message": "Backup deleted"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Recalculate portfolio total value
# [Gregory-5]
@admin.route("/portfolios/<int:portfolio_id>/validation", methods=["PUT"])
def recalculate_portfolio(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            UPDATE Portfolio
            SET total_value = (
                SELECT IFNULL(SUM(current_value), 0)
                FROM Holding
                WHERE portfolio_id = %s
            )
            WHERE portfolio_id = %s
        """, (portfolio_id, portfolio_id))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Portfolio not found"}), 404

        return jsonify({"message": "Portfolio recalculated"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()