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
print $q->header("text/HTML");
my $sth = $dbh->prepare("select text from Articles where owner=? and title=?");
$sth->execute($user, $title);

#HTML y conversion
my @arr;
while(my @row = $sth->fetchrow_array){
	@arr = &stringToArray($row[0]);
	my $abre = 1;
	my $remplace = "";
	foreach my $line (@arr){
		if (1 == $abre){
			if ($line =~ /#{6} /) {
				$line =~ s/###### /<h6>/g;
				chomp($line);
				$line = "$line<\/h6>\n";
			} if ($line =~ /#{2} /) {
				$line =~ s/## /<h2>/g;
				chomp($line);
				$line = "$line<\/h2>\n";
			} if ($line =~ /# /) {
				$line =~ s/# /<h1>/g;
				chomp($line);
				$line = "$line<\/h1>\n";
			} if ($line =~ /^\n/) {
				$line =~ s/\n/<br>/g;
				chomp($line);
				$line = "$line\n";
			} if ($line =~ /\*{3}(.*)\*{3}/) {
				$remplace = "<strong>$1<\/strong>";
				$line =~ s/\*\*\*$1\*\*\*/$remplace/g;
			} if ($line =~ /\*{2}(.*)\*{2}/) { 
				$remplace = "<strong>$1<\/strong>";
				$line =~ s/\*\*$1\*\*/$remplace/g;
			} if ($line =~ /\*(.*)\*/) {
				$remplace = "<em>$1<\/em>";
				$line =~ s/\*$1\*/$remplace/g;
			} if ($line =~ /~{2}(.*)~{2}/) {
				$remplace = "<del>$1<\/del>";
				$line =~ s/~~$1~~/$remplace/g;
			} if ($line =~ /_(.*)_/) {
				$remplace = "<em>$1<\/em>";
				$line =~ s/_$1_/$remplace/g;
			} if ($line =~ /```/) {
				$line =~ s/```/<pre>/g;
				chomp($line);
				$line = "$line\n";
				$abre = 0;
			} if ($line =~ /(\[(.*)\])(\((.*)\))/) {
				$remplace = "<a href=\"$4\">$2</a>";
				$line =~ s/\[$2\]\($4\)/$remplace/g;
				chomp($line);
				$line = "$line\n";
			} if ($line !~ /^\</) {
				$line = "<p>$line";
				chomp($line);
				$line = "$line<\/p>\n";
			}
			print $line;
		} else {
			if ($line =~ /```/) {
				$line =~ s/```/<\/pre>/g;
				chomp($line);
				$line = "$line\n";
				print "$line";
				$abre = 1;
			} else {
				print "$line";
			}
		}
	}	
}
$sth->finish;
$dbh->disconnect;

sub stringToArray{
	my $stringCopy = $_[0];
	my @arr;
	my $i = 0; 
	while($stringCopy =~ /(.*)\n/){
		$arr[$i] = "$1\n";
		$stringCopy =~ s/(.*)\n//;
		$i++;
	}
	return @arr;
}
sub stringToArray{
	my $stringCopy = $_[0];
	my @arr;
	my $i = 0; 
	while($stringCopy =~ /(.*)\n/){
		$arr[$i] = "$1\n";
		$stringCopy =~ s/(.*)\n//;
		$i++;
	}
	$arr[$i] = $stringCopy;
	return @arr;
}
