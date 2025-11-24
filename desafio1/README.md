# Desafio 1 - Containers em Rede

## Descrição

Este desafio demonstra a comunicação entre dois containers Docker através de uma rede customizada. Um container executa um servidor web Nginx na porta 8080, enquanto outro container realiza requisições HTTP periódicas para o servidor.

## Arquitetura

```
┌─────────────────┐         ┌─────────────────┐
│  Web Server     │◄────────┤  Client         │
│  (Nginx:8080)   │         │  (curl loop)    │
└─────────────────┘         └─────────────────┘
         │                           │
         └───────────┬───────────────┘
                     │
            ┌────────▼────────┐
            │ Custom Network  │
            │ (Bridge Driver) │
            └─────────────────┘
```

### Componentes

1. **Web Server Container**: Servidor Nginx servindo uma página HTML na porta 8080
2. **Client Container**: Container Alpine com curl que faz requisições HTTP periódicas a cada 5 segundos
3. **Custom Network**: Rede Docker do tipo bridge nomeada `desafio1-network`

## Decisões Técnicas

- **Nginx Alpine**: Imagem leve e eficiente para o servidor web
- **Alpine Linux**: Base mínima para o container cliente
- **Bridge Network**: Tipo de rede padrão que permite comunicação entre containers na mesma rede
- **Docker Compose**: Facilita a orquestração e gerenciamento dos containers

## Funcionamento

### Rede Docker

A rede customizada `desafio1-network` é criada automaticamente pelo Docker Compose. Esta rede permite que os containers se comuniquem usando seus nomes de serviço como hostnames (DNS interno do Docker).

### Comunicação

- O container cliente acessa o servidor usando o hostname `web-server` (nome do serviço no docker-compose.yml)
- O Docker resolve automaticamente o nome para o IP do container na rede
- As requisições são feitas via HTTP na porta 8080

### Logs

Os logs do cliente mostram:
- Timestamp de cada requisição
- Status HTTP da resposta
- Tempo de resposta
- Conteúdo HTML retornado (primeiras linhas)

## Instruções de Execução

### Pré-requisitos

- Docker instalado e rodando
- Docker Compose instalado

### Passo a Passo

1. **Navegue até a pasta do desafio:**
   ```bash
   cd desafio1
   ```

2. **Construa e inicie os containers:**
   ```bash
   docker-compose up --build
   ```

3. **Em outro terminal, visualize os logs do cliente:**
   ```bash
   docker logs -f desafio1-client
   ```

4. **Acesse o servidor web no navegador:**
   ```
   http://localhost:8080
   ```

5. **Verifique a rede criada:**
   ```bash
   docker network ls
   docker network inspect desafio1-network
   ```

6. **Para parar os containers:**
   ```bash
   docker-compose down
   ```

## Testes e Validação

### Teste 1: Verificar Comunicação

Execute o comando abaixo para verificar se o cliente está conseguindo se comunicar com o servidor:

```bash
docker exec desafio1-client curl -s http://web-server:8080 | head -20
```

### Teste 2: Verificar Rede

Liste os containers conectados à rede:

```bash
docker network inspect desafio1-network --format '{{range .Containers}}{{.Name}} {{end}}'
```

### Teste 3: Logs em Tempo Real

Observe os logs do cliente em tempo real para ver as requisições periódicas:

```bash
docker logs -f desafio1-client
```

Você verá saídas como:
```
==========================================
Fazendo requisição HTTP para o servidor...
Timestamp: 2025-11-23 21:15:30
<!DOCTYPE html>...
Status Code: 200
Tempo de Resposta: 0.005s
==========================================
```

## Estrutura de Arquivos

```
desafio1/
├── Dockerfile.server      # Dockerfile do servidor Nginx
├── Dockerfile.client      # Dockerfile do cliente
├── index.html             # Página HTML servida
├── nginx.conf             # Configuração do Nginx
├── client.sh              # Script do cliente (requisições periódicas)
├── docker-compose.yml     # Orquestração dos containers
└── README.md              # Este arquivo
```

## Explicação Detalhada

### Dockerfile.server

Cria uma imagem baseada no Nginx Alpine, copia a página HTML e a configuração do Nginx, e expõe a porta 8080.

### Dockerfile.client

Cria uma imagem Alpine com curl instalado, copia o script de requisições e o torna executável.

### docker-compose.yml

Define dois serviços:
- `web-server`: Servidor web na porta 8080
- `client`: Cliente que faz requisições periódicas

Ambos os serviços estão conectados à rede `custom-network` (tipo bridge).

### Comunicação via DNS Interno

O Docker fornece um DNS interno que resolve os nomes dos serviços para seus IPs na rede. Por isso, o cliente pode acessar `http://web-server:8080` sem precisar saber o IP do container.

## Resultados Esperados

- ✅ Servidor web acessível em http://localhost:8080
- ✅ Cliente fazendo requisições a cada 5 segundos
- ✅ Logs mostrando comunicação bem-sucedida (Status 200)
- ✅ Rede customizada criada e funcionando
- ✅ Containers se comunicando via hostname

## Limpeza

Para remover todos os containers, volumes e rede:

```bash
docker-compose down
docker network prune -f
```


