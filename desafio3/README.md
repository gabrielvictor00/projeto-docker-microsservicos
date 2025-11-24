# Desafio 3 - Docker Compose Orquestrando Serviços

## Descrição

Este desafio demonstra a orquestração de múltiplos serviços usando Docker Compose. A aplicação consiste em três serviços interdependentes: uma aplicação web Flask, um banco de dados PostgreSQL e um cache Redis.

## Arquitetura

```
┌─────────────────────────────────────────────────┐
│              Docker Compose                     │
│                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │   Web    │───▶│    DB    │    │  Cache   │ │
│  │ (Flask)  │    │(Postgres)│    │ (Redis)  │ │
│  │  :5000   │    │  :5432   │    │  :6379   │ │
│  └──────────┘    └──────────┘    └──────────┘ │
│       │                │                │       │
│       └────────────────┴────────────────┘       │
│                    │                             │
│            ┌───────▼────────┐                    │
│            │  app-network   │                    │
│            │   (bridge)     │                    │
│            └────────────────┘                    │
└─────────────────────────────────────────────────┘
```

### Componentes

1. **Web Service (Flask)**: Aplicação Python que expõe uma API REST
2. **Database Service (PostgreSQL)**: Banco de dados relacional para armazenar dados
3. **Cache Service (Redis)**: Cache em memória para melhorar performance

## Decisões Técnicas

- **Flask**: Framework web leve e flexível para Python
- **PostgreSQL**: Banco de dados robusto e confiável
- **Redis**: Cache de alta performance em memória
- **Health Checks**: Garantem que serviços estejam prontos antes de iniciar dependências
- **Depends On**: Controla a ordem de inicialização dos serviços
- **Rede Interna**: Isola os serviços em uma rede privada

## Funcionamento

### Comunicação entre Serviços

Os serviços se comunicam através de uma rede Docker interna (`app-network`). O Docker Compose fornece DNS interno, permitindo que os serviços se encontrem pelo nome do serviço.

### Dependências

- **Web depende de DB e Cache**: O serviço web só inicia após DB e Cache estarem saudáveis
- **Health Checks**: Cada serviço possui verificações de saúde que garantem prontidão
- **Restart Policies**: Serviços reiniciam automaticamente em caso de falha

### Fluxo de Requisições

1. Cliente faz requisição para `/users` ou `/products`
2. Web verifica cache (Redis)
3. Se cache hit: retorna dados do cache
4. Se cache miss: consulta banco de dados
5. Armazena resultado no cache (TTL: 30 segundos)
6. Retorna dados ao cliente

## Instruções de Execução

### Pré-requisitos

- Docker instalado e rodando
- Docker Compose instalado

### Passo a Passo

1. **Navegue até a pasta do desafio:**
   ```bash
   cd desafio3
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

4. **Teste a aplicação:**

   **Verificar saúde dos serviços:**
   ```bash
   curl http://localhost:5000/health
   ```

   **Listar usuários (primeira vez - do banco):**
   ```bash
   curl http://localhost:5000/users
   ```

   **Listar usuários novamente (do cache):**
   ```bash
   curl http://localhost:5000/users
   ```

   **Listar produtos:**
   ```bash
   curl http://localhost:5000/products
   ```

   **Estatísticas do cache:**
   ```bash
   curl http://localhost:5000/cache/stats
   ```

5. **Visualizar logs:**
   ```bash
   docker-compose logs -f
   ```

   Ou logs de um serviço específico:
   ```bash
   docker-compose logs -f web
   docker-compose logs -f db
   docker-compose logs -f cache
   ```

6. **Parar os serviços:**
   ```bash
   docker-compose down
   ```

## Endpoints da API

### GET /

Retorna informações sobre a API e endpoints disponíveis.

```bash
curl http://localhost:5000/
```

### GET /health

Verifica o status de todos os serviços (web, database, cache).

```bash
curl http://localhost:5000/health
```

Resposta:
```json
{
  "web": "online",
  "database": "online",
  "cache": "online"
}
```

### GET /users

Retorna lista de usuários. Usa cache Redis (TTL: 30 segundos).

```bash
curl http://localhost:5000/users
```

Resposta (primeira vez - do banco):
```json
{
  "source": "database",
  "data": [
    {"id": 1, "nome": "Ana Silva", "email": "ana@example.com"},
    ...
  ]
}
```

Resposta (do cache):
```json
{
  "source": "cache",
  "data": [...]
}
```

### GET /products

Retorna lista de produtos. Usa cache Redis (TTL: 30 segundos).

```bash
curl http://localhost:5000/products
```

### GET /cache/stats

Retorna estatísticas do cache Redis.

```bash
curl http://localhost:5000/cache/stats
```

## Estrutura de Arquivos

```
desafio3/
├── web/
│   ├── Dockerfile          # Dockerfile da aplicação Flask
│   ├── requirements.txt    # Dependências Python
│   └── app.py              # Aplicação Flask
├── db/
│   └── init.sql            # Script de inicialização do banco
├── docker-compose.yml      # Orquestração dos serviços
└── README.md               # Este arquivo
```

## Explicação Detalhada

### docker-compose.yml

#### Serviço: db

- **Imagem**: PostgreSQL 15 Alpine
- **Porta**: 5433 (host) → 5432 (container)
- **Volume**: Persiste dados do banco
- **Health Check**: Verifica se o banco está pronto para conexões
- **Init Script**: Executa `init.sql` na primeira inicialização

#### Serviço: cache

- **Imagem**: Redis 7 Alpine
- **Porta**: 6379
- **Health Check**: Verifica se Redis está respondendo
- **Persistência**: AOF (Append Only File) habilitado

#### Serviço: web

- **Build**: Constrói imagem a partir do Dockerfile em `./web`
- **Porta**: 5000
- **Variáveis de Ambiente**: Configuração de conexão com DB e Redis
- **Depends On**: Aguarda DB e Cache estarem saudáveis
- **Rede**: Conectado à rede interna `app-network`

### Dependências e Ordem de Inicialização

```yaml
depends_on:
  db:
    condition: service_healthy
  cache:
    condition: service_healthy
