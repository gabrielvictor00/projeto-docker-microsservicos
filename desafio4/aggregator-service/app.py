from flask import Flask, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

USERS_SERVICE_URL = os.getenv('USERS_SERVICE_URL', 'http://users-service:8001')

def calculate_days_active(ativo_desde):
    try:
        from_date = datetime.strptime(ativo_desde, '%Y-%m-%d')
        today = datetime.now()
        days = (today - from_date).days
        return days
    except:
        return 0

@app.route('/')
def index():
    return jsonify({
        'service': 'Aggregator Service',
        'version': '1.0.0',
        'description': 'Consome o Users Service e exibe informações combinadas',
        'endpoints': {
            '/': 'Informações do serviço',
            '/users-summary': 'Resumo combinado dos usuários',
            '/health': 'Status do serviço'
        }
    })

@app.route('/health')
def health():
    users_service_status = 'unknown'
    try:
        response = requests.get(f'{USERS_SERVICE_URL}/health', timeout=2)
        if response.status_code == 200:
            users_service_status = 'online'
        else:
            users_service_status = 'offline'
    except:
        users_service_status = 'offline'
    
    return jsonify({
        'status': 'healthy',
        'service': 'aggregator-service',
        'users_service': users_service_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/users-summary', methods=['GET'])
def get_users_summary():
    try:
        response = requests.get(f'{USERS_SERVICE_URL}/users', timeout=5)
        response.raise_for_status()
        data = response.json()
        
        users = data.get('users', [])
        
        summary = []
        for user in users:
            days_active = calculate_days_active(user.get('ativo_desde', ''))
            
            summary_item = {
                'id': user.get('id'),
                'nome': user.get('nome'),
                'email': user.get('email'),
                'status': user.get('status'),
                'mensagem': f"Usuário {user.get('nome')} está {user.get('status')} desde {user.get('ativo_desde')} ({days_active} dias ativo)"
            }
            summary.append(summary_item)
        
        return jsonify({
            'total_users': len(summary),
            'source': 'users-service',
            'summary': summary,
            'generated_at': datetime.now().isoformat()
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Erro ao comunicar com o Users Service',
            'details': str(e),
            'users_service_url': USERS_SERVICE_URL
        }), 503
    except Exception as e:
        return jsonify({
            'error': 'Erro interno',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)


