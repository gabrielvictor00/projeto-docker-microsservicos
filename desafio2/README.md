# Desafio 2 - Volumes e Persistência

## Descrição

Este desafio implementa um sistema de persistência de dados usando volumes Docker. A solução utiliza um container PostgreSQL que armazena seus dados em um volume nomeado, garantindo que as informações sejam preservadas mesmo quando o container é removido e recriado.

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

As escolhas técnicas para este desafio foram:

- **PostgreSQL 15 Alpine**: Escolhi esta versão por ser estável e leve. A imagem Alpine reduz o tamanho da imagem em comparação com a versão padrão, mantendo todas as funcionalidades necessárias.
- **Volume Nomeado**: Optei por usar um volume nomeado ao invés de bind mount porque volumes são completamente gerenciados pelo Docker, oferecem melhor portabilidade e são mais adequados para ambientes de produção. O volume persiste independentemente do ciclo de vida do container.
- **Docker Compose**: Usei Docker Compose para facilitar o gerenciamento do volume e do container, além de permitir a criação automática do volume na primeira execução.
- **Script de Inicialização**: Implementei um script `init.sql` que é executado automaticamente na primeira inicialização do banco, criando as tabelas e inserindo dados iniciais para demonstração.

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

O Dockerfile estende a imagem oficial `postgres:15-alpine` e define as variáveis de ambiente necessárias para configurar o banco de dados (nome do banco, usuário e senha). O arquivo `init.sql` é copiado para o diretório `/docker-entrypoint-initdb.d/`, que é um diretório especial do PostgreSQL. Qualquer script SQL neste diretório é executado automaticamente na primeira inicialização do banco, antes do serviço ficar disponível.

### init.sql

Este script SQL é executado automaticamente quando o container é criado pela primeira vez. Ele cria duas tabelas:
- **usuarios**: Armazena informações de usuários com campos id, nome, email e data_criacao
- **produtos**: Armazena informações de produtos com campos id, nome, preco e estoque

O script também insere dados iniciais em ambas as tabelas para demonstração. Esses dados são criados apenas na primeira inicialização, mas ficam persistidos no volume.

### docker-compose.yml

O arquivo define:
- **Serviço postgres**: Container do PostgreSQL com o volume `postgres_data` montado em `/var/lib/postgresql/data` (diretório padrão onde o PostgreSQL armazena dados). O volume é criado automaticamente na primeira execução.
- **Serviço reader**: Container opcional que usa a mesma imagem do PostgreSQL para consultar os dados. Este serviço demonstra como um segundo container pode acessar os dados persistidos.
- **Volume postgres_data**: Volume nomeado que persiste os dados do banco. Este volume permanece mesmo quando o container é removido.

### Volume vs Bind Mount

Existem duas formas principais de persistir dados no Docker:
- **Volume**: Gerenciado completamente pelo Docker, armazenado em um local gerenciado pelo sistema Docker. É a melhor opção para produção pois oferece melhor portabilidade e performance.
- **Bind Mount**: Mapeia diretamente um diretório do sistema host para o container. Útil para desenvolvimento, mas menos portável.

Para este desafio, escolhi usar um **volume nomeado** porque oferece melhor portabilidade (funciona em qualquer sistema), é gerenciado pelo Docker, e os dados ficam isolados do sistema de arquivos do host.

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

Através deste desafio, pude comprovar na prática a importância dos volumes Docker para persistência de dados. A solução demonstra que os dados permanecem seguros e acessíveis mesmo quando containers são recriados, atualizados ou removidos, o que é fundamental para aplicações em produção.


