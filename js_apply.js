/*#############################################################################
#                                                                             #
#  js_apply.js                                                                #
#                                                                             #
#  Written by Alex Peters, 22/9/2005-25/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Provides form field focussing and validation for the job seeker            #
#  application page.                                                          #
#                                                                             #
#############################################################################*/

// Determine and focus the first field needing attention
   with (document.forms[0])
      (id.value != '' ? position : id).focus();

/*###########################################################################*/

   function findErrors()
   {
      with (document.forms[0])
      {
         if (!checkEmpty(id, 'job ID'))
            if (id.value.search(/^j\d{4}$/) == -1)
               noteError(id, 'You have not entered a valid job ID.');
         checkEmpty(position, 'current position');
         checkInt(experience, 'length of experience');
         checkInt(salary, 'salary');
         checkEmpty(summary, 'profile summary');
      }
   }
