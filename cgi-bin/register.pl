#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use DBI;

#inicializando database
my $user = "alumno";
my $password = "pweb1";
my $dsn = "DBI:MariaDB:database=pweb1;host=192.168.0.36";
my $dbh = DBI->connect($dsn,$user,$password) or die ("No se pudo conectar!");

#inicializando variables del cgi, consulta e insercion
my $q = CGI->new; 
$user = $q->param("userName");
$password = $q->param("password");
my $firstName = $q->param("firstName");
my $lastName = $q->param("lastName");

#insercion a la base de datos
print $q->header("text/XML");
my $sth = $dbh->prepare("insert into Users (userName, password, firstName, lastName) values (?,?,?,?)");
$sth->execute($user, $password, $firstName, $lastName);

#consulta por si se agrego correctamente
$sth = $dbh->prepare("select userName, firstName, lastName from Users where userName = ? and password = ? and firstName = ? and lastName = ?");
$sth->execute($user, $password, $firstName, $lastName);

#XML
while (my @row = $sth->fetchrow_array){
	print <<XML;
<?xml version='1.0' encoding='utf-8'?>
	<user>
		<owner>$row[0]</owner>
		<firstName>$row[1]</firstName>
		<lastName>$row[2]</lastName>
	</user>
XML
}	

$sth->finish;
#Consultas al SGBD
$dbh->disconnect;

