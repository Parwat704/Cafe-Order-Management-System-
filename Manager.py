from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Cafe orders 
orders = {}

@app.route('/')
def home():
    return render_template("index.html", orders=orders)

@app.route('/order', methods=['POST'])
def receive_order():
    data = request.get_json()
    order_id = len(orders) + 1
    order_details = {
        'id': order_id,
        'items': data['items'],
        'total': data['total'],
        'status': 'Order Received',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    orders[order_id] = order_details
    return jsonify({"message": "Order received!", "order_id": order_id}), 200

@app.route('/order/<int:order_id>', methods=['GET'])
def view_order(order_id):
    if order_id in orders:
        return jsonify(orders[order_id]), 200
    return jsonify({"error": "Order not found!"}), 404

@app.route('/update_status/<int:order_id>', methods=['POST'])
def update_status(order_id):
    if order_id in orders:
        new_status = request.json.get('status')
        orders[order_id]['status'] = new_status
        return jsonify({"message": "Status updated!"}), 200
    return jsonify({"error": "Order not found!"}), 404

@app.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    if order_id in orders:
        orders[order_id]['status'] = 'Cancelled'
        return jsonify({"message": "Order cancelled!"}), 200
    return jsonify({"error": "Order not found!"}), 404

# HTML Templates for Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)
