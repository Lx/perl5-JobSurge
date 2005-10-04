/*#############################################################################
#                                                                             #
#  js_newjob.js                                                               #
#                                                                             #
#  Written by Alex Peters, 21/9/2005-25/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Provides form field focussing and validation for the company user new job  #
#  page.                                                                      #
#                                                                             #
#############################################################################*/

// Determine and focus the first field needing attention
   document.forms[0].title.focus();

/*###########################################################################*/

   function findErrors()
   {
      with (document.forms[0])
      {
         checkEmpty(title, 'job title');
         checkDate(expiry);
         checkInt(experience, 'length of experience')
         checkInt(salary, 'salary')
      }
   }
