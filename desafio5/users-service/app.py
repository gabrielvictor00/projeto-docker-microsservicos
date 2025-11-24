from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {
        'id': 1,
        'nome': 'João Silva',
        'email': 'joao@example.com',
        'telefone': '(11) 98765-4321',
        'cidade': 'São Paulo',
        'status': 'ativo'
    },
    {
        'id': 2,
        'nome': 'Maria Santos',
        'email': 'maria@example.com',
        'telefone': '(21) 97654-3210',
        'cidade': 'Rio de Janeiro',
        'status': 'ativo'
    },
    {
        'id': 3,
        'nome': 'Pedro Oliveira',
        'email': 'pedro@example.com',
        'telefone': '(31) 96543-2109',
        'cidade': 'Belo Horizonte',
        'status': 'ativo'
    },
    {
        'id': 4,
        'nome': 'Ana Costa',
        'email': 'ana@example.com',
        'telefone': '(41) 95432-1098',
        'cidade': 'Curitiba',
        'status': 'inativo'
    },
    {
        'id': 5,
        'nome': 'Carlos Mendes',
        'email': 'carlos@example.com',
        'telefone': '(51) 94321-0987',
        'cidade': 'Porto Alegre',
        'status': 'ativo'
    }
]

@app.route('/')
def index():
    return jsonify({
        'service': 'Users Service',
        'version': '1.0.0',
        'endpoints': {
            '/': 'Informações do serviço',
            '/users': 'Lista todos os usuários',
            '/users/<id>': 'Detalhes de um usuário específico',
            '/health': 'Status do serviço'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'users-service'
    })

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({
        'total': len(USERS),
        'users': USERS
    })

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in USERS if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'Usuário não encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)


