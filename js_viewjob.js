/*#############################################################################
#                                                                             #
#  js_viewjob.js                                                              #
#                                                                             #
#  Written by Alex Peters, 24/9/2005                                          #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Provides client-side confirmation for deletion of jobs.                    #
#                                                                             #
#############################################################################*/

   function deleteJob(id)
   {
      if (confirm('This job and all corresponding applications will be ' +
         'deleted. Confirm?'))
         window.location = 'company_deletejob.cgi?id=' + id + '&confirm=yes';
   }
