#!/usr/bin/perl -w

# Description: check the jobqueue status and send email 

# Created 2020-08-13, updated 2020-08-13, Nanjiang Shu

use File::Temp;

use Cwd 'abs_path';
use File::Basename;
use POSIX qw(strftime);

use LWP::Simple qw($ua head);
$ua->timeout(10);

my $rundir = dirname(abs_path(__FILE__));
my $basedir = abs_path("$rundir/../");
require "$rundir/nanjianglib.pl";
my $FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S %Z';

my $date = strftime "$FORMAT_DATETIME", localtime;
print "\n#===================\nDate: $date\n";
my $servername = "TOPCONS2";
my $target_qd_script_name = "qd_fe.py";
my $computenodelistfile = "$basedir/config/computenode.txt";
my $alert_emaillist_file = "$basedir/config/alert_email.txt";
my $from_email = "nanjiang.shu\@scilifelab.se";
my $title = "";
my $output = "";

my @to_email_list = ReadList($alert_emaillist_file);


# run the script show_jobqueuestatus.py and send the result by email
$title = "Webserver jobqueue status";
$output = `python2 $rundir/show_jobqueuestatus.py`;
# add html format
#$output = "<html><body><p><pre>$output</pre></p></body></html>";
foreach my $to_email(@to_email_list) {
    sendmail($to_email, $from_email, $title, $output);
    #sendmailHTML($to_email, $from_email, $title, $output);
}

