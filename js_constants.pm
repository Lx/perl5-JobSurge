###############################################################################
#                                                                             #
#  js_constants.pm                                                            #
#  Written by Alex Peters, 12/9/2005-24/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Imported by js_common.pm. Houses all non-configurable constants.           #
#                                                                             #
###############################################################################

#  Declare constants (some code will be more intuitive)
   use constant LF    => "\n";
   use constant TRUE  => 1;
   use constant FALSE => 0;

#  Inter-page message codes
   use constant {
      MSG_BAD_LOGIN         =>  1,
      MSG_SEEKER_LOGGED_IN  =>  2,
      MSG_COMPANY_LOGGED_IN =>  3,
      MSG_LOGGED_OUT        =>  4,
      MSG_NOT_LOGGED_IN     =>  5,
      MSG_JOB_ADDED         =>  6,
      MSG_JOB_REMOVED       =>  7,
      MSG_BAD_JOB           =>  8,
      MSG_NOT_A_SEEKER      =>  9,
      MSG_NOT_A_COMPANY     => 10,
      MSG_JOB_APPLIED       => 11,
      MSG_BAD_APP           => 12,
      MSG_SEEKER_NOTIFIED   => 13,
      MSG_NEW_COMPANY       => 14,
      MSG_COMPANY_EXISTS    => 15,
      MSG_SEEKER_EXISTS     => 16,
      MSG_NEW_SEEKER        => 17 };

   use constant LOGIN_COMPANY => 1;
   use constant LOGIN_SEEKER  => 2;

#  Style constants used by msgBox()
   use constant {
      POP_STOP  => 1,
      POP_INFO  => 2,
      POP_SMILE => 3,
      POP_FROWN => 4 };

#  File locking constants
   use constant {
      LOCK_SH => 1,
      LOCK_EX => 2,
      LOCK_NB => 4,
      LOCK_UN => 8 };

#  Return true to indicate successful inclusion of the module
   TRUE;
