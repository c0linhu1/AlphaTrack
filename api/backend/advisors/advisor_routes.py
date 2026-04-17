from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

advisors = Blueprint("advisors", __name__)


# Get all clients for an advisor
# [James-1], [James-7]
@advisors.route("/clients/<int:user_id>", methods=["GET"])
def get_clients(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.client_id, c.user_id, c.name, c.email, c.account_status,
                   c.risk_tolerance, p.portfolio_id, p.portfolio_name,
                   p.total_value, p.performance_metric, rp.risk_level,
                   rp.threshold_min, rp.threshold_max
            FROM Client c
            LEFT JOIN Portfolio p ON p.user_id = c.user_id
            LEFT JOIN Risk_Profile rp ON rp.client_id = c.client_id
            WHERE c.user_id = %s
            ORDER BY c.client_id, p.total_value DESC
        """, (user_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Add a new client portfolio
# [James-6]
@advisors.route("/clients/<int:user_id>", methods=["POST"])
def add_client_portfolio(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        required = ["benchmark_id", "portfolio_name", "total_value"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor.execute("""
            INSERT INTO Portfolio (user_id, benchmark_id, portfolio_name, total_value)
            VALUES (%s, %s, %s, %s)
        """, (user_id, data["benchmark_id"], data["portfolio_name"], data["total_value"]))
        get_db().commit()
        return jsonify({"message": "Client portfolio created", "portfolio_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Close/remove a client account
# [James-5]
@advisors.route("/clients/<int:client_id>", methods=["PUT"])
def close_client_account(client_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json(silent=True) or {}
        account_status = data.get("account_status", "closed")

        cursor.execute("""
            UPDATE Client
            SET account_status = %s
            WHERE client_id = %s
        """, (account_status, client_id))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Client not found"}), 404

        return jsonify({"message": "Client account updated"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get client risk profile
# [James-4], [James-7]
@advisors.route("/clients/<int:client_id>/risk-profile", methods=["GET"])
def get_risk_profile(client_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.client_id, c.name, c.email, c.account_status, c.risk_tolerance,
                   rp.risk_profile_id, rp.risk_level, rp.threshold_min, rp.threshold_max
            FROM Client c
            LEFT JOIN Risk_Profile rp ON rp.client_id = c.client_id
            WHERE c.client_id = %s
        """, (client_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Update risk tolerance thresholds
# [James-4]
@advisors.route("/clients/<int:client_id>/risk-profile", methods=["PUT"])
def update_risk_profile(client_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        required = ["risk_level", "threshold_min", "threshold_max"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor.execute("""
            UPDATE Risk_Profile
            SET risk_level = %s,
                threshold_min = %s,
                threshold_max = %s
            WHERE client_id = %s
        """, (data["risk_level"], data["threshold_min"], data["threshold_max"], client_id))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Risk profile not found"}), 404

        return jsonify({"message": "Risk profile updated"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Generate a performance report
# [James-2]
@advisors.route("/clients/<int:client_id>/reports", methods=["POST"])
def generate_report(client_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json(silent=True) or {}
        report_type = data.get("report_type", "monthly")
        summary = data.get("summary", f"Auto-generated {report_type} report for client {client_id}")

        cursor.execute("""
            INSERT INTO Report (client_id, report_type, summary)
            VALUES (%s, %s, %s)
        """, (client_id, report_type, summary))
        get_db().commit()
        return jsonify({"message": "Report generated", "report_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get rebalancing suggestions
# [James-3]
@advisors.route("/clients/<int:client_id>/rebalance", methods=["GET"])
def get_rebalancing_suggestions(client_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.portfolio_id, p.portfolio_name, a.asset_id, a.ticker, a.asset_name,
                   h.quantity, h.avg_cost, h.current_value, h.allocation_percent,
                   h.weight, rp.risk_level, rp.threshold_min, rp.threshold_max
            FROM Client c
            JOIN Portfolio p ON p.user_id = c.user_id
            JOIN Holding h ON h.portfolio_id = p.portfolio_id
            JOIN Asset a ON a.asset_id = h.asset_id
            LEFT JOIN Risk_Profile rp ON rp.client_id = c.client_id
            WHERE c.client_id = %s
            ORDER BY p.portfolio_id, h.allocation_percent DESC
        """, (client_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()