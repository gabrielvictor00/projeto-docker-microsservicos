CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nome, email) VALUES
    ('João Silva', 'joao@example.com'),
    ('Maria Santos', 'maria@example.com'),
    ('Pedro Oliveira', 'pedro@example.com');

CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INTEGER DEFAULT 0
);

INSERT INTO produtos (nome, preco, estoque) VALUES
    ('Notebook', 3500.00, 10),
    ('Mouse', 50.00, 50),
    ('Teclado', 120.00, 30);


