#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  company.cgi                                                                #
#                                                                             #
#  Written by Alex Peters, 25/8/2005-24/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Verifies that a company user is logged in. Displays past and present       #
#  offerings with links to more information. Provides links to add new jobs   #
#  and log out.                                                               #
#                                                                             #
#  May be diverted to this page when:                                         #
#  -  a valid job ID is not passed to another company page                    #
#  -  a job is deleted                                                        #
#  -  a new company has successfully registered                               #
#  -  an existing company has attempted to re-register but has given cred-    #
#     entials matching those on file                                          #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Ensure that a company user is logged in; get their ID if so
   my %company = assertCompanyLogin();

#  Load jobs owned by this company into one of two arrays according to status
   my (@pastJobs, @presentJobs);
   open(RECORDS, FILE_JOBS);
   flock(RECORDS, LOCK_SH);
   while (my $record = <RECORDS>)
   {
      chomp($record);
      my @fields = split(DELIM_PRIMARY, $record);
      if ($fields[1] eq $company{'id'})
      {
      #  The job belongs to this company
         if (dateHasExpired($fields[5])) {
            push(@pastJobs, $record); }
         else {
            push(@presentJobs, $record); }
      }
   }
   close(RECORDS);

#  Assemble page output
   my $pageData;

#  Handle diversions to this page
   my $msg = getMsg();
   if ($msg == MSG_JOB_REMOVED) {
      $pageData .= msgBox(POP_INFO, h4('The job has been deleted.')); }
   if ($msg == MSG_BAD_JOB) {
      $pageData .= msgBox(POP_STOP, h4('An invalid job ID was passed.'),
         'Please only select a job from the list below.'); }
   if ($msg == MSG_COMPANY_EXISTS) {
      $pageData .=
         msgBox(
            POP_INFO,
            h4('Your company is already registered with JobSurge.'),
            'You provided the same login credentials as when you registered,',
            'so you have been logged in.'
         ); }
   if ($msg == MSG_NEW_COMPANY) {
      $pageData .=
         msgBox(
            POP_SMILE,
            h4(
               'Congratulations!', 
               'Your company is now registered with JobSurge.'
            ),
            'Here is a copy of your details:',
            ul(li([
               "Your JobSurge company ID is <b>$company{'id'}</b>",
               "Your company is <b>$company{'name'}</b> " .
                  "(ABN <b>$company{'abn'}</b>)",
               "Your company is a <b>\l$company{'type'} organisation</b>",
               "Your company address is <b>$company{'address'}</b>",
               "Your company contact is <b>$company{'contact'}</b>:" .
                  ul(li([
                     "Phone: <b>$company{'phone'}</b>",
                     'Email: <a href="mailto:' . $company{'email'} . '"><b>' .
                        $company{'email'} . '</b></a>'
                  ])),
               "Your company username is <b>$company{'user'}</b>"
            ]))
         ); }

#  Construct tables of past and current jobs belonging to this company
   my $newJobLink =
      myA('Click here', 'company_newjob.cgi') . ' to add a new job.';
   if (@pastJobs || @presentJobs)
   {
   #  The company has past and/or present jobs to be displayed
   #  Get an application count for each job
      my %numApps = getJobAppCountHash();

   #  Output a table of past jobs if any
      if (@pastJobs) {
         $pageData .= offeringTable('Past offerings', \@pastJobs, \%numApps); }

   #  Output a table of present jobs or a message indicating no present jobs
      if (@presentJobs) {
         $pageData .=
            offeringTable('Present offerings', \@presentJobs, \%numApps); }
      else {
         $pageData .=
            msgBox(POP_INFO, h4('This company has no present offerings.'),
            $newJobLink); }
   }
   else
   {
   #  The company has no jobs to be displayed
      $pageData .=
         msgBox(POP_INFO, h4('This company has no past or present offerings.'),
            $newJobLink);
   }

   printPage(
      "Main menu for $company{'name'}",
      $pageData,
      myA('Add new job', 'company_newjob.cgi'),
      myA('Log out', 'company_login.cgi')
   );
