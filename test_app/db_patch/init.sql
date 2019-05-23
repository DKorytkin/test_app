
CREATE TYPE roles as ENUM (
    'admin',
    'manager',
    'user'
);


CREATE TABLE IF NOT EXISTS accounts (
    id serial PRIMARY KEY,
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    email VARCHAR (355) UNIQUE NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
    date_edited TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
    role roles
);


CREATE TABLE IF NOT EXISTS orders(
    id serial PRIMARY KEY,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
    date_edited TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
    account_id int references accounts(id)
);


CREATE TABLE IF NOT EXISTS products(
    id serial PRIMARY KEY,
    name VARCHAR(200),
    price INTEGER,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
    date_edited TIMESTAMP NOT NULL DEFAULT CURRENT_DATE
);


CREATE TABLE IF NOT EXISTS carts (
    id serial PRIMARY KEY,
    order_id    int REFERENCES orders(id) ON UPDATE CASCADE ON DELETE CASCADE,
    product_id int REFERENCES products(id) ON UPDATE CASCADE ON DELETE CASCADE
);
