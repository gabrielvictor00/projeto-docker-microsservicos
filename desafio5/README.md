# Desafio 5 - Microsserviços com API Gateway

## Descrição

Este desafio implementa uma arquitetura completa de microsserviços com API Gateway. O Gateway atua como ponto único de entrada, orquestrando chamadas para dois microsserviços: **Users Service** (dados de usuários) e **Orders Service** (dados de pedidos).

## Arquitetura

```
┌─────────────────────────────────────────────────┐
│           Arquitetura com API Gateway            │
│                                                 │
│              ┌──────────────┐                   │
│              │ API Gateway  │                   │
│              │   :8080      │                   │
│              │  (Ponto de  │                   │
│              │   Entrada)   │                   │
│              └──────┬───────┘                   │
│                     │                            │
│         ┌───────────┴───────────┐               │
│         │                       │               │
│  ┌──────▼──────┐      ┌────────▼──────┐        │
│  │ Users       │      │ Orders        │        │
│  │ Service     │      │ Service       │        │
│  │ :8001       │      │ :8002         │        │
│  └─────────────┘      └───────────────┘        │
│         │                       │               │
│         └───────────┬───────────┘               │
│                     │                            │
│            ┌────────▼────────┐                   │
│            │ microservices-  │                   │
│            │    network      │                   │
│            └─────────────────┘                   │
└─────────────────────────────────────────────────┘
```

### Componentes

1. **API Gateway**: Ponto único de entrada que roteia requisições para os microsserviços
2. **Users Service**: Microsserviço que fornece dados de usuários
3. **Orders Service**: Microsserviço que fornece dados de pedidos

## Decisões Técnicas

- **API Gateway Pattern**: Centraliza acesso e simplifica comunicação cliente-serviços
- **Flask**: Framework leve para todos os serviços
- **Proxy Pattern**: Gateway faz proxy das requisições para os serviços backend
- **Health Checks**: Garantem que serviços estejam prontos antes do Gateway iniciar
- **Rede Interna**: Microsserviços não expostos externamente, apenas Gateway
- **Tratamento de Erros**: Gateway trata timeouts e falhas de comunicação

## Funcionamento

### Fluxo de Requisições

1. **Cliente faz requisição** para o Gateway na porta 8080
2. **Gateway identifica** o endpoint (`/users` ou `/orders`)
3. **Gateway faz proxy** da requisição para o serviço apropriado
4. **Serviço processa** e retorna resposta
5. **Gateway retorna** resposta ao cliente

### Roteamento

- `/users` → Users Service (`http://users-service:8001/users`)
- `/users/<id>` → Users Service (`http://users-service:8001/users/<id>`)
- `/orders` → Orders Service (`http://orders-service:8002/orders`)
- `/orders/<id>` → Orders Service (`http://orders-service:8002/orders/<id>`)
- `/orders/user/<user_id>` → Orders Service (`http://orders-service:8002/orders/user/<user_id>`)

### Isolamento

- Microsserviços **não são expostos** externamente (sem portas mapeadas)
- Apenas o Gateway é acessível do host (porta 8080)
- Comunicação interna via rede Docker

## Instruções de Execução

### Pré-requisitos

- Docker instalado e rodando
- Docker Compose instalado

### Passo a Passo

1. **Navegue até a pasta do desafio:**
   ```bash
   cd desafio5
   ```

2. **Construa e inicie todos os serviços:**
   ```bash
   docker-compose up --build
   ```

   Para executar em background:
   ```bash
   docker-compose up -d --build
   ```

3. **Aguarde alguns segundos para todos os serviços iniciarem:**
   ```bash
   docker-compose ps
   ```

