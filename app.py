from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, headers=["Content-Type", "X-API-Key"])

API_KEY = "ak_6havt15wfdx5y0ry2qt9ephg"
EMAIL = "your_logged_in_email@example.com"  # Replace this!

@app.route("/analytics", methods=["POST"])
def analytics():
    api_key = request.headers.get("X-API-Key")

    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("events"), list):
        return jsonify({"error": "Body must contain an events array"}), 400

    events = data["events"]

    users = set()
    positive_totals = {}
    revenue = 0.0

    for event in events:
        user = event.get("user")
        amount = event.get("amount", 0)

        if user is not None:
            users.add(user)

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            amount = 0

        if amount > 0:
            revenue += amount
            positive_totals[user] = positive_totals.get(user, 0) + amount

    top_user = None
    highest_total = float("-inf")

    for user, total in positive_totals.items():
        if total > highest_total:
            highest_total = total
            top_user = user

    return jsonify({
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user
    })
