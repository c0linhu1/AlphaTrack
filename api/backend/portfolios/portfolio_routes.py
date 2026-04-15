from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

portfolios = Blueprint("portfolios", __name__)


# Get all portfolios for a user
# [Bobby-1], [Bobby-2], [Mike-1]
@portfolios.route("/portfolios/<int:user_id>", methods=["GET"])
def get_user_portfolios(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.*, b.benchmark_name
            FROM Portfolio p
            LEFT JOIN Benchmark b ON p.benchmark_id = b.benchmark_id
            WHERE p.user_id = %s
        """, (user_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get risk metrics for a portfolio
# [Bobby-1], [Bobby-6]
@portfolios.route("/portfolios/<int:portfolio_id>/risk-metrics", methods=["GET"])
def get_risk_metrics(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.portfolio_name, rm.*, b.benchmark_name
            FROM Risk_Metrics rm
            JOIN Portfolio p ON rm.portfolio_id = p.portfolio_id
            LEFT JOIN Benchmark b ON p.benchmark_id = b.benchmark_id
            WHERE rm.portfolio_id = %s
        """, (portfolio_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Update date range for risk metrics
# [Bobby-4]
@portfolios.route("/portfolios/<int:portfolio_id>/risk-metrics", methods=["PUT"])
def update_risk_metrics(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        required = ["metric_id", "date_range_start", "date_range_end"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor.execute("""
            UPDATE Risk_Metrics
            SET date_range_start = %s, date_range_end = %s
            WHERE portfolio_id = %s AND metric_id = %s
        """, (data["date_range_start"], data["date_range_end"],
              portfolio_id, data["metric_id"]))
        get_db().commit()
        return jsonify({"message": "Risk metrics updated"}), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get portfolio vs benchmark performance
# [Bobby-2]
@portfolios.route("/portfolios/<int:portfolio_id>/benchmark", methods=["GET"])
def get_benchmark_comparison(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT ph.date, ph.closing_price AS asset_price,
                   bph.closing_price AS benchmark_price
            FROM Price_History ph
            JOIN Holding h ON ph.asset_id = h.asset_id
            JOIN Portfolio p ON h.portfolio_id = p.portfolio_id
            JOIN Benchmark_Price_History bph ON bph.benchmark_id = p.benchmark_id
                AND bph.date = ph.date
            WHERE p.portfolio_id = %s
            ORDER BY ph.date
        """, (portfolio_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get correlation matrix data for portfolio holdings
# [Bobby-3]
@portfolios.route("/portfolios/<int:portfolio_id>/correlation", methods=["GET"])
def get_correlation_data(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT a.ticker, ph.date, ph.closing_price
            FROM Price_History ph
            JOIN Asset a ON ph.asset_id = a.asset_id
            JOIN Holding h ON h.asset_id = a.asset_id
            WHERE h.portfolio_id = %s
            ORDER BY a.ticker, ph.date
        """, (portfolio_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get all watchlists for a user
# [Bobby-5]
@portfolios.route("/watchlists/<int:user_id>", methods=["GET"])
def get_watchlists(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT w.*, GROUP_CONCAT(a.ticker) AS tickers
            FROM Watchlist w
            LEFT JOIN Watchlist_Asset wa ON w.watchlist_id = wa.watchlist_id
            LEFT JOIN Asset a ON wa.asset_id = a.asset_id
            WHERE w.user_id = %s
            GROUP BY w.watchlist_id
        """, (user_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Create a new watchlist
# [Bobby-5]
@portfolios.route("/watchlists/<int:user_id>", methods=["POST"])
def create_watchlist(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if "watchlist_name" not in data:
            return jsonify({"error": "Missing watchlist_name"}), 400

        cursor.execute("""
            INSERT INTO Watchlist (user_id, watchlist_name)
            VALUES (%s, %s)
        """, (user_id, data["watchlist_name"]))
        get_db().commit()
        return jsonify({"message": "Watchlist created", "watchlist_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()