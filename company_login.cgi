#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  company_login.cgi                                                          #
#                                                                             #
#  Written by Alex Peters, 2/9/2005-26/9/2005                                 #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Provides a form to allow a company user to log in.                         #
#                                                                             #
#  May be diverted to this page when:                                         #
#  -  a company user logs out                                                 #
#  -  a company page was accessed without a valid login session established   #
#  -  a company attempts to re-register but gives incorrect credentials       #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Declare variables requiring script scope
   my ($pageData, $user, $divertTo);

#  Log out any currently logged-in user
   my $wasLoggedIn = FALSE;
   if (defined(cookie('company_id')))
   {
      deleteCookie('company_id');
      $wasLoggedIn = TRUE;
   }

#  Note where we must go on a successful login if specified
   if (defined(cookie('msg_data')))
   {
      $divertTo = cookie('msg_data');
      deleteCookie('msg_data');
   }

   if (param('submit'))
   {
   #  Form was submitted
      $user = param('user');
      $divertTo = param('divert_to');
      if (companyLogin($user, param('pass')))
      {
      #  Credentials are correct and login cookie has been established
         setCookie('login', LOGIN_COMPANY);
         divert($divertTo || 'company.cgi');
      }
   #  Bad credentials were passed
      use URI::Escape;
      $pageData .=
         msgBox(
            POP_STOP,
            h4('An invalid username/password combination was entered.'),
            'Do you mean to <a href="seeker_login.cgi?user=' .
            uri_escape($user) . '">log in as a job seeker</a>?'
         );
   }
   elsif ($wasLoggedIn)
   {
      $pageData .=
         msgBox(
            POP_INFO,
            h4('You have successfully logged out.'),
            'Please close your browser to clear your session.'
         );
   }

#  Handle diversions to this page
   my $msg = getMsg();
   if ($msg == MSG_NOT_LOGGED_IN) {
      $pageData .= msgBox(POP_STOP, h4('You are currently not logged in.'),
         'Please enter your credentials to continue.'); }
   if ($msg == MSG_COMPANY_EXISTS) {
      $pageData .=
         msgBox(
            POP_INFO,
            h4('Your company appears to be registered with JobSurge already.'),
            'The ABN you specified is already in our records, however the',
            "login credentials you supplied don't match. Please try again."
         ); }

#  Prepare login form
   $pageData .=
      myForm(
         -elements =>
            [
               'Username' => textfield('user', $user),
               'Password' => password_field(-name => 'pass', -force => 1)
            ],
         -hiddens =>
            [
               'divert_to' => (defined($divertTo) && $divertTo)
            ],
         -button => 'Login',
         -validation => 'js_login.js'
      );

#  Output page
   &printPage(
      'Company login', $pageData,
      myA('Sign up',          'company_signup.cgi'),
      myA('Job seeker login', 'seeker_login.cgi')
   );
