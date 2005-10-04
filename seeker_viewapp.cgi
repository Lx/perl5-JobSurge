#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  seeker_viewapp.cgi                                                         #
#                                                                             #
#  Written by Alex Peters, 21/9/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Verifies that a job seeker is logged in. Displays detailed information     #
#  on the user's application for the job identified by the specified ID,      #
#  ensuring first that the user has made an application.                      #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Ensure that a job seeker is logged in; get their ID if so
   my %seeker = assertSeekerLogin();

#  Get passed data
   my $jID = param('id');

#  Ensure that a valid job ID was passed; redirect to the main menu if not
   divert('seeker.cgi', MSG_BAD_JOB)
      unless elementInArray($jID, [getAppIDs($seeker{'id'})]);

#  Page output
   my $pageData;

#  Get information on the job
   my %job = getJobHash($jID);
#  Get information on the company offering the job
   my %company = getCompanyHash($job{cID});

#  Output information on the job
   $pageData .=
      jobBox(
         -job     => \%job,
         -company => \%company
      );

#  Get information on the application
   my %app = getAppHash($jID, $seeker{'id'});

#  Get the profile summary
   my $summary;
   open(FILE, PATH_SUMMARIES . "/$jID$seeker{id}.txt");
   flock(FILE, LOCK_SH);
   $summary .= $_ while (<FILE>);
   close(FILE);

#  Display information on the application
   $pageData .=
      lrBox(-values => [
         'Current position' =>
            b($app{position}),
         'Experience' =>
            b($app{experience}) . ' years',
         'Skills' =>
            (friendlyList($app{skills}, TRUE) || b('None')),
         'Minimum salary' =>
            b('$' . $app{salary}),
         'Profile summary' =>
            textarea(
               -readonly => 'readonly',
               -default => $summary,
               -rows => 10,
               -columns => 60
            )
      ]);

#  Output page
   printPage(
      'Application details',
      $pageData,
      myA('Main menu', 'seeker.cgi'),
      myA('Search', 'seeker_search.cgi'),
      myA('Apply', 'seeker_apply.cgi'),
      myA('Log out', 'seeker_login.cgi')
   );
