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
$user = $q->param("owner");
my $title = $q->param("title");

#consulta
my $sth = $dbh->prepare("select title, text from Articles where title = ? and owner = ?");
$sth->execute($title, $user);

#xml
print $q->header("text/XML");
while (my @row = $sth->fetchrow_array){
	print <<XML;
<?xml version='1.0' encoding='utf-8'?>
	<article>
		<owner>$user</owner>
		<title>$row[0]</title>
		<text>$row[1]</text>
	</article>
XML
}	
$sth->finish;
#Consultas al SGBD
$dbh->disconnect;

