from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

investors = Blueprint("investors", __name__)


# Get all holdings in a portfolio
# [Mike-1], [Mike-3]
@investors.route("/portfolios/<int:portfolio_id>/holdings", methods=["GET"])
def get_holdings(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT a.ticker, a.asset_name, h.quantity, h.avg_cost,
                   a.current_price, h.current_value, h.allocation_percent,
                   (a.current_price - h.avg_cost) AS price_change,
                   ROUND(((a.current_price - h.avg_cost) / h.avg_cost * 100), 2) AS pct_return
            FROM Holding h
            JOIN Asset a ON h.asset_id = a.asset_id
            WHERE h.portfolio_id = %s
            ORDER BY pct_return DESC
        """, (portfolio_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Add a new holding
# [Mike-4]
@investors.route("/portfolios/<int:portfolio_id>/holdings", methods=["POST"])
def add_holding(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        required = ["asset_id", "quantity", "avg_cost"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Look up current price to calculate current_value
        cursor.execute("SELECT current_price FROM Asset WHERE asset_id = %s", (data["asset_id"],))
        asset = cursor.fetchone()
        if not asset:
            return jsonify({"error": "Asset not found"}), 404

        current_value = round(float(data["quantity"]) * float(asset["current_price"]), 2)

        cursor.execute("""
            INSERT INTO Holding (portfolio_id, asset_id, quantity, avg_cost,
                                 current_value, allocation_percent, weight)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (portfolio_id, data["asset_id"], data["quantity"], data["avg_cost"],
              current_value, data.get("allocation_percent", 0),
              data.get("weight", 0)))
        get_db().commit()
        return jsonify({"message": "Holding added", "holding_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Update holding quantity/cost
# [Mike-5]
@investors.route("/holdings/<int:portfolio_id>/<int:asset_id>", methods=["PUT"])
def update_holding(portfolio_id, asset_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        cursor.execute("""
            UPDATE Holding
            SET quantity = %s, avg_cost = %s, current_value = %s,
                allocation_percent = %s
            WHERE portfolio_id = %s AND asset_id = %s
        """, (data.get("quantity"), data.get("avg_cost"),
              data.get("current_value"), data.get("allocation_percent"),
              portfolio_id, asset_id))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Holding not found"}), 404

        return jsonify({"message": "Holding updated"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Remove a holding
# [Mike-6]
@investors.route("/holdings/<int:portfolio_id>/<int:asset_id>", methods=["DELETE"])
def remove_holding(portfolio_id, asset_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            DELETE FROM Holding
            WHERE portfolio_id = %s AND asset_id = %s
        """, (portfolio_id, asset_id))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Holding not found"}), 404

        return jsonify({"message": "Holding removed"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get portfolio performance over time
# [Mike-2]
@investors.route("/portfolios/<int:portfolio_id>/performance", methods=["GET"])
def get_performance(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT date, portfolio_value, gain_loss
            FROM Performance_History
            WHERE portfolio_id = %s
            ORDER BY date
        """, (portfolio_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()