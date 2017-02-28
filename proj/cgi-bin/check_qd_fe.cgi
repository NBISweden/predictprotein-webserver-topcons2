#!/usr/bin/perl -w
# check the running process for the qd_fe.py
# Created 2015-04-10, updated 2017-02-28, Nanjiang Shu
use CGI qw(:standard);
use CGI qw(:cgi-lib);
use CGI qw(:upload);

use Cwd 'abs_path';
use File::Basename;
my $rundir = dirname(abs_path(__FILE__));
# at proj
my $basedir = abs_path("$rundir/../pred");
my $auth_ip_file = "$basedir/auth_iplist.txt";#ip address which allows to run cgi script
my $name_targetprog = "qd_fe.py";
my $path_targetprog = "$basedir/app/$name_targetprog";
$path_targetprog = abs_path($path_targetprog);
my $progname = basename(__FILE__);

print header();
print start_html(-title => "check if qd_fe.py is running",
    -author => "nanjiang.shu\@scilifelab.se",
    -meta   => {'keywords'=>''});

if(!param())
{
    my $remote_host = $ENV{'REMOTE_ADDR'};
    my @auth_iplist = ();
    open(IN, "<", $auth_ip_file) or die;
    while(<IN>) {
        chomp;
        push @auth_iplist, $_;
    }
    close IN;

    if (grep { $_ eq $remote_host } @auth_iplist) {
        print "<pre>";
        my $already_running=`ps aux  | grep  "$path_targetprog" | grep -v grep | grep -v archive_logfile | grep -v vim ` ;
        print $already_running;
        print "</pre>";
    }else{
        print "Permission denied!\n";
    }

    print '<br>';
    print end_html();
}

