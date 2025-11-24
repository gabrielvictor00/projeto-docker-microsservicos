# Desafio 4 - Microsserviços Independentes

## Descrição

Este desafio implementa uma arquitetura de microsserviços com dois serviços independentes que se comunicam via HTTP. O **Users Service** fornece dados de usuários através de uma API REST, enquanto o **Aggregator Service** consome essas informações e as enriquece com cálculos e formatações adicionais.

## Arquitetura

```
┌─────────────────────────────────────────────────┐
│         Microsserviços Independentes            │
│                                                 │
│  ┌──────────────────┐                          │
│  │  Users Service   │                          │
│  │  (Flask :8001)   │                          │
│  │                  │                          │
│  │  GET /users      │                          │
│  │  GET /users/:id  │                          │
│  └────────┬─────────┘                          │
│           │ HTTP Request                        │
│           │                                     │
│  ┌────────▼─────────┐                          │
│  │ Aggregator       │                          │
│  │ Service          │                          │
│  │ (Flask :8002)    │                          │
│  │                  │                          │
│  │ GET /users-      │                          │
│  │    summary       │                          │
│  └──────────────────┘                          │
│           │                                     │
│           └─────────────────────────────────────┘
│                    │                            │
│            ┌───────▼────────┐                   │
│            │ microservices- │                   │
│            │    network     │                   │
│            └────────────────┘                   │
└─────────────────────────────────────────────────┘
```

### Componentes

1. **Users Service**: Microsserviço que retorna lista de usuários em formato JSON
2. **Aggregator Service**: Microsserviço que consome o Users Service e exibe informações combinadas

## Decisões Técnicas

As escolhas técnicas para esta implementação foram:

- **Flask**: Utilizei Flask para ambos os serviços por ser simples e adequado para criar APIs REST. Permite implementar endpoints rapidamente sem complexidade desnecessária.
- **Python 3.11 Alpine**: Escolhi Python 3.11 com base Alpine para manter as imagens pequenas e eficientes. Python é ideal para este tipo de aplicação onde precisamos processar dados e fazer requisições HTTP.
- **Requests**: Usei a biblioteca `requests` para fazer as chamadas HTTP entre serviços. É a biblioteca mais popular e confiável para este propósito em Python, com uma API simples e intuitiva.
- **Dockerfiles Separados**: Cada serviço possui seu próprio Dockerfile para garantir isolamento completo. Isso permite que cada serviço tenha suas próprias dependências e seja construído independentemente, facilitando manutenção e escalabilidade.
- **Rede Docker**: Implementei comunicação via rede Docker interna, onde os serviços se encontram usando seus nomes (definidos no docker-compose.yml). Isso elimina a necessidade de conhecer IPs e facilita a descoberta de serviços.

## Funcionamento

### Users Service

Fornece endpoints REST para acessar dados de usuários:
- `GET /users`: Retorna lista completa de usuários
- `GET /users/<id>`: Retorna detalhes de um usuário específico
- `GET /health`: Status do serviço

### Aggregator Service

Consome o Users Service e enriquece os dados:
- Faz requisição HTTP para `http://users-service:8001/users`
- Calcula dias ativos para cada usuário
- Gera mensagens combinadas (ex: "Usuário X ativo desde...")
- Expõe endpoint `/users-summary` com informações enriquecidas

### Comunicação

Os serviços se comunicam através de uma rede Docker interna. O Aggregator Service usa o hostname `users-service` (nome do serviço no docker-compose) para acessar o Users Service.

## Instruções de Execução

### Pré-requisitos

- Docker instalado e rodando
- Docker Compose instalado

### Passo a Passo

1. **Navegue até a pasta do desafio:**
   ```bash
   cd desafio4
   ```

2. **Construa e inicie os serviços:**
   ```bash
   docker-compose up --build
   ```

   Para executar em background:
   ```bash
   docker-compose up -d --build
   ```

