CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  brand TEXT NOT NULL,
  features TEXT,
  price NUMERIC NOT NULL,
  quantity INTEGER NOT NULL,
  categories JSON DEFAULT '[]',
  image_url VARCHAR(500),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE
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

insert into products (name, brand, features, price, quantity, categories, image_url, created_at, updated_at) values
    ('Arduino Uno R3', 'Arduino', 'Microcontroller;14 Digital I/O;6 Analog Inputs;USB Interface', 25.0, 50, '["microcontrollers", "electronics", "maker", "arduino", "programming"]', 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Raspberry Pi 4 Model B', 'Raspberry Pi', '4GB RAM;Quad-core ARM;WiFi;Bluetooth;4K Support', 55.0, 30, '["single-board-computers", "electronics", "maker", "raspberry-pi", "programming"]', 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('3D Printer Ender 3 Pro', 'Creality', '220x220x250mm Build;Resume Print;Carborundum Glass', 299.0, 15, '["3d-printing", "maker", "manufacturing", "prototyping"]', 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('DJI Mini 3 Pro Drone', 'DJI', '4K Camera;34min Flight;Obstacle Avoidance;Lightweight', 759.0, 8, '["drones", "cameras", "tech", "aerial", "photography"]', 'https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Oculus Quest 2 VR Headset', 'Meta', '128GB;Wireless VR;Touch Controllers;6DOF Tracking', 299.0, 12, '["vr", "gaming", "tech", "virtual-reality", "entertainment"]', 'https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('MacBook Pro M2', 'Apple', '13-inch;8GB RAM;256GB SSD;M2 Chip;Retina Display', 1299.0, 10, '["laptops", "computers", "apple", "tech", "professional"]', 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Sony A7 IV Camera', 'Sony', '33MP Full-Frame;4K Video;Real-time Eye AF;5-axis Stabilization', 2499.0, 5, '["cameras", "photography", "professional", "mirrorless", "tech"]', 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('iPad Pro 12.9" M2', 'Apple', '12.9-inch;M2 Chip;128GB;Liquid Retina XDR;Apple Pencil Compatible', 1099.0, 15, '["tablets", "apple", "tech", "creative", "professional"]', 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('GoPro Hero 11 Black', 'GoPro', '5.3K Video;27MP Photos;HyperSmooth 5.0;Waterproof', 399.0, 20, '["action-cameras", "sports", "tech", "adventure", "video"]', 'https://images.unsplash.com/photo-1574944985070-8b3b3a2a1c1b?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Samsung Galaxy Tab S9', 'Samsung', '11-inch;8GB RAM;128GB;S Pen;AMOLED Display', 699.0, 18, '["tablets", "android", "tech", "creative", "productivity"]', 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Nintendo Switch OLED', 'Nintendo', '7-inch OLED Screen;64GB Storage;Joy-Con Controllers;Dock Included', 349.0, 25, '["gaming", "consoles", "entertainment", "tech", "nintendo"]', 'https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Sony WH-1000XM5 Headphones', 'Sony', 'Noise Cancelling;30h Battery;Bluetooth 5.2;Premium Sound', 349.0, 12, '["headphones", "audio", "tech", "wireless", "premium"]', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);