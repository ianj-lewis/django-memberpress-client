DROP USER IF EXISTS `mp_user`@`localhost`;
DROP DATABASE IF EXISTS `memberpress_client`;

CREATE USER `mp_user`@`localhost` IDENTIFIED BY 'mp';
CREATE DATABASE `memberpress_client`;
GRANT ALL PRIVILEGES ON `memberpress_client`.* TO "mp_user"@"localhost";
FLUSH PRIVILEGES;
