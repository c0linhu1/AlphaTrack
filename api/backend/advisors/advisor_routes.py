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
        data = request.get_json(silent=True) or {}
        required = ["benchmark_id", "portfolio_name", "total_value"]

        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Make sure the advisor/user exists
        cursor.execute("SELECT user_id FROM User WHERE user_id = %s", (user_id,))
        user_exists = cursor.fetchone()
        if not user_exists:
            return jsonify({"error": "User not found"}), 404

        # Make sure the benchmark exists
        cursor.execute("SELECT benchmark_id FROM Benchmark WHERE benchmark_id = %s", (data["benchmark_id"],))
        benchmark_exists = cursor.fetchone()
        if not benchmark_exists:
            return jsonify({"error": "Benchmark not found"}), 404

        # Validate portfolio name
        portfolio_name = str(data["portfolio_name"]).strip()
        if not portfolio_name:
            return jsonify({"error": "portfolio_name cannot be empty"}), 400

        # Validate total value
        try:
            total_value = float(data["total_value"])
        except (TypeError, ValueError):
            return jsonify({"error": "total_value must be a number"}), 400

        if total_value < 0:
            return jsonify({"error": "total_value cannot be negative"}), 400

        cursor.execute("""
            INSERT INTO Portfolio (user_id, benchmark_id, portfolio_name, total_value)
            VALUES (%s, %s, %s, %s)
        """, (user_id, data["benchmark_id"], portfolio_name, total_value))
        get_db().commit()

        return jsonify({
            "message": "Client portfolio created",
            "portfolio_id": cursor.lastrowid
        }), 201

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

        # Only allow supported account statuses
        allowed_statuses = {"active", "closed"}
        if account_status not in allowed_statuses:
            return jsonify({"error": f"account_status must be one of: {', '.join(sorted(allowed_statuses))}"}), 400

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
        data = request.get_json(silent=True) or {}
        required = ["risk_level", "threshold_min", "threshold_max"]

        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        allowed_risk_levels = {"conservative", "moderate", "aggressive"}
        if data["risk_level"] not in allowed_risk_levels:
            return jsonify({
                "error": f"risk_level must be one of: {', '.join(sorted(allowed_risk_levels))}"
            }), 400

        try:
            threshold_min = float(data["threshold_min"])
            threshold_max = float(data["threshold_max"])
        except (TypeError, ValueError):
            return jsonify({"error": "threshold_min and threshold_max must be numeric"}), 400

        if threshold_min < 0 or threshold_max < 0:
            return jsonify({"error": "Thresholds must be non-negative"}), 400

        if threshold_min > threshold_max:
            return jsonify({"error": "threshold_min cannot be greater than threshold_max"}), 400

        cursor.execute("""
            UPDATE Risk_Profile
            SET risk_level = %s,
                threshold_min = %s,
                threshold_max = %s
            WHERE client_id = %s
        """, (data["risk_level"], threshold_min, threshold_max, client_id))
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

        # Make sure the client exists
        cursor.execute("SELECT client_id FROM Client WHERE client_id = %s", (client_id,))
        client_exists = cursor.fetchone()
        if not client_exists:
            return jsonify({"error": "Client not found"}), 404

        report_type = data.get("report_type", "monthly")
        allowed_report_types = {"monthly", "quarterly", "annual"}

        if report_type not in allowed_report_types:
            return jsonify({
                "error": f"report_type must be one of: {', '.join(sorted(allowed_report_types))}"
            }), 400

        summary = data.get(
            "summary",
            f"Auto-generated {report_type} report for client {client_id}"
        )

        cursor.execute("""
            INSERT INTO Report (client_id, report_type, summary)
            VALUES (%s, %s, %s)
        """, (client_id, report_type, summary))
        get_db().commit()

        return jsonify({
            "message": "Report generated",
            "report_id": cursor.lastrowid
        }), 201

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
        # First, make sure the client exists
        cursor.execute("SELECT client_id FROM Client WHERE client_id = %s", (client_id,))
        client_exists = cursor.fetchone()

        if not client_exists:
            return jsonify({"error": "Client not found"}), 404

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

        # Add a simple computed flag without changing existing fields
        for row in results:
            try:
                alloc = float(row["allocation_percent"]) if row["allocation_percent"] is not None else None
                threshold_max = float(row["threshold_max"]) if row["threshold_max"] is not None else None

                if alloc is not None and threshold_max is not None:
                    row["exceeds_threshold"] = alloc > (threshold_max * 100)
                else:
                    row["exceeds_threshold"] = None
            except (TypeError, ValueError):
                row["exceeds_threshold"] = None

        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()