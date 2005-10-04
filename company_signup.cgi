#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  company_signup.cgi                                                         #
#                                                                             #
#  Written by Alex Peters, 31/8/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Accepts signup information from and registers a new company. Ensures that  #
#  all fields are populated. Prevents double signups by checking for dupli-   #
#  cate ABNs. Forces unique usernames for each company user.                  #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Define variables needing script-wide scope
   my (@errors, $maxID, $pageData);
   my ($fName, $fABN, $fType, $fAddr, $fContact, $fPhone, $fEmail, $fUser,
      $fPass);

   if (param('submit'))
   {
   #  Form has been submitted
   #  Get the form data into variables
      $fName    = param('name');
      $fABN     = param('abn');
      $fType    = param('type');
      $fAddr    = param('address');
      $fContact = param('contact');
      $fPhone   = param('phone');
      $fEmail   = param('email');
      $fUser    = param('user');
      $fPass    = param('pass');

   #  Determine errors
      push(@errors,
         &emptyCheck    ($fName, 'company name'),
         &abnCheck      ($fABN),
         &choiceCheck   ($fType, 'company type', COMPANY_TYPES),
         &emptyCheck    ($fAddr, 'address'),
         &emptyCheck    ($fContact, 'contact person'),
         &phoneCheck    ($fPhone),
         &emailCheck    ($fEmail),
         &usernameCheck ($fUser),
         &passwordCheck ($fPass)
         );
      push(@errors,
         "Fields cannot contain the '<b>" . htmlEncode(DELIM_PRIMARY) .
         "</b>' character.") if primaryDelimCheck($fName, $fABN, $fType,
         $fAddr, $fContact, $fPhone, $fEmail, $fUser, $fPass);

      unless (@errors)
      {
      #  Form data is valid
      #  Convert form data into 'raw' format in preparation for writing to file
         $fABN =~ s/[\,\ ]//g;
         $fPhone =~ s/\-//g;
      #  Do any company records exist yet?
         if (-e FILE_COMPANIES)
         {
         #  Loop through company records attempting to find given username and
         #  ABN; also determine largest used ID for later use if to create new
         #  record
            open(RECORDS, '+<' . FILE_COMPANIES);
            flock(RECORDS, LOCK_EX);
            while (my $record = <RECORDS>)
            {
               my ($rID, $rABN, $rUser, $x);
               ($rID, $x, $rABN, $x, $x, $x, $x, $x, $rUser, $x) =
                  split(DELIM_PRIMARY, $record);
               if ($rABN eq $fABN)
               {
               #  Specified ABN found in records
               #  Attempt to log the user in with their specified credentials
                  close(RECORDS);
                  my %company = getCompanyHash($rID);
                  if ($company{'user'} eq $fUser && $company{'pass'} eq $fPass)
                  {
                     companyLogin($fUser, $fPass);
                     divert('company.cgi', MSG_COMPANY_EXISTS);
                  }
                  else {
                     divert('company_login.cgi', MSG_COMPANY_EXISTS); }
               #  The script has terminated
               }
               if ($rUser eq $fUser)
               {
                  push(@errors, 'Your chosen username is already claimed.');
                  close(RECORDS);
                  last;
               }
               $rID = &intFromID($rID);
               $maxID = $rID if $rID > $maxID;
            }
         #  At this point either there has been an error and the file is closed
         #  or all is well and the file is ready to be appended to if necessary
         }
         else
         {
            $maxID = 0;
            open(RECORDS, '>' . FILE_COMPANIES);
            flock(RECORDS, LOCK_EX);
         }
      }

      unless (@errors)
      {
      #  The company has not previously registered and the username is unique
      #  The details can therefore be written
         $maxID = &idFromInt('c', $maxID + 1);
         print RECORDS join(DELIM_PRIMARY, $maxID, $fName, $fABN, $fType,
            $fAddr, $fContact, $fPhone, $fEmail, $fUser, $fPass), LF;
         close(RECORDS);
      #  Log the user into their new account
         companyLogin($fUser, $fPass);
         divert('company.cgi', MSG_NEW_COMPANY);
      }
   }

#  Prepare page data
#  Output any errors
   $pageData .= formErrorPop(@errors) if @errors;
#  Prepare form
   $pageData .=
      myForm(
         -elements =>
            [
               'Company name' => textfield('name', $fName),
               'ABN' => textfield('abn', $fABN, 14, 14),
               'Company type' => popup_menu('type', [COMPANY_TYPES], $fType),
               'Address' => textfield('address', $fAddr),
               'Contact person' => textfield('contact', $fContact),
               'Contact phone' => textfield('phone', $fPhone, 11, 11),
               'Contact Email' => textfield('email', $fEmail),
               'Username' => textfield('user', $fUser),
               'Password' => password_field(-name=>'pass', -force=>1)
            ],
         -button => 'Sign up',
         -validation => 'js_company_signup.js'
      );

#  Output page
   printPage(
      'Company signup',
      $pageData,
      myA('Log in', 'company_login.cgi'),
      myA('Job seeker signup', 'seeker_signup.cgi')
   );
