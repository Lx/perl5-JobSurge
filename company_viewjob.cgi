#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  company_viewjob.cgi                                                        #
#                                                                             #
#  Written by Alex Peters, 2/9/2005-26/9/2005                                 #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Verifies that a company user is logged in. Displays detailed information   #
#  on the specified job, ensuring first that it belongs to the company        #
#  accessing it.                                                              #
#                                                                             #
#  May be diverted to this page when:                                         #
#  -  a new job is added                                                      #
#  -  a valid job seeker ID is not passed along with a valid job ID when      #
#     attempting to view an application's details                             #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Ensure that a company user is logged in; get their ID if so
   my %company = assertCompanyLogin();

#  Get passed data
   my $jID = param('id');

#  Attempt to get information pertaining to the given job
   my %job = getJobHash($jID);

#  Redirect to the main company page if a job ID wasn't passed, doesn't exist
#  or doesn't belong to the company accessing it
   if (!$jID || !%job || $job{'cID'} ne $company{'id'}) {
      divert('company.cgi', MSG_BAD_JOB); }

#  Assemble page output
   my $pageData;

#  Handle diversions to this page
   my $msg = getMsg();
   my $jobJustAdded = FALSE;
   if ($msg == MSG_JOB_ADDED)
   {
      $pageData .=
         msgBox(
            POP_INFO,
            h4('The job was successfully added.'),
            myA('Click here', "company.cgi"), 'to return to the main menu.'
         );
      $jobJustAdded = TRUE;
   }
   if ($msg == MSG_BAD_APP) {
   $pageData .=
      msgBox(
         POP_STOP,
         h4('An invalid job seeker ID was passed.'),
         'Please only select an application from the list below.'
      ); }

#  Embed deletion confirmation JavaScript
   $pageData .=
      '<script type="text/javascript" src="js_viewjob.js"></script>';

#  Output job details
   $pageData .=
      jobBox(
         -job => \%job,
         -footer =>
            myA(
               'Delete...',
               "company_deletejob.cgi?id=$jID",
               "deleteJob('$jID'); return false;"
            )
      );

#  Get applications for the specified ID
   my @apps = getAppsForJob($jID);

#  Output an applicant table or a message indicating no applications
   if (@apps)
   {
   #  Prepare a hash of job seeker ID/name pairs (so that applicants can be
   #  displayed by name and not by ID)
      my %sNames = getSIDFullNameHash();

   #  Prepare the rows
      my $appRows;
      foreach my $app (@apps)
      {
         my @record = split(DELIM_PRIMARY, $app);
         $appRows .=
            Tr(
               td([
                  myA(
                     $sNames{@record[1]},
                     "company_viewapp.cgi?jid=$jID&sid=@record[1]"
                  ),
                  @record[2],
                  "@record[3] years",
                  join(', ', split(DELIM_SECONDARY, @record[4])),
                  @record[5]
               ])
            );
      }

   #  Complete and output the table
      $pageData .=
         table(
            {-class=>'formBox', -width=>'100%'},
            Tr(td(
               {-colspan => 4, -style => 'padding-bottom: 8px'},
               h2((@apps > 1 ? @apps . ' applications' : 'One application')),
               'Select a job seeker for more information'
            )),
            Tr(th([
               'Job Seeker',
               'Current Position',
               'Experience',
               'Skills',
               'Min.<br />Salary'
            ])),
            $appRows
         );
   }
   elsif (!$jobJustAdded)
   {
      $pageData .=
         msgBox(POP_INFO, h4('No applications have been made for this job.'));
   }

#  Finish HTML output
   printPage(
      'Job details', $pageData,
      myA('Main menu', 'company.cgi'),
      myA('Add new job', 'company_newjob.cgi'),
      myA('Log out', 'company_login.cgi')
      );