3. **Aguarde alguns segundos para os serviços iniciarem:**
   ```bash
   docker-compose ps
   ```

4. **Teste o Users Service diretamente:**

   **Informações do serviço:**
   ```bash
   curl http://localhost:8001/
   ```

   **Lista de usuários:**
   ```bash
   curl http://localhost:8001/users
   ```

   **Usuário específico:**
   ```bash
   curl http://localhost:8001/users/1
   ```

   **Health check:**
   ```bash
   curl http://localhost:8001/health
   ```

5. **Teste o Aggregator Service:**

   **Informações do serviço:**
   ```bash
   curl http://localhost:8002/
   ```

   **Resumo combinado (consome Users Service):**
   ```bash
   curl http://localhost:8002/users-summary
   ```

   **Health check (verifica conexão com Users Service):**
   ```bash
   curl http://localhost:8002/health
   ```

6. **Visualizar logs:**
   ```bash
   docker-compose logs -f
   ```

   Ou logs de um serviço específico:
   ```bash
   docker-compose logs -f users-service
   docker-compose logs -f aggregator-service
   ```

7. **Parar os serviços:**
   ```bash
   docker-compose down
   ```

## Endpoints

### Users Service (Porta 8001)

#### GET /

Retorna informações sobre o serviço.

```bash
curl http://localhost:8001/
```

#### GET /users

Retorna lista completa de usuários.

```bash
curl http://localhost:8001/users
```

Resposta:
```json
{
  "total": 5,
  "users": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@example.com",
      "ativo_desde": "2023-01-15",
      "status": "ativo"
    },
    ...
  ]
}
```

#### GET /users/:id

Retorna detalhes de um usuário específico.

```bash
curl http://localhost:8001/users/1
```

#### GET /health

Status do serviço.

```bash
curl http://localhost:8001/health
```

### Aggregator Service (Porta 8002)

#### GET /

Retorna informações sobre o serviço.

```bash
curl http://localhost:8002/
```

#### GET /users-summary

Consome o Users Service e retorna informações combinadas.

```bash
curl http://localhost:8002/users-summary
```

Resposta:
```json
{
  "total_users": 5,
  "source": "users-service",
  "summary": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@example.com",
      "status": "ativo",
      "mensagem": "Usuário João Silva está ativo desde 2023-01-15 (678 dias ativo)"
    },
    ...
  ],
  "generated_at": "2025-11-23T21:30:00"
}
```

#### GET /health

Status do serviço e conexão com Users Service.

```bash
curl http://localhost:8002/health
```

## Estrutura de Arquivos

```
desafio4/
├── users-service/
│   ├── Dockerfile          # Dockerfile do Users Service
│   ├── requirements.txt    # Dependências Python
│   └── app.py              # Aplicação Flask do Users Service
├── aggregator-service/
│   ├── Dockerfile          # Dockerfile do Aggregator Service
│   ├── requirements.txt    # Dependências Python
│   └── app.py              # Aplicação Flask do Aggregator Service
├── docker-compose.yml      # Orquestração dos microsserviços
└── README.md               # Este arquivo
```

## Explicação Detalhada

### Users Service (app.py)

O Users Service é uma aplicação Flask simples que mantém uma lista de usuários em memória (em uma variável `USERS`). Na prática, isso poderia ser substituído por um banco de dados, mas para este desafio, manter em memória é suficiente para demonstrar a comunicação entre serviços.

A aplicação expõe três endpoints principais:
- `GET /`: Retorna informações sobre o serviço e endpoints disponíveis
- `GET /users`: Retorna a lista completa de usuários em formato JSON
- `GET /users/<id>`: Retorna os detalhes de um usuário específico
- `GET /health`: Endpoint de health check que retorna o status do serviço

Cada usuário possui campos como id, nome, email, data de ativação e status. O serviço retorna os dados em formato JSON, que é facilmente consumível por outros serviços.

