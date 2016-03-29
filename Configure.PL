#!/usr/bin/perl
use strict;
use warnings;
use Getopt::Long qw(:config no_ignore_case);

my $o_prefix = "/usr/local";
my $o_confdir = "/etc";
my $o_initdir = "/etc/init.d";
my $o_logdir = "/var/log";
my $o_libdir = "/var/lib";
my $o_rundir = "/var/run";
my $o_srvdir = "/srv";
my $o_perl = "/usr/bin/perl";
my $o_build_package = 0;
my $o_help = undef;

if (!-e "Makefile") {
    print "Execute me from the source directory!\n";
    exit 1;
}

GetOptions(
    "prefix=s" => \$o_prefix,
    "confdir=s" => \$o_confdir,
    "initdir=s" => \$o_initdir,
    "libdir=s" => \$o_libdir,
    "logdir=s" => \$o_logdir,
    "rundir=s" => \$o_rundir,
    "srvdir=s" => \$o_srvdir,
    "build-package" => \$o_build_package,
    "perl=s" => \$o_perl,
    "h|help" => \$o_help
);

if ($o_help) {
    print "Usage: perl Configure.PL [ OPTIONS ]\n\n";
    print "Configure options:\n\n";
    print "  --prefix DIR (default: $o_prefix)\n";
    print "  --confdir DIR (default: $o_confdir)\n";
    print "  --initdir DIR (default: $o_initdir)\n";
    print "  --logdir DIR (default: $o_logdir)\n";
    print "  --rundir DIR (default: $o_rundir)\n";
    print "  --srvdir DIR (default: $o_srvdir)\n";
    print "  --perl PERL EXECUTABLE (default: $o_perl)\n";
    print "\n";
    exit 0;
}

open my $fh, ">", "Makefile.config" or die "Unable to overwrite Makefile - $!";

print "Writing Makefile.config ...\n";

print $fh <<EOF;
# Base paths
PREFIX=\$(DESTDIR)$o_prefix
CONFDIR=\$(DESTDIR)$o_confdir
INITDIR=\$(DESTDIR)$o_initdir
LIBDIR=\$(DESTDIR)$o_libdir
LOGDIR=\$(DESTDIR)$o_logdir
RUNDIR=\$(DESTDIR)$o_rundir
SRVDIR=\$(DESTDIR)$o_srvdir
USRLIBDIR=\$(DESTDIR)$o_prefix/lib
BUILDPKG=$o_build_package
PERL=$o_perl
EOF

close $fh;

print "Done.\n";
