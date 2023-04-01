CREATE TABLE accounts (Account_ID INT NOT NULL AUTO_INCREMENT, Account_Name VARCHAR(60) NOT NULL, Account_Description VARCHAR(90), PRIMARY KEY (Account_ID));
CREATE TABLE users (User_ID INT NOT NULL AUTO_INCREMENT, User_Name VARCHAR(50) NOT NULL, User_Email VARCHAR(100) NOT NULL, Account_ID INT NOT NULL, PRIMARY KEY (User_ID));
CREATE TABLE passwords (Password_ID INT NOT NULL AUTO_INCREMENT, Password_Hash VARCHAR(255) NOT NULL, Password_Salt VARCHAR(255) NOT NULL, User_ID INT NOT NULL, Primary key (Password_ID));
CREATE INDEX user_account_id_fk_index ON "users" (Account_ID);
CREATE INDEX passwrods_user_id_fk_index ON "passwords" (User_ID);
ALTER TABLE users
ADD CONSTRAINT fk_Account_ID
FOREIGN KEY (Account_ID)
REFERENCES accounts (Account_ID);
ALTER TABLE passwords
ADD CONSTRAINT fk_User_ID
FOREIGN KEY (User_ID)
REFERENCES users (User_ID);