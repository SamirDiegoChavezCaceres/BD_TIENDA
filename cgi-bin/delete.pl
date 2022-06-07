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
my $title = $q->param("title");

#consulta
print $q->header("text/XML");
my $sth = $dbh->prepare("delete from Articles where title=? and owner=?");
$sth->execute($title,$user);

$sth->finish;
#Consultas al SGBD
$dbh->disconnect;

