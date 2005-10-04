#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  company_newjob.cgi                                                         #
#                                                                             #
#  Written by Alex Peters, 28/8/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Verifies that a company user is logged in. Accepts information on a new    #
#  job offering and creates the necessary record.                             #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Ensure that a company user is logged in; get their ID if so
   my %company = assertCompanyLogin();

#  Define outcome constants
   use constant OC_BAD_DATA => 1;
   use constant OC_SUCCESS  => 2;

#  Declare the necessary variables
   my @errors;
#  $f... = form data
   my ($fTitle, $fType, $fLoc, $fExp, $fYrs, @fSkills, $fSalary);

#  If the form was submitted then start processing it
   if (param('submit'))
   {
   #  Get the form data into variables
      $fTitle  = param('title');
      $fType   = param('type');
      $fLoc    = param('location');
      $fExp    = param('expiry');
      $fYrs    = param('experience');
      @fSkills = param('skills');
      $fSalary = param('salary');
   #  Validation
      push(@errors,
         emptyCheck($fTitle, 'job title'),
         choiceCheck($fType, 'job type', JOB_TYPES),
         choiceCheck($fLoc, 'location', JOB_LOCATIONS));
      push(@errors, dateCheck($fExp, 'expiry date'));
      push(@errors, emptyCheck($fYrs, 'minimum number of years'));
      push(@errors, intCheck($fYrs, 'minimum number of years'))
         unless $fYrs eq '';
      push(@errors, emptyCheck($fSalary, 'maximum salary'));
      push(@errors, intCheck($fSalary, 'maximum salary'))
         unless $fSalary eq '';
   #  -  Should incorporate server-side skill validation (all skills match the
   #     list of given ones)?
      push(@errors,
         "Fields cannot contain the '<b>" . htmlEncode(DELIM_PRIMARY) .
         "</b>' character.") if primaryDelimCheck($fTitle, $fType, $fLoc,
         $fExp, $fYrs, @fSkills, $fSalary);
      push(@errors,
         "Skills cannot contain the '<b>" . htmlEncode(DELIM_SECONDARY) .
         "</b>' character.") if secondaryDelimCheck(@fSkills);


   #  If there are form errors then we shouldn't process any further
      unless (@errors)
      {
         my $maxID = 0;
      #  Do any jobs currently exist?
         if (-e FILE_JOBS)
         {
         #  Open the file to determine the current maximum ID; this needs to be
         #  exclusively locked (so that two instances don't see the same
         #  maximum ID and then write a record with the next up)
            open(RECORDS, '+<' . FILE_JOBS);
            flock(RECORDS, LOCK_EX);
         #  Get the maximum job ID
            while (my $record = <RECORDS>)
            {
               my ($rID, $x) = split(DELIM_PRIMARY, $record);
               $rID = &intFromID($rID);
               $maxID = $rID if $rID > $maxID;
            }
         }
         else
         {
            open(RECORDS, '>' . FILE_JOBS);
            flock(RECORDS, LOCK_EX);
         }
      #  We are now pointing at the end of the file, ready to append
      #  The ID of this record will be the maximum + 1
         $maxID++;
         $maxID = &idFromInt('j', $maxID);
      #  Write data to end of file
         print RECORDS join(DELIM_PRIMARY, $maxID, $company{'id'}, $fTitle,
            $fType, $fLoc, $fExp, $fYrs, join(DELIM_SECONDARY, @fSkills),
            $fSalary), LF;
         close(RECORDS);
      #  Indicate success
         divert("company_viewjob.cgi?id=$maxID", MSG_JOB_ADDED);
      }
   }
#  Otherwise form was not submitted

#  HTML output time!
   my $pageData;

#  Determine necessary output
#  There was an error in the form data or the form was not submitted
   $pageData .= formErrorPop(@errors) if @errors;
#  Output the form
   my $skillHTML = checkbox_group('skills', [getSkills()], [@fSkills], TRUE);
   $pageData .=
      myForm(
         -elements =>
            [
               'Job title' => textfield('title', $fTitle),
               'Job type' => popup_menu('type', [JOB_TYPES], $fType),
               'Location' => popup_menu('location', [JOB_LOCATIONS], $fLoc),
               'Expiry date (<b>d/m/yyyy</b>)' =>
                  textfield('expiry', $fExp, 10, 10),
               'Minimum experience as<br />a software developer' =>
                  textfield('experience', $fYrs, 2, 2) . '&nbsp; year/s',
               'Skills required' => $skillHTML,
               'Maximum salary' => textfield('salary', $fSalary, 6, 6)
            ],
         -button => 'Add',
         -validation => 'js_newjob.js'
      );

#  Finish HTML output
   printPage(
      'Add new job',
      $pageData,
      myA('Main menu', 'company.cgi'),
      myA('Log out', 'company_login.cgi')
      );
