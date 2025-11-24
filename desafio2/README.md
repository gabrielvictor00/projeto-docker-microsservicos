# Desafio 2 - Volumes e Persistência

## Descrição

Este desafio demonstra a persistência de dados usando volumes Docker. Um container PostgreSQL armazena dados em um volume nomeado, permitindo que as informações sejam mantidas mesmo após a remoção do container.

## Arquitetura

```
┌─────────────────────────────────┐
│  PostgreSQL Container           │
│  (Porta 5432)                   │
│                                  │
│  ┌───────────────────────────┐  │
│  │  Banco de Dados           │  │
│  │  - desafio2_db            │  │
│  │  - Tabelas:               │  │
│  │    * usuarios             │  │
│  │    * produtos             │  │
│  └───────────────────────────┘  │
└──────────────┬──────────────────┘
               │
               │ Volume Mount
               ▼
    ┌──────────────────────┐
    │  Volume Docker       │
    │  postgres_data       │
    │  (Persistente)       │
    └──────────────────────┘
```

### Componentes

1. **PostgreSQL Container**: Banco de dados rodando na porta 5432
2. **Volume Nomeado**: `postgres_data` que persiste os dados em `/var/lib/postgresql/data`
3. **Container Reader** (Opcional): Container que lê os dados persistidos

## Decisões Técnicas

- **PostgreSQL 15 Alpine**: Versão leve e estável do PostgreSQL
- **Volume Nomeado**: Permite persistência e fácil gerenciamento
- **Docker Compose**: Facilita o gerenciamento do volume e container
- **Script de Inicialização**: `init.sql` cria tabelas e dados iniciais

## Funcionamento

### Volumes Docker

Um volume Docker é um mecanismo para persistir dados gerados e usados por containers. Diferente de bind mounts, volumes são completamente gerenciados pelo Docker.

### Persistência

1. **Criação do Volume**: O Docker cria automaticamente o volume `postgres_data` na primeira execução
2. **Montagem**: O volume é montado em `/var/lib/postgresql/data` dentro do container
3. **Armazenamento**: Todos os dados do PostgreSQL são salvos no volume
4. **Persistência**: Mesmo após remover o container, o volume permanece com os dados

### Fluxo de Dados

```
Container Criado → Volume Montado → Dados Salvos no Volume
     ↓
Container Removido → Volume Permanece → Dados Preservados
     ↓
Container Recriado → Volume Remontado → Dados Restaurados
```

## Instruções de Execução

### Pré-requisitos

- Docker instalado e rodando
- Docker Compose instalado

### Passo a Passo

#### Execução Básica

1. **Navegue até a pasta do desafio:**
   ```bash
   cd desafio2
   ```

2. **Construa e inicie o container:**
   ```bash
   docker-compose up -d --build
   ```

3. **Aguarde alguns segundos para o banco inicializar:**
   ```bash
   sleep 5
   ```

4. **Verifique os dados iniciais:**
   ```bash
   docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT * FROM usuarios;"
   docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT * FROM produtos;"
   ```

5. **Adicione novos dados:**
   ```bash
   docker exec desafio2-db psql -U admin -d desafio2_db -c "INSERT INTO usuarios (nome, email) VALUES ('Carlos Mendes', 'carlos@example.com');"
   ```

6. **Verifique o volume criado:**
   ```bash
   docker volume ls
   docker volume inspect desafio2_postgres_data
   ```

#### Teste de Persistência

1. **Execute o script de teste automatizado:**
   ```bash
   chmod +x test-persistence.sh
   ./test-persistence.sh
   ```

   Ou no Windows PowerShell:
   ```powershell
   bash test-persistence.sh
   ```

2. **Teste manual:**
   ```bash
   # Parar e remover o container
   docker-compose down
   
   # Verificar que o volume ainda existe
   docker volume ls | grep desafio2
   
   # Recriar o container
   docker-compose up -d
   
   # Aguardar inicialização
   sleep 5
   
   # Verificar que os dados persistiram
   docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT * FROM usuarios;"
   ```

#### Usar o Container Reader

O docker-compose.yml inclui um serviço `reader` que consulta os dados:

```bash
docker-compose up reader
```

## Estrutura de Dados

### Tabela: usuarios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | SERIAL | Chave primária |
| nome | VARCHAR(100) | Nome do usuário |
| email | VARCHAR(100) | Email único |
| data_criacao | TIMESTAMP | Data de criação |

### Tabela: produtos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | SERIAL | Chave primária |
| nome | VARCHAR(100) | Nome do produto |
| preco | DECIMAL(10,2) | Preço |
| estoque | INTEGER | Quantidade em estoque |

## Comandos Úteis

### Consultar Dados

```bash
# Listar todos os usuários
docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT * FROM usuarios;"

# Listar todos os produtos
docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT * FROM produtos;"

# Contar registros
docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT COUNT(*) FROM usuarios;"
```

### Inserir Dados

```bash
docker exec desafio2-db psql -U admin -d desafio2_db -c "INSERT INTO usuarios (nome, email) VALUES ('Novo Usuário', 'novo@example.com');"
```

### Gerenciar Volumes

```bash
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect desafio2_postgres_data

# Ver uso do volume
docker system df -v
```

## Estrutura de Arquivos

```
desafio2/
├── Dockerfile              # Dockerfile do PostgreSQL
├── init.sql                # Script de inicialização do banco
├── docker-compose.yml      # Orquestração com volume
├── test-persistence.sh     # Script de teste automatizado
└── README.md               # Este arquivo
```

## Explicação Detalhada

### Dockerfile

Cria uma imagem baseada no PostgreSQL 15 Alpine, define variáveis de ambiente e copia o script de inicialização.

### init.sql

Script executado automaticamente na primeira inicialização do banco. Cria as tabelas `usuarios` e `produtos` e insere dados iniciais.

### docker-compose.yml

Define:
- **Serviço postgres**: Container do banco de dados com volume montado
- **Serviço reader**: Container opcional para ler dados
- **Volume postgres_data**: Volume nomeado para persistência

### Volume vs Bind Mount

- **Volume**: Gerenciado pelo Docker, melhor para produção
- **Bind Mount**: Mapeia diretório do host, útil para desenvolvimento

Neste desafio usamos **volume nomeado** para garantir portabilidade e melhor gerenciamento.

## Validação da Persistência

### Teste Completo

1. ✅ Criar container e inserir dados
2. ✅ Verificar dados no container
3. ✅ Parar e remover container
4. ✅ Verificar que volume existe
5. ✅ Recriar container
6. ✅ Verificar que dados persistiram

### Resultados Esperados

- ✅ Volume criado automaticamente
- ✅ Dados iniciais carregados do `init.sql`
- ✅ Dados persistem após remoção do container
- ✅ Dados restaurados ao recriar container
- ✅ Container reader consegue acessar dados

## Limpeza

### Remover Container (mantendo volume)

```bash
docker-compose down
```

### Remover Container e Volume

```bash
docker-compose down -v
```

### Remover Volume Manualmente

```bash
docker volume rm desafio2_postgres_data
```

⚠️ **Atenção**: Remover o volume apaga todos os dados permanentemente!

## Conclusão

Este desafio demonstra que volumes Docker são essenciais para persistência de dados em aplicações containerizadas. Os dados permanecem seguros mesmo quando containers são recriados, atualizados ou removidos.


