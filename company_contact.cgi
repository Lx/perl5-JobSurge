#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  company_contact.cgi                                                        #
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

#  Ensure that a company user is logged in; get their ID if so
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

#  Form variables
   my ($fDate, $fTime, $fLoc, @errors);

#  If the form was submitted then start processing it
   if (param('submit'))
   {
   #  Get the form data
      $fDate = param('date');
      $fTime = param('time');
      $fLoc  = param('location');

   #  Ensure that no fields are left blank
   #  Validate fields with data
      push(@errors,
         dateCheck($fDate,  'interview date'),
         emptyCheck($fTime, 'interview time'),
         emptyCheck($fLoc,  'interview location')      
      );

      unless (@errors)
      {
      #  There were no errors in the form data
      #  Get the necessary information to add into the Email

      #  Get the necessary job seeker details
         my %seeker = getSeekerHash($sID);

      #  Contact the applicant
         use Text::Wrap;
         local($Text::Wrap::columns) = 72;
         open(MAIL, '|'. PATH_SENDMAIL . ' -t -oi > /dev/null');
         print MAIL
            'From: JobSurge <no-reply@jobsurge.com.au>', LF,
            "Reply-To: $company{'name'} <$company{'email'}>", LF,
            "To: \u$seeker{'fName'} \u$seeker{'lName'} <$seeker{'email'}>", LF,
            "Subject: [JobSurge] $job{'title'} application successful", LF,
            LF,
            "Dear \u$seeker{'fName'},", LF,
            LF,
            wrap('', '', "   Congratulations -- $company{'name'} has accepted your application for the '$job{'title'}' position and an interview has been arranged. Please note the following details:"), LF,
            LF,
            wrap('   Date: ', '      ', $fDate), LF,
            wrap('   Time: ', '      ', $fTime), LF,
            wrap('   Location: ', '      ', $fLoc), LF,
            LF,
            wrap('', '', "   If the date and time above are not convenient for you then please contact $company{'name'} by phone on $company{'phone'} to discuss an alternative plan of action."), LF,
            LF,
            wrap('', '', "   Once again congratulations on your achievement and thank you for using JobSurge."), LF,
            LF,
            '-- ', LF,
            LF,
            'Best wishes,', LF,
            wrap('', '', "The team at JobSurge (on behalf of $company{'name'})"), LF;
         close(MAIL);
         divert("company_viewapp.cgi?jid=$jID&sid=$sID", MSG_SEEKER_NOTIFIED);
      }
   }

#  Assemble page output
   my $pageData;

#  There was an error in the form data or the form was not submitted
   $pageData .= formErrorPop(@errors) if scalar(@errors);
#  Output the form
   $pageData .=
      myForm(
         -elements =>
            [
               'Interview date' => textfield('date', $fDate),
               'Interview time' => textfield('time', $fTime),
               'Interview location' => textfield('location', $fLoc)
            ],
         -hiddens =>
            [
               'jid' => $jID,
               'sid' => $sID
            ],
         -button => 'Notify',
         -validation => 'js_contact.js'
      );

#  Finish HTML output
   printPage(
      'Arrange interview with applicant',
      $pageData,
      myA('Application details', "company_viewapp.cgi?jid=$jID&sid=$sID"),
      myA('Job details',         "company_viewjob.cgi?id=$jID"),
      myA('Main menu',           'company.cgi'),
      myA('Add new job',         'company_newjob.cgi'),
      myA('Log out',             'company_login.cgi')
      );
