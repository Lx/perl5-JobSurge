/*#############################################################################
#                                                                             #
#  js_contact.js                                                              #
#                                                                             #
#  Written by Alex Peters, 22/9/2005-25/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Provides form field focussing and validation for the company user contact  #
#  applicant page.                                                            #
#                                                                             #
#############################################################################*/

// Determine and focus the first field needing attention
   document.forms[0].date.focus();

/*###########################################################################*/

   function findErrors()
   {
      with (document.forms[0])
      {
         checkDate(date);
         checkEmpty(time, 'time');
         checkEmpty(location, 'location');
      }
   }
