/*#############################################################################
#                                                                             #
#  js_login.js                                                                #
#                                                                             #
#  Written by Alex Peters, 21/9/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Provides form field focussing and validation for the login pages.          #
#                                                                             #
#############################################################################*/

// Determine and focus the first field needing attention
   with (document.forms[0])
      (user.value != '' ? pass : user).focus();

/*###########################################################################*/

   function findErrors()
   {
      with (document.forms[0])
      {
         checkEmpty(user, ' username');
         checkEmpty(pass, 'password');
      }
   }
