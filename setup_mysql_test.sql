--  a script that prepares a MySQL server for the project

-- create the database `hbnb_test_db`
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- create the user `hbnb_test` (in localhost) with passowrd `hbnb_test_pwd`
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- grant all privileges on only the database `hbnb_test_db` to user `hbnb_test`
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- grant the SELECT privilege on only the database `performance_schema` to user `hbnb_test`
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
