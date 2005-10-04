#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  company_viewapp.cgi                                                        #
#                                                                             #
#  Written by Alex Peters, 21/9/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Verifies that a company user is logged in. Displays detailed information   #
#  on the application identified by a job ID and job seeker ID, ensuring      #
#  first that the job belongs to the company accessing it and that the job    #
#  seeker specified has applied for it.                                       #
#                                                                             #
#  May be diverted to this page when:                                         #
#  -  an applicant has been notified about an interview                       #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Ensure that a company user is logged in
   my %company = assertCompanyLogin();

#  Get passed data
   my ($jID, $sID) = (param('jid'), param('sid'));

#  Get information on job
   my %job = getJobHash($jID);

#  Redirect if a valid job ID wasn't specified
   if (!$jID || !%job || $job{'cID'} ne $company{'id'}) {
      divert('company.cgi', MSG_BAD_JOB); }

#  Ensure that the specified job seeker has applied for this job; redirect to
#  the Job Details page if not
   divert("company_viewjob.cgi?id=$jID", MSG_BAD_APP)
      unless elementInArray($sID, [getSeekers($jID)]);

#  Assemble page output
   my $pageData;

#  Handle diversions to this page
   my $msg = getMsg();
   if ($msg == MSG_SEEKER_NOTIFIED) {
      $pageData .=
         msgBox(
            POP_INFO,
            h4('The applicant has been notified via Email.'),
            myA('Click here', "company_viewjob.cgi?id=$jID"),
            'to return to the Job Detail page.'
         ); }

#  Get information on the application
   my %app = getAppHash($jID, $sID);
#  Get information on the job seeker
   my %seeker = getSeekerHash($sID);

#  Get the application summary
   my $summary;
   open(FILE, PATH_SUMMARIES . "/$jID$sID.txt");
   flock(FILE, LOCK_SH);
   $summary .= $_ while (<FILE>);
   close(FILE);

#  Output the application information and an interview link
   $pageData .=
      lrBox(
         -values => [
            'Applicant' =>
               b("$seeker{fName} $seeker{lName}"),
            'Phone number' =>
               b($seeker{phone}),
            'Email address' =>
               myA(b($seeker{email}), "mailto:$seeker{email}"),
            'Current position' =>
               b($app{position}),
            'Experience' =>
               b($app{experience}) . ' years',
            'Skills'=>
               (friendlyList($app{skills}, TRUE) || b('None')),
            'Minimum salary' =>
               b('$' . $app{salary}),
            'Profile summary' =>
               textarea(
                  -readonly => 'readonly',
                  -default  => $summary,
                  -rows     => 10,
                  -columns  => 60
               )
         ],
         -footer =>
            myA(
               'Arrange interview with applicant',
               "company_contact.cgi?jid=$jID&sid=$sID"
            )
      );

#  Output page
   printPage(
      "$job{title} application",
      $pageData,
      myA('Job details', "company_viewjob.cgi?id=$jID"),
      myA('Main menu', 'company.cgi'),
      myA('Add new job', 'company_newjob.cgi'),
      myA('Log out', 'company_login.cgi')
   );