4. **Teste o Gateway:**

   **Informações do Gateway:**
   ```bash
   curl http://localhost:8080/
   ```

   **Health Check (status de todos os serviços):**
   ```bash
   curl http://localhost:8080/health
   ```

   **Listar usuários (via Gateway):**
   ```bash
   curl http://localhost:8080/users
   ```

   **Detalhes de um usuário:**
   ```bash
   curl http://localhost:8080/users/1
   ```

   **Listar pedidos (via Gateway):**
   ```bash
   curl http://localhost:8080/orders
   ```

   **Detalhes de um pedido:**
   ```bash
   curl http://localhost:8080/orders/1
   ```

   **Pedidos de um usuário:**
   ```bash
   curl http://localhost:8080/orders/user/1
   ```

5. **Visualizar logs:**
   ```bash
   docker-compose logs -f
   ```

   Ou logs de um serviço específico:
   ```bash
   docker-compose logs -f gateway
   docker-compose logs -f users-service
   docker-compose logs -f orders-service
   ```

6. **Parar os serviços:**
   ```bash
   docker-compose down
   ```

## Endpoints do Gateway (Porta 8080)

### GET /

Retorna informações sobre o Gateway e endpoints disponíveis.

```bash
curl http://localhost:8080/
```

### GET /health

Verifica status do Gateway e de todos os microsserviços.

```bash
curl http://localhost:8080/health
```

Resposta:
```json
{
  "gateway": "online",
  "users_service": "online",
  "orders_service": "online"
}
```

### GET /users

Lista todos os usuários (proxied para Users Service).

```bash
curl http://localhost:8080/users
```

### GET /users/:id

Detalhes de um usuário específico (proxied para Users Service).

```bash
curl http://localhost:8080/users/1
```

### GET /orders

Lista todos os pedidos (proxied para Orders Service).

```bash
curl http://localhost:8080/orders
```

### GET /orders/:id

Detalhes de um pedido específico (proxied para Orders Service).

```bash
curl http://localhost:8080/orders/1
```

### GET /orders/user/:user_id

Pedidos de um usuário específico (proxied para Orders Service).

```bash
curl http://localhost:8080/orders/user/1
```

## Estrutura de Arquivos

```
desafio5/
├── users-service/
│   ├── Dockerfile          # Dockerfile do Users Service
│   ├── requirements.txt    # Dependências Python
│   └── app.py              # Aplicação Flask do Users Service
├── orders-service/
│   ├── Dockerfile          # Dockerfile do Orders Service
│   ├── requirements.txt    # Dependências Python
│   └── app.py              # Aplicação Flask do Orders Service
├── gateway/
│   ├── Dockerfile          # Dockerfile do API Gateway
│   ├── requirements.txt    # Dependências Python
│   └── app.py              # Aplicação Flask do Gateway
├── docker-compose.yml      # Orquestração completa
└── README.md                # Este arquivo
```

## Explicação Detalhada

### API Gateway (app.py)

O Gateway implementa o padrão de proxy reverso:

- **Roteamento**: Identifica qual serviço deve processar cada requisição
- **Proxy**: Encaminha requisições HTTP para os serviços backend
- **Tratamento de Erros**: Captura timeouts e erros de conexão
- **Health Check**: Verifica status de todos os serviços

#### Função `proxy_request`

```python
def proxy_request(service_url, path, method='GET', timeout=5):
    # Faz requisição para o serviço backend
    # Trata timeouts e erros de conexão
    # Retorna resposta e status code
```

### Users Service

Fornece dados de usuários:
- Lista de usuários com informações completas
- Detalhes de usuário específico
- Health check endpoint

### Orders Service

Fornece dados de pedidos:
- Lista de pedidos
- Detalhes de pedido específico
- Pedidos filtrados por usuário
- Health check endpoint

### docker-compose.yml

#### Isolamento de Serviços

- **Users e Orders Services**: Não têm portas expostas (`ports` não definido)
- **Gateway**: Única porta exposta (8080)
- **Health Checks**: Garantem que serviços estejam prontos antes do Gateway iniciar

#### Dependências

```yaml
depends_on:
  users-service:
    condition: service_healthy
  orders-service:
    condition: service_healthy
```

