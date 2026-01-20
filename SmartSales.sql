drop table if exists item;
drop table if exists orders;
drop table if exists status;
drop table if exists users;
drop table if exists staff;
drop table if exists price;
drop table if exists product;
drop table if exists customer;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

create table customer (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_name varchar(50) NOT NULL,
    customer_email varchar(40) UNIQUE NOT NULL,
    customer_phone varchar(15) NOT NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

insert into customer (customer_name, customer_email, customer_phone) VALUES
('John Smith', 'john.smith@gmail.com', '+12025550101'),
('Emily Johnson', 'emily.johnson@gmail.com', '+12025550102'),
('Michael Brown', 'michael.brown@gmail.com', '+12025550103'),
('Sarah Wilson', 'sarah.wilson@gmail.com', '+12025550104'),
('David Miller', 'david.miller@gmail.com', '+12025550105'),
('Jessica Davis', 'jessica.davis@gmail.com', '+12025550106'),
('Daniel Anderson', 'daniel.anderson@gmail.com', '+12025550107'),
('Laura Martinez', 'laura.martinez@gmail.com', '+34915550108'),
('Robert Taylor', 'robert.taylor@gmail.com', '+44770090010'),
('Sophia Garcia', 'sophia.garcia@gmail.com', '+52155501011');

create table product (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_name varchar(100) NOT NULL,
    product_description text,
    product_quantity int NOT NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

insert into product (product_name, product_description, product_quantity) VALUES
('Laptop', 'A high-performance laptop suitable for all your computing needs.', 50),
('Smartphone', 'A latest-generation smartphone with advanced features.', 100),
('Headphones', 'Noise-cancelling over-ear headphones for immersive sound.', 75),
('Smartwatch', 'A stylish smartwatch with fitness tracking capabilities.', 60),
('Tablet', 'A lightweight tablet perfect for browsing and media consumption.', 80),
('Camera', 'A digital camera with high resolution and multiple lenses.', 40),
('Printer', 'A wireless printer with fast printing speeds and high quality.', 30),
('Monitor', 'A 27-inch 4K monitor for stunning visuals and clarity.', 45),
('Keyboard', 'A mechanical keyboard with customizable RGB lighting.', 90),
('Mouse', 'An ergonomic wireless mouse with precision tracking.', 120);

create table price (
    price_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES product(product_id),
    price_amount decimal(10, 2) NOT NULL,
    price_date date NOT NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

create table users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_name varchar(50) NOT NULL,
    user_email varchar(40) UNIQUE NOT NULL,
    user_phone varchar(15) NOT NULL,
    user_account varchar(50) UNIQUE NOT NULL,
    user_password varchar(255) NOT NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

insert into users (user_name, user_email, user_phone, user_account, user_password) VALUES
('James Miller', 'james.miller@company.com', '+12025550101', 'james.miller', 'hashed_password_1'),
('Olivia Brown', 'olivia.brown@company.com', '+12025550102', 'olivia.brown', 'hashed_password_2'),
('Ethan Wilson', 'ethan.wilson@company.com', '+12025550103', 'ethan.wilson', 'hashed_password_3'),
('Sophia Taylor', 'sophia.taylor@company.com', '+12025550104', 'sophia.taylor', 'hashed_password_4'),
('Liam Anderson', 'liam.anderson@company.com', '+12025550105', 'liam.anderson', 'hashed_password_5'),
('Noah Thompson', 'noah.thompson@company.com', '+12025550106', 'noah.thompson', 'hashed_password_6'), 
('Emma Harris', 'emma.harris@company.com', '+12025550107', 'emma.harris', 'hashed_password_7'),
('Daniel Martinez', 'daniel.martinez@company.com', '+12025550108', 'daniel.martinez', 'hashed_password_8');

create table status (
    status_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status_name varchar(50) NOT NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

insert into status (status_name) VALUES
('Pending'),
('Processing'),
('Shipped'),
('Delivered'),
('Cancelled');

create table orders (
    orders_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customer(customer_id),
    users_id UUID NOT NULL REFERENCES users(users_id),
    orders_date date NOT NULL,
    orders_total decimal(10, 2) NOT NULL DEFAULT 0,
    status_id UUID NOT NULL REFERENCES status(status_id),
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

create table item (
    orders_id UUID NOT NULL REFERENCES orders(orders_id),
    product_id UUID NOT NULL REFERENCES product(product_id),
    item_quantity int NOT NULL,
    item_price decimal(10, 2) NOT NULL DEFAULT 0,
    PRIMARY KEY (orders_id, product_id),
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);




create or replace function set_updated_at()
returns trigger as $$
begin
    new.updated_at = current_timestamp;
    return new;
end;
$$ language plpgsql;

create trigger trg_customer_updated_at
before update on customer
for each row
execute function set_updated_at();

create trigger trg_product_updated_at
before update on product
for each row
execute function set_updated_at();

create trigger trg_price_updated_at
before update on price
for each row
execute function set_updated_at();

create trigger trg_staff_updated_at
before update on staff
for each row
execute function set_updated_at();

create trigger trg_users_updated_at
before update on users
for each row
execute function set_updated_at();

create trigger trg_status_updated_at
before update on status
for each row
execute function set_updated_at();

create trigger trg_orders_updated_at
before update on orders
for each row
execute function set_updated_at();

create trigger trg_item_updated_at
before update on item
for each row
execute function set_updated_at();