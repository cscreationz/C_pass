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
     password_id   INT NOT NULL auto_increment,
     password_hash VARCHAR(255) NOT NULL,
     password_salt VARCHAR(255) NOT NULL,
     user_id       INT NOT NULL,
     PRIMARY KEY (password_id)
  );

CREATE INDEX user_account_id_fk_index ON "users" (account_id);

CREATE INDEX passwrods_user_id_fk_index ON "passwords" (user_id); 