/*#############################################################################
#                                                                             #
#  js_seeker_signup.js                                                        #
#                                                                             #
#  Written by Alex Peters, 23/9/2005-25/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Provides form field focussing and validation for the job seeker signup     #
#  page.                                                                      #
#                                                                             #
#############################################################################*/

// Determine and focus the first field needing attention
   document.forms[0].first.focus();

/*###########################################################################*/

   function findErrors()
   {
      with (document.forms[0])
      {
         checkEmpty(first, 'first name');
         checkEmpty(last, 'last name');
         checkPhone(phone);
         checkEmpty(address, 'address');
         checkEmail(email);
         checkUsername(user);
         checkPassword(pass);
      }
   }
