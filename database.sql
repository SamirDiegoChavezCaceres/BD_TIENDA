DROP TABLE IF EXISTS Articles;
DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
	userName varchar(100) PRIMARY KEY,
	password varchar(255) NOT NULL,
	lastName varchar(255) NOT NULL,
	firstName varchar(255)
);
insert into Users (userName, password, lastName, firstName) values ('administrador', 'pweb1', 'Sistemas', 'Administrador');

CREATE TABLE Articles(
	title varchar(255) NOT NULL,
	owner varchar(100) NOT NULL, 
	text varchar(1024) NOT NULL,
	PRIMARY KEY (title, owner),
	FOREIGN KEY (owner) REFERENCES Users(userName)
);
