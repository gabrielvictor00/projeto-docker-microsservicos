from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

ORDERS = [
    {
        'id': 1,
        'user_id': 1,
        'produto': 'Notebook Dell',
        'quantidade': 1,
        'valor': 3500.00,
        'status': 'entregue',
        'data_pedido': '2025-11-15',
        'data_entrega': '2025-11-18'
    },
    {
        'id': 2,
        'user_id': 1,
        'produto': 'Mouse Logitech',
        'quantidade': 2,
        'valor': 100.00,
        'status': 'em_transito',
        'data_pedido': '2025-11-20',
        'data_entrega': None
    },
    {
        'id': 3,
        'user_id': 2,
        'produto': 'Teclado Mecânico',
        'quantidade': 1,
        'valor': 450.00,
        'status': 'processando',
        'data_pedido': '2025-11-22',
        'data_entrega': None
    },
    {
        'id': 4,
        'user_id': 3,
        'produto': 'Monitor LG',
        'quantidade': 1,
        'valor': 1200.00,
        'status': 'entregue',
        'data_pedido': '2025-11-10',
        'data_entrega': '2025-11-12'
    },
    {
        'id': 5,
        'user_id': 5,
        'produto': 'Webcam HD',
        'quantidade': 1,
        'valor': 250.00,
        'status': 'cancelado',
        'data_pedido': '2025-11-18',
        'data_entrega': None
    }
]

@app.route('/')
def index():
    return jsonify({
        'service': 'Orders Service',
        'version': '1.0.0',
        'endpoints': {
            '/': 'Informações do serviço',
            '/orders': 'Lista todos os pedidos',
            '/orders/<id>': 'Detalhes de um pedido específico',
            '/orders/user/<user_id>': 'Pedidos de um usuário',
            '/health': 'Status do serviço'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'orders-service'
    })

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({
        'total': len(ORDERS),
        'orders': ORDERS
    })

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in ORDERS if o['id'] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Pedido não encontrado'}), 404

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    user_orders = [o for o in ORDERS if o['user_id'] == user_id]
    return jsonify({
        'user_id': user_id,
        'total': len(user_orders),
        'orders': user_orders
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)


