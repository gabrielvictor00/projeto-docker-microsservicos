from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

USERS_SERVICE_URL = os.getenv('USERS_SERVICE_URL', 'http://users-service:8001')
ORDERS_SERVICE_URL = os.getenv('ORDERS_SERVICE_URL', 'http://orders-service:8002')

def proxy_request(service_url, path, method='GET', timeout=5):
    try:
        url = f"{service_url}{path}"
        if method == 'GET':
            response = requests.get(url, timeout=timeout, params=request.args)
        else:
            response = requests.request(method, url, timeout=timeout, json=request.json)
        return response.json(), response.status_code
    except requests.exceptions.Timeout:
        return {'error': 'Service timeout'}, 504
    except requests.exceptions.ConnectionError:
        return {'error': 'Service unavailable'}, 503
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/')
def index():
    return jsonify({
        'service': 'API Gateway',
        'version': '1.0.0',
        'description': 'Gateway centralizando acesso aos microsserviços',
        'endpoints': {
            '/': 'Informações do gateway',
            '/health': 'Status do gateway e serviços',
            '/users': 'Lista de usuários (proxied to users-service)',
            '/users/<id>': 'Detalhes de usuário (proxied to users-service)',
            '/orders': 'Lista de pedidos (proxied to orders-service)',
            '/orders/<id>': 'Detalhes de pedido (proxied to orders-service)',
            '/orders/user/<user_id>': 'Pedidos de um usuário (proxied to orders-service)'
        }
    })

@app.route('/health')
def health():
    services_status = {
        'gateway': 'online',
        'users_service': 'unknown',
        'orders_service': 'unknown'
    }
    
    try:
        response = requests.get(f'{USERS_SERVICE_URL}/health', timeout=2)
        if response.status_code == 200:
            services_status['users_service'] = 'online'
        else:
            services_status['users_service'] = 'offline'
    except:
        services_status['users_service'] = 'offline'
    
    try:
        response = requests.get(f'{ORDERS_SERVICE_URL}/health', timeout=2)
        if response.status_code == 200:
            services_status['orders_service'] = 'online'
        else:
            services_status['orders_service'] = 'offline'
    except:
        services_status['orders_service'] = 'offline'
    
    return jsonify(services_status)

@app.route('/users', methods=['GET'])
def get_users():
    data, status_code = proxy_request(USERS_SERVICE_URL, '/users')
    return jsonify(data), status_code

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    data, status_code = proxy_request(USERS_SERVICE_URL, f'/users/{user_id}')
    return jsonify(data), status_code

@app.route('/orders', methods=['GET'])
def get_orders():
    data, status_code = proxy_request(ORDERS_SERVICE_URL, '/orders')
    return jsonify(data), status_code

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    data, status_code = proxy_request(ORDERS_SERVICE_URL, f'/orders/{order_id}')
    return jsonify(data), status_code

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    data, status_code = proxy_request(ORDERS_SERVICE_URL, f'/orders/user/{user_id}')
    return jsonify(data), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


