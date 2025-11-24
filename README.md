# Projeto Docker e Microsserviços

Este repositório contém a implementação de 5 desafios práticos sobre Docker e Arquitetura de Microsserviços, desenvolvidos como parte de uma avaliação acadêmica.

## Estrutura do Projeto

```
projeto2/
├── desafio1/          # Containers em Rede
├── desafio2/          # Volumes e Persistência
├── desafio3/          # Docker Compose Orquestrando Serviços
├── desafio4/          # Microsserviços Independentes
├── desafio5/          # Microsserviços com API Gateway
└── README.md          # Este arquivo
```

## Pré-requisitos

Antes de executar os desafios, certifique-se de ter instalado:

- **Docker** (versão 20.10 ou superior)
- **Docker Compose** (versão 2.0 ou superior)

### Instalação do Docker no Windows

1. Baixe o Docker Desktop para Windows: https://www.docker.com/products/docker-desktop
2. Execute o instalador e siga as instruções
3. Reinicie o computador se necessário
4. Abra o Docker Desktop e aguarde a inicialização
5. Verifique a instalação executando no terminal:
   ```bash
   docker --version
   docker-compose --version
   ```

## Desafios

### [Desafio 1 - Containers em Rede](./desafio1/README.md)
Demonstração de comunicação entre containers através de uma rede Docker customizada.

### [Desafio 2 - Volumes e Persistência](./desafio2/README.md)
Demonstração de persistência de dados usando volumes Docker.

### [Desafio 3 - Docker Compose](./desafio3/README.md)
Orquestração de múltiplos serviços usando Docker Compose.

### [Desafio 4 - Microsserviços Independentes](./desafio4/README.md)
Dois microsserviços independentes que se comunicam via HTTP.

### [Desafio 5 - Microsserviços com API Gateway](./desafio5/README.md)
Arquitetura completa com API Gateway centralizando acesso a microsserviços.

## Execução Rápida

Cada desafio possui seu próprio diretório com instruções detalhadas. Acesse a pasta do desafio desejado e siga as instruções no README.md específico.

### Comandos Básicos para Todos os Desafios

```bash
# Navegar até o desafio
cd desafio[N]

# Construir e iniciar containers
docker-compose up --build

# Executar em background
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Parar e remover volumes (cuidado: apaga dados)
docker-compose down -v
```

## Resumo dos Desafios

| Desafio | Descrição | Portas | Tecnologias |
|---------|-----------|--------|-------------|
| **Desafio 1** | Containers em Rede | 8080 | Nginx, Alpine, curl |
| **Desafio 2** | Volumes e Persistência | 5432 | PostgreSQL |
| **Desafio 3** | Docker Compose | 5000, 5433, 6379 | Flask, PostgreSQL, Redis |
| **Desafio 4** | Microsserviços Independentes | 8001, 8002 | Flask, Python |
| **Desafio 5** | API Gateway | 8080 | Flask, Python |

## Verificação da Instalação

Após instalar o Docker, verifique se está funcionando:

```bash
# Verificar versão do Docker
docker --version

# Verificar versão do Docker Compose
docker-compose --version

# Testar execução de um container
docker run hello-world

# Ver containers em execução
docker ps

# Ver todas as imagens
docker images
```

## Solução de Problemas

### Docker não inicia
- Certifique-se de que o Docker Desktop está rodando
- Verifique se a virtualização está habilitada no BIOS
- Reinicie o Docker Desktop

### Porta já em uso
- Verifique se outra aplicação está usando a porta
- Altere a porta no `docker-compose.yml` se necessário

### Erro de permissão
- No Windows, certifique-se de estar executando como administrador se necessário
- Verifique as configurações do Docker Desktop

### Limpar tudo
```bash
# Parar todos os containers
docker stop $(docker ps -aq)

# Remover todos os containers
docker rm $(docker ps -aq)

# Remover todas as imagens
docker rmi $(docker images -q)

# Limpar sistema (cuidado: remove tudo)
docker system prune -a --volumes
```

## Sobre o Projeto

Este projeto foi desenvolvido como parte de uma avaliação acadêmica sobre Docker e Arquitetura de Microsserviços. Cada desafio foi implementado seguindo os requisitos especificados, com foco em demonstrar o funcionamento prático de containers, volumes, orquestração e comunicação entre serviços.

