#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  seeker_signup.cgi                                                          #
#                                                                             #
#  Written by Alex Peters, 31/8/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Accepts signup information from and registers a new job seeker. Ensures    #
#  that all fields are populated. Prevents double signups by checking for     #
#  duplicate first name/phone number pairs. Forces unique usernames for each  #
#  job seeker.                                                                #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Define variables needing script-wide scope
   my (@errors, $maxID, $pageData);
   my ($fFName, $fLName, $fPhone, $fAddr, $fEmail, $fUser, $fPass);

   if (param('submit'))
   {
   #  Form has been submitted
   #  Get the form data into variables
      $fFName = param('first');
      $fLName = param('last');
      $fPhone = param('phone');
      $fAddr  = param('address');
      $fEmail = param('email');
      $fUser  = param('user');
      $fPass  = param('pass');

   #  Determine errors
      push(@errors,
         &emptyCheck    ($fFName, 'first name'),
         &emptyCheck    ($fLName, 'last name' ),
         &phoneCheck    ($fPhone              ),
         &emptyCheck    ($fAddr,  'address'   ),
         &emailCheck    ($fEmail              ),
         &usernameCheck ($fUser               ),
         &passwordCheck ($fPass               )
         );
      push(@errors,
         "Fields cannot contain the '<b>" . htmlEncode(DELIM_PRIMARY) .
         "</b>' character.") if primaryDelimCheck($fFName, $fLName, $fPhone,
         $fAddr, $fEmail, $fUser, $fPass);

      unless (@errors)
      {
      #  Form data is valid
      #  Convert form data into 'raw' format in preparation for writing to file
         $fPhone =~ s/\-//g;
      #  Do any company records exist yet?
         if (-e FILE_SEEKERS)
         {
         #  Loop through job seeker records attempting to find given username,
         #  first name and phone number
         #  Also determine largest used ID for later use if to create new record
            open(RECORDS, '+<' . FILE_SEEKERS);
            flock(RECORDS, LOCK_EX);
            while (my $record = <RECORDS>)
            {
               chomp($record);
               my ($rID, $rFName, $rPhone, $rUser, $x);
               ($rID, $rFName, $x, $rPhone, $x, $x, $rUser, $x) =
                  split(DELIM_PRIMARY, $record);
               if ($rFName eq $fFName && $rPhone eq $fPhone)
               {
               #  Specified first name and phone number found together in records
               #  Attempt to log the user in with their specified credentials
                  close(RECORDS);
                  my %seeker = getSeekerHash($rID);
                  if ($seeker{'user'} eq $fUser && $seeker{'pass'} eq $fPass)
                  {
                     seekerLogin($fUser, $fPass);
                     divert('seeker.cgi', MSG_SEEKER_EXISTS);
                  }
                  else {
                     divert('seeker_login.cgi', MSG_SEEKER_EXISTS); }
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
            open(RECORDS, '>' . FILE_SEEKERS);
            flock(RECORDS, LOCK_EX);
         }
      }

      unless (@errors)
      {
      #  The job seeker has not previously registered and the username is
      #  unique
      #  The details can therefore be written
         $maxID = &idFromInt('s', $maxID + 1);
         print RECORDS join(DELIM_PRIMARY, $maxID, $fFName, $fLName, $fPhone,
            $fAddr, $fEmail, $fUser, $fPass), LF;
         close(RECORDS);
      #  Log the user into their new account
         seekerLogin($fUser, $fPass);
         divert('seeker.cgi', MSG_NEW_SEEKER);
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
               'First name'    => textfield('first',   $fFName        ),
               'Last name'     => textfield('last',    $fLName        ),
               'Phone number'  => textfield('phone',   $fPhone, 11, 11),
               'Address'       => textfield('address', $fAddr         ),
               'Email address' => textfield('email',   $fEmail        ),
               'Username'      => textfield('user',    $fUser         ),
               'Password'      => password_field(-name=>'pass', -force=>1)
            ],
         -button => 'Sign up',
         -validation => 'js_seeker_signup.js'
      );

#  Output page
   printPage(
      'Job seeker signup',
      $pageData,
      myA('Log in', 'seeker_login.cgi'),
      myA('Company signup', 'company_signup.cgi')
   );
