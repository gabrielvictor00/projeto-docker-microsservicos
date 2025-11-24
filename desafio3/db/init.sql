CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nome, email) VALUES
    ('Ana Silva', 'ana@example.com'),
    ('Bruno Costa', 'bruno@example.com'),
    ('Carla Mendes', 'carla@example.com'),
    ('Daniel Santos', 'daniel@example.com');

CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INTEGER DEFAULT 0
);

INSERT INTO produtos (nome, preco, estoque) VALUES
    ('Laptop', 4500.00, 8),
    ('Smartphone', 2500.00, 15),
    ('Tablet', 1800.00, 12),
    ('Fones de Ouvido', 350.00, 25);


