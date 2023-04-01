DROP DATABASE IF EXISTS password_manager;

CREATE DATABASE password_manager;

\c password_manager

CREATE TABLE IF NOT EXISTS accounts
  (
     account_id          BIGSERIAL NOT NULL,
     account_name        VARCHAR(60) NOT NULL,
     account_description VARCHAR(90),
     PRIMARY KEY (account_id)
  );

CREATE TABLE IF NOT EXISTS users
  (
     user_id    BIGSERIAL NOT NULL,
     user_name  VARCHAR(50) NOT NULL,
     user_email VARCHAR(100) NOT NULL,
     account_id INT NOT NULL,
     PRIMARY KEY (user_id)
  );

CREATE TABLE IF NOT EXISTS passwords
  (
     password_id   BIGSERIAL NOT NULL,
     password_hash VARCHAR(255) NOT NULL,
     password_salt VARCHAR(255) NOT NULL,
     user_id       INT NOT NULL,
     PRIMARY KEY (password_id)
  );

CREATE INDEX user_account_id_fk_index ON "users" (account_id);

CREATE INDEX passwrods_user_id_fk_index ON "passwords" (user_id);
ALTER TABLE users
ADD CONSTRAINT fk_Account_ID
FOREIGN KEY (Account_ID)
REFERENCES accounts (Account_ID);
ALTER TABLE passwords
ADD CONSTRAINT fk_User_ID
FOREIGN KEY (User_ID)
REFERENCES users (User_ID);