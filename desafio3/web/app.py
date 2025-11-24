from flask import Flask, jsonify
import psycopg2
import redis
import os

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'desafio3_db')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'senha123')

REDIS_HOST = os.getenv('REDIS_HOST', 'cache')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def get_redis_connection():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route('/')
def index():
    return jsonify({
        'message': 'API Desafio 3 - Docker Compose',
        'endpoints': {
            '/': 'Esta página',
            '/health': 'Status dos serviços',
            '/users': 'Lista de usuários (com cache)',
            '/products': 'Lista de produtos (com cache)',
            '/cache/stats': 'Estatísticas do cache'
        }
    })

@app.route('/health')
def health():
    status = {
        'web': 'online',
        'database': 'unknown',
        'cache': 'unknown'
    }
    
    try:
        conn = get_db_connection()
        conn.close()
        status['database'] = 'online'
    except Exception as e:
        status['database'] = f'offline: {str(e)}'
    
    try:
        r = get_redis_connection()
        r.ping()
        status['cache'] = 'online'
    except Exception as e:
        status['cache'] = f'offline: {str(e)}'
    
    return jsonify(status)

@app.route('/users')
def get_users():
    cache_key = 'users_list'
    r = get_redis_connection()
    
    cached = r.get(cache_key)
    if cached:
        return jsonify({
            'source': 'cache',
            'data': eval(cached)
        })
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, nome, email FROM usuarios ORDER BY id')
        users = cur.fetchall()
        cur.close()
        conn.close()
        
        result = [{'id': u[0], 'nome': u[1], 'email': u[2]} for u in users]
        
        r.setex(cache_key, 30, str(result))
        
        return jsonify({
            'source': 'database',
            'data': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products')
def get_products():
    cache_key = 'products_list'
    r = get_redis_connection()
    
    cached = r.get(cache_key)
    if cached:
        return jsonify({
            'source': 'cache',
            'data': eval(cached)
        })
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, nome, preco, estoque FROM produtos ORDER BY id')
        products = cur.fetchall()
        cur.close()
        conn.close()
        
        result = [{'id': p[0], 'nome': p[1], 'preco': float(p[2]), 'estoque': p[3]} for p in products]
        
        r.setex(cache_key, 30, str(result))
        
        return jsonify({
            'source': 'database',
            'data': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cache/stats')
def cache_stats():
    try:
        r = get_redis_connection()
        info = r.info()
        return jsonify({
            'connected_clients': info.get('connected_clients', 0),
            'used_memory_human': info.get('used_memory_human', '0B'),
            'total_keys': r.dbsize(),
            'keys': {
                'users_list': r.exists('users_list'),
                'products_list': r.exists('products_list')
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


