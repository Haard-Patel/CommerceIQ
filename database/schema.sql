-- ============================================================
-- CommerceIQ Database Schema
-- E-Commerce Intelligence & Analytics Platform
-- ============================================================

-- ============================================================
-- CUSTOMERS
-- ============================================================

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    country VARCHAR(100),
    first_order_date TIMESTAMP,
    last_order_date TIMESTAMP,
    order_count INTEGER DEFAULT 0,
    total_revenue NUMERIC(14, 2) DEFAULT 0
);


-- ============================================================
-- PRODUCTS
-- ============================================================

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    description VARCHAR(255),
    first_seen_at TIMESTAMP,
    last_seen_at TIMESTAMP,
    average_unit_price NUMERIC(14, 4)
);


-- ============================================================
-- ORDERS
-- ============================================================

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id INTEGER,
    order_date TIMESTAMP NOT NULL,
    country VARCHAR(100),
    is_cancelled BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- ============================================================
-- ORDER ITEMS
-- ============================================================

CREATE TABLE order_items (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(14, 4) NOT NULL,
    line_revenue NUMERIC(14, 4) NOT NULL,

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


-- ============================================================
-- DIMENSION: DATE
-- ============================================================

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    calendar_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL
);


-- ============================================================
-- DIMENSION: COUNTRY
-- ============================================================

CREATE TABLE dim_country (
    country_key SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE
);


-- ============================================================
-- FACT: SALES
-- ============================================================

CREATE TABLE fact_sales (
    sales_id BIGSERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    customer_id INTEGER,
    date_key INTEGER NOT NULL,
    country_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 4) NOT NULL,
    revenue NUMERIC(14, 4) NOT NULL,
    is_cancelled BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_fact_sales_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_fact_sales_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_fact_sales_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_fact_sales_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT fk_fact_sales_country
        FOREIGN KEY (country_key)
        REFERENCES dim_country(country_key)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_orders_customer_id
    ON orders(customer_id);

CREATE INDEX idx_orders_order_date
    ON orders(order_date);

CREATE INDEX idx_order_items_order_id
    ON order_items(order_id);

CREATE INDEX idx_order_items_product_id
    ON order_items(product_id);

CREATE INDEX idx_fact_sales_date_key
    ON fact_sales(date_key);

CREATE INDEX idx_fact_sales_product_id
    ON fact_sales(product_id);

CREATE INDEX idx_fact_sales_customer_id
    ON fact_sales(customer_id);

CREATE INDEX idx_fact_sales_country_key
    ON fact_sales(country_key);


-- ============================================================
-- SCHEMA VERIFICATION
-- ============================================================

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;