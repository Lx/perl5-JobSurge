/*#############################################################################
#                                                                             #
#  js_company_signup.js                                                       #
#                                                                             #
#  Written by Alex Peters, 23/9/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Provides form field focussing and validation for the company user signup   #
#  page.                                                                      #
#                                                                             #
#############################################################################*/

// Determine and focus the first field needing attention
   document.forms[0].name.focus();

/*###########################################################################*/

   function findErrors()
   {
      with (document.forms[0])
      {
         checkEmpty(name, 'company name');
         if (!checkEmpty(abn, 'ABN'))
            if (abn.value.search(/^\d{2}([\,\ ]?)(\d{3}\1){2}\d{3}$/) == -1)
               noteError(abn, 'You have not entered a valid ABN (must be in ' +
                  'the form ###########, ## ### ### ### or ##,###,###,###).');
         checkEmpty(address, 'address');
         checkEmpty(contact, 'contact person');
         checkPhone(phone);
         checkEmail(email);
         checkUsername(user);
         checkPassword(pass);
      }
   }
