###############################################################################
#                                                                             #
#  js_config.pm                                                               #
#  Written by Alex Peters, 31/8/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Houses customisable configuration settings.                                #
#                                                                             #
###############################################################################

#  Location of CSS file relative to JobSurge scripts
   use constant FILE_CSS => './js_styles.css';

#  Job type, location and skill sets
   use constant JOB_TYPES => qw(Permanent Part-time Casual);
   use constant JOB_LOCATIONS => qw(Melbourne Sydney Canberra Brisbane Perth);

#  Location of skills XML file
   use constant FILE_SKILLS => './js_skills.xml';

#  Company type set
   use constant COMPANY_TYPES => qw(Private Government Charity);

#  Delimiters
   use constant DELIM_PRIMARY   => ':';
   use constant DELIM_SECONDARY => '~';

#  Filenames
   use constant {
      FILE_JOBS         => './jobs.txt',
      FILE_SEEKERS      => './seekers.txt',
      FILE_COMPANIES    => './companies.txt',
      FILE_APPLICATIONS => './applications.txt' };

#  Path to store summaries (please ensure that this path exists already)
   use constant PATH_SUMMARIES => '.';

###############################################################################

#  sendmail location
   use constant PATH_SENDMAIL => '/usr/lib/sendmail';

#  Email address to use in 'From' field of outgoing mail
   use constant MAIL_FROM => 'no-reply@jobsurge.com.au';

###############################################################################

#  Return true to indicate successful inclusion of the module
   TRUE;
