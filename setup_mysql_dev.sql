--  a script that prepares a MySQL server for the project

-- create the database `hbnb_dev_db`
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- create the user `hbnb_dev` (in localhost) with passowrd `hbnb_dev_pwd`
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- grant all privileges on only the database `hbnb_dev_db` to user `hbnb_dev`
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- grant the SELECT privilege on only the database `performance_schema` to user `hbnb_dev`
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
