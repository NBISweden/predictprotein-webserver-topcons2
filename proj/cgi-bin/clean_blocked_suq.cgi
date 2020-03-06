#!/usr/bin/perl -w
# check if the suq queue is hang, if so, clean it
#Created 2016-02-29, updated 2018-09-03, Nanjiang Shu
use CGI qw(:standard);
use CGI qw(:cgi-lib);
use CGI qw(:upload);

use Cwd 'abs_path';
use File::Basename;
my $rundir = dirname(abs_path(__FILE__));
# at proj
my $basedir = abs_path("$rundir/../");
my $progname = basename(__FILE__);
my $logpath = "$basedir/pred/static/log";
my $errfile = "$logpath/$progname.err";
my $path_result = "$basedir/pred/static/result";
my $auth_ip_file = "$basedir/pred/config/auth_iplist.txt";#ip address which allows to run cgi script
my $suq = "/usr/bin/suq";
my $suqbase = "/tmp";

print header();
print start_html(-title => "clean blocked suq queue",
    -author => "nanjiang.shu\@scilifelab.se",
    -meta   => {'keywords'=>''});

my $remote_host = $ENV{'REMOTE_ADDR'};

my @auth_iplist = ();
open(IN, "<", $auth_ip_file) or die;
while(<IN>) {
    chomp;
    push @auth_iplist, $_;
}
close IN;

my $threshold = 8;
if (grep { $_ eq $remote_host } @auth_iplist) {
    my $command =  "pgrep suq | wc -l ";
    $numsuqjob = `$command`;
    chomp($numsuqjob);
    my $idx_first_wait_job = `$suq -b $suqbase ls | awk '{if (\$3=="Running" || \$3=="Wait") print}' | awk '{if(\$3=="Wait") print NR}' | head -n 1 2>>$errfile`;

    print "<pre>";
    if ($numsuqjob >= $threshold || $idx_first_wait_job == 1 ){
        print "numsuqjob = $numsuqjob >= $threshold. Try to clean the queue\n";
        `rm -rf /scratch/.suq ; rm -rf /tmp/.suq.*/; pgrep suq | xargs kill `;
        print "rm -rf /scratch/.suq ; rm -rf /tmp/.suq.*/; pgrep suq | xargs kill\n\n";
        # then delete non started jobs
        `for folder in \$(find $path_result  -maxdepth 1  -type d -name "rst_*"); do if [ ! -f \$folder/runjob.start ];then  rm -rf \$folder;fi; done`;
        print "for folder in \$(find $path_result  -maxdepth 1  -type d -name \"rst_*\"); do if [ ! -f \$folder/runjob.start ];then  rm -rf \$folder;fi; done\n\n";
    }else{
        print "suq queue is normal\n";
    }
    print "</pre>";
}else{
    print "Permission denied!\n";
}

print '<br>';
print end_html();

