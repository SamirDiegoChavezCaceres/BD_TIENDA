#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use DBI;

#Inicializando database
my $user = "alumno";
my $password = "pweb1";
my $dsn = "DBI:MariaDB:database=pweb1;host=192.168.0.36";
my $dbh = DBI->connect($dsn,$user,$password) or die ("No se pudo conectar!");
#inicializando variables del cgi
my $q = CGI->new;
$user = $q->param("userName");
$password = $q->param("password");

print $q->header("text/XML");
my $sth = $dbh->prepare("select userName, firstName, lastName from Users where userName=? and password=?");
$sth->execute($user, $password);

#generandoXML
while (my @row = $sth->fetchrow_array){
	print <<XML;
<?xml version='1.0' encoding='utf-8'?>\n
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

