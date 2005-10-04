#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  seeker_login.cgi                                                           #
#                                                                             #
#  Written by Alex Peters, 26/8/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Provides a form to allow a company user to log in.                         #
#                                                                             #
#  May be diverted to this page when:                                         #
#  -  a job seeker logs out                                                   #
#  -  a job seeker page was accessed without a valid login session            #
#     established                                                             #
#  -  a job seeker attempts to re-register but gives incorrect credentials    #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Declare variables requiring script scope
   my ($pageData, $user, $divertTo);

#  Log out any currently logged-in user
   my $wasLoggedIn = FALSE;
   if (defined(cookie('seeker_id')))
   {
      deleteCookie('seeker_id');
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
      if (seekerLogin($user, param('pass')))
      {
      #  Credentials are correct and login cookie has been established
         setCookie('login', LOGIN_SEEKER);
         divert($divertTo || 'seeker.cgi');
      }
   #  Bad credentials were passed
      use URI::Escape;
      $pageData .=
         msgBox(
            POP_STOP,
            h4('An invalid username/password combination was entered.'),
            'Do you mean to <a href="company_login.cgi?user=' .
            uri_escape($user) . '">log in as a company user</a>?'
         );
   }

#  Handle diversions to this page
   my $msg = getMsg();
   if ($msg == MSG_NOT_LOGGED_IN) {
      $pageData .= msgBox(
         POP_STOP,
         h4('You are not currently logged in.'),
         'Please enter your credentials to continue.'); }
   elsif ($msg == MSG_SEEKER_EXISTS) {
      $pageData .=
         msgBox(
            POP_INFO,
            h4('You appear to be a JobSurge member already.'),
            'The first name and phone number you specified already appear ',
            'together in our records, however the login credentials you ',
            "supplied don't match. Please try again."
         ); }
   elsif ($wasLoggedIn && !param('submit'))
   {
      $pageData .= msgBox(
         POP_INFO,
         h4('You have successfully logged out.'),
         'Please close your browser to clear your session.');
   }

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
      'Job seeker login', $pageData,
      myA('Sign up',       'seeker_signup.cgi'),
      myA('Company login', 'company_login.cgi')
   );
