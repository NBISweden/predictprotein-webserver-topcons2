#!/usr/bin/perl -w
# show the queue status for all web-servers
# Created 2018-06-25, updated 2018-06-25, Nanjiang Shu
use CGI qw(:standard);
use CGI qw(:cgi-lib);
use CGI qw(:upload);

use Cwd 'abs_path';
use File::Basename;
my $rundir = dirname(abs_path(__FILE__));
# at proj
my $basedir = abs_path("$rundir/../pred");
my $auth_ip_file = "$basedir/config/auth_iplist.txt";#ip address which allows to run cgi script
my $name_targetprog = "qd_fe.py";
my $path_targetprog = "$basedir/app/$name_targetprog";
$path_targetprog = abs_path($path_targetprog);
my $progname = basename(__FILE__);

print header();
print start_html(-title => "show queue status ",
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
        my $content = `python $basedir/app/show_jobqueuestatus.py`;
        print $content;
        print "</pre>";
    }else{
        print "Permission denied!\n";
    }

    print '<br>';
    print end_html();
}

