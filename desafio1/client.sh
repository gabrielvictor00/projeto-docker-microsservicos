#!/bin/sh

echo "Cliente iniciado. Fazendo requisições para o servidor web..."

while true; do
    echo "=========================================="
    echo "Fazendo requisição HTTP para o servidor..."
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
    
    response=$(curl -s -w "\nStatus Code: %{http_code}\nTempo de Resposta: %{time_total}s" http://web-server:8080)
    
    echo "$response"
    echo "=========================================="
    echo ""
    
    sleep 5
done


