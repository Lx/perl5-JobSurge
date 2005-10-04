#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  seeker.cgi                                                                 #
#                                                                             #
#  Written by Alex Peters, 3/9/2005-24/9/2005                                 #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Verifies that a job seeker is logged in. Displays all applications made    #
#  by the job seeker with links to more information. Provides links to        #
#  search and apply for jobs and to log out.                                  #
#                                                                             #
#  May be diverted to this page when:                                         #
#  -  a job seeker logs in                                                    #
#  -  a valid job ID is not passed to the 'view application' page             #
#  -  a new job seeker has successfully registered                            #
#  -  an existing job seeker has attempted to re-register but has given       #
#     credentials matching those on file                                      #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Ensure that a job seeker is logged in; get their ID if so
   my %seeker = assertSeekerLogin();

#  Get applications made by this job seeker
   my @apps = getAppsForSeeker($seeker{'id'});

#  Assemble page output  
   my $pageData;

#  Output any necessary popups
   my $msg = getMsg();
   if ($msg == MSG_BAD_JOB) {
      $pageData .=
         msgBox(
            POP_STOP,
            h4('An invalid job ID was passed.'),
            'Please only select a job from the list below.'
         ); }
   if ($msg == MSG_NEW_SEEKER) {
      $pageData .=
         msgBox(
            POP_SMILE,
            h4(
               'Congratulations! You are now a JobSurge member.'
            ),
            'Here is a copy of your details:',
            ul(li([
               "Your JobSurge seeker ID is <b>$seeker{id}</b>",
               "Your name is <b>\u$seeker{fName} \u$seeker{lName}</b>",
               "Your phone number is a <b>$seeker{phone}</b>",
               "Your address is <b>$seeker{address}</b>",
               'Your Email address is <a href="mailto:' . $seeker{email} .
                  '"><b>' . $seeker{email} . '</b></a>',
               "Your username is <b>$seeker{user}</b>"
            ]))
         ); }
   if ($msg == MSG_SEEKER_EXISTS) {
      $pageData .=
         msgBox(
            POP_INFO,
            h4('You are already a JobSurge member.'),
            'You provided the same login credentials as when you registered,',
            'so you have been logged in.'
         ); }
   $pageData .= msgBox(
      POP_SMILE,
      h4('You have successfully applied for the job.'), 'Best of luck.')
      if $msg == MSG_JOB_APPLIED;

#  Construct table of applications if any have been made
   if (@apps)
   {
   #  Populate a hash of company ID/name pairs
      my %cNames = getCompanyIDNameHash();
     
   #  Populate a hash of job ID/title pairs and a hash of job ID/company ID
   #  pairs
      my (%jTitles, %jCompanies);
      open(RECORDS, FILE_JOBS);
      flock(RECORDS, LOCK_SH);
      while (my $record = <RECORDS>)
      {
         my ($jID, $jCompany, $jTitle, $x) = split(DELIM_PRIMARY, $record);
         $jTitles{$jID} = $jTitle;
         $jCompanies{$jID} = $jCompany;
      }
      close(RECORDS);
      my $appRows;
      foreach my $jID (@apps)
      {
         $appRows .=
            Tr(td([
               myA($jID, "seeker_viewapp.cgi?id=$jID"),
               $jTitles{$jID},
               $cNames{$jCompanies{$jID}}
            ]));
      }
      $pageData .=
         table(
            {-class => 'formBox', -width => '100%'},
            Tr(td(
                  {-colspan => 3, -style => 'padding-bottom: 8px'},
                  h2('My applications'),
                  'Select a job ID for more information'
            )),
            Tr(th([
                  'Job ID',
                  'Position',
                  'Company'
            ])),
            $appRows
         );
   }
   else
   {
      $pageData .=
         msgBox(
            POP_INFO,
            h4('You currently have no applications on offer.'),
            'You may wish to <a href="seeker_search.cgi">search for a job',
            'now</a>.'
         );
   }

   printPage(
      "Main menu for \u$seeker{'fName'} \u$seeker{'lName'}",
      $pageData,
      myA('Search', 'seeker_search.cgi'),
      myA('Apply', 'seeker_apply.cgi'),
      myA('Log out', 'seeker_login.cgi')
   );