```

Isso garante que:
1. DB e Cache iniciem primeiro
2. Health checks confirmem que estão prontos
3. Web só inicie após confirmação

### Rede Interna

Todos os serviços estão na mesma rede (`app-network`), permitindo comunicação usando nomes de serviço:
- `http://db:5432` (do container web)
- `redis://cache:6379` (do container web)

### Cache Strategy

A aplicação implementa cache com TTL de 30 segundos:
- Primeira requisição: busca no banco, armazena no cache
- Requisições subsequentes: retorna do cache
- Após 30 segundos: cache expira, próxima requisição busca no banco novamente

## Testes e Validação

### Teste 1: Verificar Comunicação

```bash
curl http://localhost:5000/health
```

Todos os serviços devem estar "online".

### Teste 2: Cache Funcionando

```bash
# Primeira requisição (deve vir do banco)
curl http://localhost:5000/users | jq '.source'
# Resultado: "database"

# Segunda requisição imediata (deve vir do cache)
curl http://localhost:5000/users | jq '.source'
# Resultado: "cache"
```

### Teste 3: Persistência do Banco

```bash
# Parar serviços
docker-compose down

# Reiniciar (sem remover volumes)
docker-compose up -d

# Verificar que dados persistiram
curl http://localhost:5000/users
```

### Teste 4: Logs de Comunicação

```bash
docker-compose logs web | grep -i "database\|cache"
```

## Comandos Úteis

### Gerenciamento

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Reconstruir imagens
docker-compose build --no-cache

# Ver status
docker-compose ps

# Ver logs
docker-compose logs -f [servico]
```

### Acesso aos Containers

```bash
# Acessar container web
docker exec -it desafio3-web sh

# Acessar banco de dados
docker exec -it desafio3-db psql -U admin -d desafio3_db

# Acessar Redis
docker exec -it desafio3-cache redis-cli
```

### Inspecionar Rede

```bash
docker network inspect desafio3-network
```

## Resultados Esperados

- ✅ Todos os serviços iniciam corretamente
- ✅ Health checks funcionam
- ✅ Web se comunica com DB e Cache
- ✅ Cache funciona (primeira requisição do banco, segunda do cache)
- ✅ Dados persistem após reiniciar containers
- ✅ Logs mostram comunicação entre serviços

## Limpeza

Para remover tudo (containers, volumes, rede):

```bash
docker-compose down -v
docker network prune -f
```

## Conclusão

Este desafio demonstra como Docker Compose facilita a orquestração de múltiplos serviços interdependentes, gerenciando:
- Ordem de inicialização
- Health checks
- Rede interna
- Volumes de persistência
- Variáveis de ambiente

A arquitetura resultante é escalável, isolada e fácil de gerenciar.


