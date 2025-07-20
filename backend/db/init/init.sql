CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  brand TEXT NOT NULL,
  features TEXT,
  price NUMERIC NOT NULL,
  quantity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    role VARCHAR(20) NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'user')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_type VARCHAR(20) NOT NULL CHECK (message_type IN ('user', 'assistant')),
    content TEXT NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at);

COMMENT ON TABLE products IS 'Product and stock catalog for e-commerce';
COMMENT ON TABLE users IS 'User accounts for authentication and personalization';
COMMENT ON TABLE chat_messages IS 'Chat conversation history for each user session';

INSERT INTO products (name, brand, features, price, quantity) VALUES
    ('UltraBook X15', 'HP', '16GB RAM;512GB SSD', 1200.0, 2),
    ('GamingPro G5', 'Dell', '32GB RAM;1TB SSD;RTX3070', 1800.0, 1),
    ('iPhone 15 Pro', 'Apple', '256GB;A17 Pro;48MP Camera', 999.0, 5),
    ('Samsung Galaxy S24', 'Samsung', '128GB;Snapdragon 8 Gen 3;AI Features', 799.0, 8),
    ('Sony WH-1000XM5', 'Sony', 'Noise Cancelling;30h Battery;Bluetooth 5.2', 349.0, 12),
    ('Nike Air Max 270', 'Nike', 'Men''s Size 10;Black/White;Air Max Unit', 150.0, 25),
    ('Instant Pot Duo 7-in-1', 'Instant Pot', '6QT;Pressure Cooker;Slow Cooker;Rice Cooker', 89.0, 15),
    ('Kindle Paperwhite', 'Amazon', '8GB;6.8" Display;Waterproof;Warm Light', 139.0, 20),
    ('Adidas Ultraboost 22', 'Adidas', 'Women''s Size 8;Primeknit Upper;Boost Midsole', 190.0, 18),
    ('Dyson V15 Detect', 'Dyson', 'Cordless;Laser Detection;60min Runtime', 699.0, 7),
    ('Apple Watch Series 9', 'Apple', '45mm;GPS;Heart Rate Monitor;ECG', 399.0, 10),
    ('Levi''s 501 Original Jeans', 'Levi''s', 'Men''s 32x32;Classic Fit;100% Cotton', 69.0, 30);
