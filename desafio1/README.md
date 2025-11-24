# Desafio 1 - Containers em Rede

## Descrição

Este desafio implementa dois containers Docker que se comunicam através de uma rede customizada. A solução consiste em um servidor web Nginx rodando na porta 8080 e um container cliente que realiza requisições HTTP periódicas para demonstrar a comunicação entre containers.

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

Para este desafio, escolhi as seguintes tecnologias:

- **Nginx Alpine**: Escolhi esta imagem por ser leve e eficiente para servir conteúdo estático. A versão Alpine reduz significativamente o tamanho da imagem final.
- **Alpine Linux**: Usei Alpine como base para o container cliente por ser uma distribuição mínima, ideal para containers que precisam apenas de ferramentas básicas como curl.
- **Bridge Network**: Utilizei uma rede do tipo bridge, que é o padrão do Docker. Esta rede permite que containers na mesma rede se comuniquem usando seus nomes como hostnames, facilitando a descoberta de serviços.
- **Docker Compose**: Optei por usar Docker Compose para facilitar a orquestração dos containers e a criação da rede customizada de forma declarativa.

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

Este Dockerfile cria a imagem do servidor web. Ele parte da imagem base `nginx:alpine`, que já contém o servidor Nginx configurado. O arquivo copia a página HTML (`index.html`) para o diretório padrão do Nginx e também copia uma configuração customizada (`nginx.conf`) que define o servidor para escutar na porta 8080 ao invés da porta padrão 80. A porta 8080 é exposta para permitir acesso externo.

### Dockerfile.client

O Dockerfile do cliente cria uma imagem mínima baseada em Alpine Linux. Instala o `curl` através do gerenciador de pacotes `apk`, copia o script `client.sh` que contém o loop de requisições HTTP, e torna o script executável. Este container não precisa expor portas, pois apenas faz requisições de saída.

### docker-compose.yml

O arquivo docker-compose.yml define a orquestração completa:
- **web-server**: Serviço que constrói a imagem do servidor e mapeia a porta 8080 do host para a porta 8080 do container
- **client**: Serviço que constrói a imagem do cliente e depende do web-server estar rodando
- **custom-network**: Define uma rede do tipo bridge nomeada `desafio1-network`, onde ambos os containers se conectam

A rede customizada permite que os containers se comuniquem usando o nome do serviço como hostname. Por isso, o cliente pode acessar o servidor usando `http://web-server:8080`.

### Comunicação via DNS Interno

Uma das funcionalidades mais úteis do Docker é o DNS interno. Quando containers estão na mesma rede, o Docker automaticamente resolve os nomes dos serviços (definidos no docker-compose.yml) para seus endereços IP. Isso significa que o container cliente pode acessar o servidor usando simplesmente `http://web-server:8080`, sem precisar descobrir ou hardcodar o IP do container servidor. O Docker gerencia isso automaticamente.

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