Isso garante que o Gateway só inicie após ambos os serviços estarem saudáveis.

### Rede Interna

Todos os serviços estão na mesma rede (`microservices-network`), mas apenas o Gateway é acessível externamente. Isso proporciona:
- **Segurança**: Microsserviços não expostos
- **Isolamento**: Comunicação apenas via Gateway
- **Controle**: Gateway pode implementar autenticação, rate limiting, etc.

## Testes e Validação

### Teste 1: Gateway como Ponto Único de Entrada

```bash
# Acessar usuários via Gateway
curl http://localhost:8080/users

# Acessar pedidos via Gateway
curl http://localhost:8080/orders

# Verificar que serviços não são acessíveis diretamente
curl http://localhost:8001/users
# Deve falhar (porta não exposta)
```

### Teste 2: Health Check

```bash
curl http://localhost:8080/health
```

Todos os serviços devem estar "online".

### Teste 3: Roteamento Correto

```bash
# Gateway deve rotear corretamente
curl http://localhost:8080/users/1
curl http://localhost:8080/orders/1
curl http://localhost:8080/orders/user/1
```

### Teste 4: Tratamento de Erros

```bash
# Parar um serviço
docker-compose stop users-service

# Tentar acessar via Gateway
curl http://localhost:8080/users
# Deve retornar erro 503

# Verificar health
curl http://localhost:8080/health
# Deve mostrar users_service como "offline"
```

### Teste 5: Logs de Proxy

```bash
# Ver logs do Gateway para observar requisições proxy
docker-compose logs gateway | grep -i "proxy\|request"
```

## Comandos Úteis

### Gerenciamento

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Reconstruir imagens
docker-compose build --no-cache

# Ver status
docker-compose ps

# Ver logs
docker-compose logs -f [servico]
```

### Acesso aos Containers

```bash
# Acessar Gateway
docker exec -it desafio5-gateway sh

# Acessar Users Service
docker exec -it desafio5-users sh

# Acessar Orders Service
docker exec -it desafio5-orders sh

# Testar comunicação interna
docker exec desafio5-gateway wget -qO- http://users-service:8001/users
```

### Inspecionar Rede

```bash
docker network inspect desafio5-network
```

### Verificar Portas Expostas

```bash
# Gateway deve ter porta 8080 exposta
docker-compose ps

# Serviços não devem ter portas expostas
docker port desafio5-users
docker port desafio5-orders
```

## Vantagens do API Gateway

1. **Ponto Único de Entrada**: Cliente não precisa conhecer múltiplos endpoints
2. **Segurança**: Microsserviços não expostos externamente
3. **Orquestração**: Gateway pode combinar respostas de múltiplos serviços
4. **Autenticação**: Pode centralizar autenticação/autorização
5. **Rate Limiting**: Pode limitar requisições por cliente
6. **Logging**: Centraliza logs de todas as requisições
7. **Versionamento**: Pode gerenciar versões de API

## Resultados Esperados

- ✅ Gateway acessível na porta 8080
- ✅ Gateway roteia corretamente para Users e Orders Services
- ✅ Health check mostra status de todos os serviços
- ✅ Microsserviços não acessíveis externamente
- ✅ Tratamento de erros funciona (serviço offline retorna 503)
- ✅ Logs mostram requisições proxy do Gateway

## Limpeza

Para remover tudo:

```bash
docker-compose down
docker network prune -f
```

## Conclusão

Este desafio demonstra uma arquitetura completa de microsserviços com API Gateway, onde:

- **Gateway** atua como ponto único de entrada
- **Microsserviços** são isolados e não expostos externamente
- **Comunicação** acontece via rede Docker interna
- **Orquestração** é gerenciada pelo Docker Compose
- **Health Checks** garantem disponibilidade dos serviços

A arquitetura resultante é segura, escalável e fácil de gerenciar, seguindo boas práticas de microsserviços.


