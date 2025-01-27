CREATE  DATABASE flask_usuarios_app;
USE flask_usuarios_app;


CREATE TABLE usuarios(
    id INT  UNSIGNED PRIMARY KEY   AUTO_INCREMENT,
    nombre VARCHAR(150),
    apellidos VARCHAR(200),
    email VARCHAR(150) NOT NULL UNIQUE ,
    password VARCHAR(255)
);
