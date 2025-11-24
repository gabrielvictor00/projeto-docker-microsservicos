#!/bin/bash

echo "=== TESTE DE PERSISTÊNCIA DE DADOS ==="
echo ""

echo "1. Criando e iniciando o container do banco de dados..."
docker-compose up -d postgres

echo ""
echo "2. Aguardando inicialização do banco..."
sleep 5

echo ""
echo "3. Inserindo dados adicionais no banco..."
docker exec desafio2-db psql -U admin -d desafio2_db -c "INSERT INTO usuarios (nome, email) VALUES ('Ana Costa', 'ana@example.com');"
docker exec desafio2-db psql -U admin -d desafio2_db -c "INSERT INTO produtos (nome, preco, estoque) VALUES ('Monitor', 800.00, 15);"

echo ""
echo "4. Consultando dados antes de remover o container..."
docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT * FROM usuarios;"
docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT * FROM produtos;"

echo ""
echo "5. Parando e removendo o container..."
docker-compose down

echo ""
echo "6. Verificando que o volume ainda existe..."
docker volume ls | grep desafio2_postgres_data

echo ""
echo "7. Recriando o container (sem remover o volume)..."
docker-compose up -d postgres
sleep 5

echo ""
echo "8. Consultando dados após recriação do container..."
echo "Se os dados persistirem, o teste foi bem-sucedido!"
docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT * FROM usuarios;"
docker exec desafio2-db psql -U admin -d desafio2_db -c "SELECT * FROM produtos;"

echo ""
echo "=== TESTE CONCLUÍDO ==="