### Aggregator Service (app.py)

O Aggregator Service consome o Users Service e enriquece os dados. A função principal é `get_users_summary()`, que:

1. Faz uma requisição HTTP GET para `http://users-service:8001/users` usando a biblioteca `requests`
2. Processa a resposta JSON recebida
3. Para cada usuário, calcula quantos dias ele está ativo usando a função `calculate_days_active()`, que compara a data `ativo_desde` com a data atual
4. Gera uma mensagem combinada para cada usuário no formato "Usuário X está ativo desde Y (Z dias ativo)"
5. Retorna um JSON com o resumo enriquecido

O serviço também implementa tratamento de erros robusto: se o Users Service estiver offline ou não responder, o Aggregator retorna um erro HTTP 503 (Service Unavailable) com uma mensagem descritiva. O endpoint `/health` verifica a conectividade com o Users Service e reporta seu status.

### Dockerfiles Separados

Cada serviço possui seu próprio Dockerfile, garantindo:
- **Isolamento**: Dependências independentes
- **Portabilidade**: Cada serviço pode ser construído e executado separadamente
- **Escalabilidade**: Fácil escalar serviços individualmente

### docker-compose.yml

- Define dois serviços independentes
- Conecta ambos à mesma rede (`microservices-network`)
- Configura variável de ambiente `USERS_SERVICE_URL` no Aggregator
- Usa `depends_on` para garantir ordem de inicialização

### Comunicação via DNS Interno

O Docker fornece DNS interno que resolve nomes de serviços para IPs. Por isso:
- Aggregator acessa Users Service via `http://users-service:8001`
- Não é necessário conhecer IPs dos containers

## Testes e Validação

### Teste 1: Serviços Independentes

```bash
# Testar Users Service isoladamente
curl http://localhost:8001/users

# Testar Aggregator Service isoladamente (deve falhar se Users Service estiver offline)
curl http://localhost:8002/users-summary
```

### Teste 2: Comunicação entre Serviços

```bash
# Verificar que Aggregator consegue acessar Users
curl http://localhost:8002/health
# Deve mostrar: "users_service": "online"
```

### Teste 3: Resiliência

```bash
# Parar Users Service
docker-compose stop users-service

# Tentar acessar Aggregator
curl http://localhost:8002/users-summary
# Deve retornar erro 503

# Reiniciar Users Service
docker-compose start users-service

# Aguardar e testar novamente
sleep 2
curl http://localhost:8002/users-summary
# Deve funcionar novamente
```

### Teste 4: Logs de Comunicação

```bash
# Ver logs do Aggregator para observar requisições
docker-compose logs aggregator-service | grep -i "users-service"
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
# Acessar container do Users Service
docker exec -it desafio4-users sh

# Acessar container do Aggregator Service
docker exec -it desafio4-aggregator sh

# Testar comunicação de dentro do container
docker exec desafio4-aggregator wget -qO- http://users-service:8001/users
```

### Inspecionar Rede

```bash
docker network inspect desafio4-network
```

## Resultados Esperados

- ✅ Users Service acessível na porta 8001
- ✅ Aggregator Service acessível na porta 8002
- ✅ Aggregator consegue consumir Users Service
- ✅ Endpoints retornam dados corretos
- ✅ Health checks funcionam
- ✅ Logs mostram comunicação HTTP entre serviços

## Limpeza

Para remover tudo:

```bash
docker-compose down
docker network prune -f
```

## Conclusão

Através deste desafio, pude implementar e entender na prática os conceitos fundamentais de arquitetura de microsserviços. A solução demonstra como serviços independentes podem trabalhar juntos mantendo desacoplamento e responsabilidades bem definidas. Cada serviço tem sua responsabilidade única, se comunicam via HTTP/REST, estão isolados em containers separados e se descobrem através da rede Docker interna. Esta arquitetura facilita escalabilidade e manutenção, permitindo que cada serviço evolua independentemente.


