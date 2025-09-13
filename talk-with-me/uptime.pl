#!/usr/bin/env perl
use warnings;
use strict;

my $uptime = '';
my $prev   = '';

{
   ($uptime) = `uptime` =~ /load average:(.*)/;
   print "$uptime\n" unless $uptime eq $prev;
   $prev = $uptime;
   sleep 2;
   redo;
}
