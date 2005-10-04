JOBSURGE
Online job search agency for software developers

Written by Alex Peters, 25/8/2005-26/9/2005
3105178 // apeters@cs.rmit.edu.au


ONLINE DEMONSTRATION
--------------------

A working copy of the JobSurge package is accessible at:
http://yallara.cs.rmit.edu.au/~apeters/jobsurge/index.html

*  Prepared demo company accounts (username/password):
   -  centrelink/alexpeters
   -  zikaiq/123456

*  Prepared demo job seeker accounts:
   -  apeters/alexpeters
   -  sipsas/123456

*  You are of course free to create your own accounts and post your own whacky
   job listings and applications (in fact I look forward to reading them!).

For the best possible viewing experience please consider Mozilla Firefox:
http://www.mozilla.org/products/firefox/


INSTALLATION
------------

*  All files can be placed in the one directory and used with no problems. It
   is recommended however that the FILE_* and PATH_SUMMARIES constants within
   js_config.pm are set so that the data files are stored in another directory
   to keep things tidy (e.g. the FILE_* constants set to './data/...' and
   PATH_SUMMARIES set to './summaries').

*  Necessary permissions for various files:

   -  .htaccess: 604
   -  *.gif, *.html, *.js, *.png: 604
   -  *.cgi: 701


TECHNICAL FEATURES
------------------

*  Administrator-customisable features are separated out into a dedicated file
   (js_config.pm) for easy access and manipulation.

*  Data is stored in files using the format outlined in the assignment specifi-
   cation, with file locking implemented for error-free concurrent access.

*  Data validation is performed on the client side as well as the server side,
   which eases server load and reduces traffic.

*  Subroutines are used heavily. They are spread out across a few different
   modules depending on their nature.

*  Scripts perform a redirect after most operations, which helps to protect
   against double-ups of e.g. new job postings through page refreshes.

*  All page output from each script is deferred to the very end through the use
   of a $pageData variable and a printPage() function. This allows for liberal
   use of redirects and elegant handling of errors.


TO DO
-----

*  Functionality issues:

   -  Client-side validation does not cover internal delimiters, expired dates
      or drop-down entries.

   -  Time is not validated on the company interview form (this is probably
      best left as it is, because it allows the user to enter extra information
      such as the expected duration of the interview).

*  Cosmetic issues:

   -  Although all scripts work as expected under Internet Explorer, time
      constraints have prevented me from having the layout render to my
      satisfaction.

   -  Dollar figures could be shown as e.g. $1,234 instead of $1234.

   -  The job deletion confirmation page is functional but visually primitive
      (however it is only displayed if the user has JavaScript disabled).
