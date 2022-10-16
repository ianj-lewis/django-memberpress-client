DROP USER IF EXISTS `mp-user`@`localhost`;
DROP DATABASE IF EXISTS `mp-db`;

CREATE USER `mp-user`@`localhost` IDENTIFIED BY 'mp';
CREATE DATABASE `mp-db`;
GRANT ALL PRIVILEGES ON `mp-db`.* TO "mp-user"@"localhost";
FLUSH PRIVILEGES;
