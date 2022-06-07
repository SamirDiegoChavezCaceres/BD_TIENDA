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

#inicializando variables
my $q = CGI->new;
$user = $q->param("owner");

#consulta
print $q->header("text/XML");
my $sth = $dbh->prepare("select owner, title from Articles where owner=?");
$sth->execute($user);

#XML
print <<XML;
<?xml version="1.0" encoding="utf-8"?>
	<articles>
XML
while(my @row = $sth->fetchrow_array){
	print"<article>  
	<owner>$row[0]</owner>
	<title>$row[1]</title>
	</article>"
}	
print <<XML;
	</articles>
XML
$sth->finish;
#Consultas al SGBD
$dbh->disconnect;

