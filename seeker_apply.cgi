#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  seeker_apply.cgi                                                           #
#                                                                             #
#  Written by Alex Peters, 2/9/2005-26/9/2005                                 #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Verifies that a job seeker is logged in. Allows the user to apply for a    #
#  specific job. Ensures that the job exists, that it has not expired and     #
#  that the user has not already applied for it.                              #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Ensure that a job seeker is logged in; get their ID if so
   my %seeker = assertSeekerLogin();

#  Form variables
   my ($fID, $fPos, $fYrs, $fSalary, @fSkills, $fSummary);

#  HTML output time!
   my $pageData;

   $fID = param('id');

#  Has the form been submitted?
   if (param('submit'))
   {
   #  Yes, the form has been submitted
   #  Read form data into variables
      $fPos     = param('position');
      $fYrs     = param('experience');
      @fSkills  = param('skills');
      $fSalary  = param('salary');
      $fSummary = param('summary');

   #  Error checking is broken up to conserve server resources (e.g. it is not
   #  desirable to check for the existance of a job ID if a form field is left
   #  blank)

   #  Ensure that no fields are blank or incorrectly entered
   #  (Don't check the ID validity yet -- there may be form errors?)
      my @errors;
      push(@errors,
         &emptyCheck($fID, 'job ID'),
         &emptyCheck($fPos, 'current position'),
         &emptyCheck($fYrs, 'minimum number of years'));
      push(@errors, &intCheck($fYrs, 'minimum number of years'))
         unless $fYrs eq '';
      push(@errors, &emptyCheck($fSalary, 'minimum salary'));
      push(@errors, &intCheck($fSalary, 'minimum salary'))
         unless $fSalary eq '';
      push(@errors, &emptyCheck($fSummary, 'profile summary'));
      push(@errors,
         "Fields cannot contain the '<b>" . htmlEncode(DELIM_PRIMARY) .
         "</b>' character.") if
         primaryDelimCheck($fID, $fPos, $fYrs, @fSkills, $fSalary);
      push(@errors,
         "Skills cannot contain the '<b>" . htmlEncode(DELIM_SECONDARY) .
         "</b>' character.") if secondaryDelimCheck(@fSkills);

      my ($jID, $jExp, $jYrs, $jSalary);
      unless (@errors)
      {
      #  All fields are correct (the job ID has not been checked yet)
         open(FILE, FILE_JOBS);
         flock(FILE, LOCK_SH);
         my @jobs = <FILE>;
         close(FILE);
         my $validJob = FALSE;
         foreach my $job (@jobs)
         {
            my $x;
            ($jID, $x, $x, $x, $x, $jExp, $jYrs, $x, $jSalary, $x) =
               split(DELIM_PRIMARY, $job);
            if ($jID eq $fID && !&dateHasExpired($jExp))
            {
               $validJob = TRUE;
               last;
            }
         }
         push(@errors, 'You have entered an <b>invalid job ID</b>.')
            unless $validJob;
      }

      unless (@errors)
      {
      #  The specified ID links to a non-expired job
         push(@errors, 'This job requests a <b>minimum of ' . $jYrs .
            ' years of experience</b>.') if $jYrs > $fYrs;
         push(@errors, 'You have requested a <b>minimum salary</b> greater ' .
            'than the <b>maximum of $' . $jSalary . '</b> offered for the ' .
            'position.') if $fSalary > $jSalary;
      }

      unless (@errors)
      {
      #  The job seeker meets the requirements of the offering
      #  Has the user already applied for this job?
         push(@errors, 'You have <b>already applied</b> for this position ' .
            '(<a href="seeker_viewapp.cgi?id=' . $fID . '">view</a>).')
            if elementInArray($fID, [getAppIDs($seeker{'id'})]);
      }

      unless (@errors)
      {
      #  The user has not already applied for this job and so the details can
      #  be written to disk
         open(RECORDS, '>>' . FILE_APPLICATIONS);
         flock(RECORDS, LOCK_EX);
         print RECORDS join(DELIM_PRIMARY, $jID, $seeker{'id'}, $fPos, $fYrs, 
            join(DELIM_SECONDARY, @fSkills), $fSalary), LF;
         close(RECORDS);
         open(SUMMARY, '>' . PATH_SUMMARIES . "/$jID$seeker{'id'}.txt");
         flock(SUMMARY, LOCK_EX);
         print SUMMARY $fSummary;
         close(SUMMARY);
         
      #  Redirect to the main menu indicating success
         divert('seeker.cgi', MSG_JOB_APPLIED);
      }

      $pageData .= formErrorPop(@errors) if @errors;
   }

#  Output the form
   $pageData .=
      myForm(
         -elements =>
            [
               'Job ID' => textfield('id', $fID, 5, 5) . '&nbsp; ' .
                  myA('Search...', 'seeker_search.cgi'),
               'Current position' => textfield('position', $fPos),
               'Experience' =>
                  textfield('experience', $fYrs, 2, 2) . '&nbsp; years',
               'Existing skills' =>
                  scalar(
                     checkbox_group('skills', [&getSkills()], [@fSkills], TRUE)
                  ),
               'Minimum salary' => textfield('salary', $fSalary, 6, 6),
               'Profile summary' => textarea('summary', $fSummary, 10, 60)
            ],
         -button => 'Apply',
         -validation => 'js_apply.js'
      );

#  Finish HTML output
   printPage(
      'Apply for a job',
      $pageData,
      myA('Main menu', 'seeker.cgi'),
      myA('Search', 'seeker_search.cgi'),
      myA('Log out', 'seeker_login.cgi')
      );
