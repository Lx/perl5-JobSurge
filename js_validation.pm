###############################################################################
#                                                                             #
#  js_validation.pm                                                           #
#  Written by Alex Peters, 1/9/2005-24/9/2005                                 #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Imported by js_common.pm. Houses all form validation functionality.        #
#                                                                             #
###############################################################################

#  Enforce declaration of variables
   use strict;

###############################################################################

   sub primaryDelimCheck #(value[, value[, ...]])
#  Returns TRUE if any of the passed values contain the primary delimeter (as
#  defined in js_config.pm).
   {
      while (@_) {
         return TRUE if index(shift(), DELIM_PRIMARY) >= 0; }
      return FALSE;
   }

###############################################################################

   sub secondaryDelimCheck #(value[, value[, ...]])
#  Returns TRUE if any of the passed values contain the secondary delimeter (as
#  defined in js_config.pm).
   {
      while (@_) {
         return TRUE if index(shift(), DELIM_SECONDARY) >= 0; }
      return FALSE;
   }

###############################################################################

   sub emptyCheck
   {
      my $data = $_[0];
      my $name = $_[1];

      my $msg = 'You have not entered a';
      $msg .= 'n' if $name =~ /^[AaEeIiOoUu]/;
      $msg .= ' <b>' . $name . '</b>.';

      my @error;
      push(@error, $msg) if $data eq '';
      return @error;
   }

###############################################################################

   sub choiceCheck #(formData, fieldName, validChoices)
#  Checks whether a form field contains a valid choice. Returns an error
#  message (as an array) if the field is empty or contains foreign data.
   {
   #  Read the parameters into variables
      my $data = $_[0];
      my $name = $_[1];
      shift; shift;
      my @choices = @_;

      my @error;
      if ($data eq '')
      {
         my $msg = 'You have not selected a';
         $msg .= 'n' if $name =~ /^[AaEeIiOoUu]/;
         $msg .= ' <b>' . $name . '</b>.';
         push(@error, $msg);
         return @error;
      }

   #  Data has a value
      my $valid;
      foreach my $option (@choices)
      {
         return my @nothing if $data eq $option;
      }

   #  Data does not match one of allowed values
      push(@error, 'You have not selected a <b>valid ' . $name . '</b> ' .
         '(please select one from the list).');
      return @error;
   }

###############################################################################

   sub intCheck
   {
      my $data = $_[0];
      my $name = $_[1];
      my @error;
      push(@error, 'You have not entered a <b>valid ' . $name . '</b> (must ' .
         'be an <b>integer</b>).') unless $data =~ /^\d+$/;
      return @error;
   }

###############################################################################

   sub phoneCheck
   {
      my $data = $_[0];
      my @error;
      if ($data eq '')
      {
         push(@error, 'You have not entered a <b>phone number</b>.');
         return @error;
      }
      unless ($data =~ /^((\d{2}\-)?\d{8}|\d{4}\-\d{6})$/)
      {
         push(@error, 'You have not entered a <b>valid phone number</b> ' .
            '(must be in the form <b>########</b>, <b>##-########</b> or ' .
            '<b>####-######</b>).');
      }
      return @error;
   }

###############################################################################

   sub emailCheck
   {
      my $email = $_[0];
      my @error;
      if ($email eq '')
      {
         push(@error, 'You have not entered an <b>Email address</b>.');
         return @error;
      }
      my $hasCorrectTLD      = ($email =~ /.(au|com|net)$/);
      my $hasAdjacentSymbols = ($email =~ /(\W)\1/        );
      my $hasMoreThanOneAt   = ($email =~ /\@.*\@/        );
      my $hasTwoCharsAfterAt = ($email =~ /\@.{2}/        );

      my $emailValid =
         $hasCorrectTLD && $hasTwoCharsAfterAt &&
         !($hasAdjacentSymbols || $hasMoreThanOneAt);

      unless ($emailValid)
      {
         push(@error, 'You have not entered a <b>valid Email address</b> ' .
            '(must end in <b>.au</b>, <b>.com</b> or <b>.net</b>, must not ' .
            'have two adjacent non-alphanumeric characters, must contain ' .
            'precisely one <b>@</b> symbol and must have two characters ' .
            'after it).');
      }
      return @error;
   }

###############################################################################

   sub usernameCheck
   {
      my $data = $_[0];
      my @error;
      if ($data eq '')
      {
         push(@error, 'You have not entered a <b>username</b>.');
         return @error;
      }
      unless ($data =~ /^\w{6,}$/)
      {
         push(@error, 'You have not entered a <b>valid username</b> (must ' .
            'consist of at least <b>6 alphanumeric</b> characters).');
      }
      return @error;
   }

###############################################################################

   sub passwordCheck
   {
      my $data = $_[0];
      my @error;
      if ($data eq '')
      {
         push(@error, 'You have not entered a <b>password</b>.');
         return @error;
      }
      if ($data =~ /(.)\1/ || !($data =~ /^\w{6,}$/))
      {
         push(@error, 'You have not entered a <b>valid password</b> (must ' .
            'consist of at least <b>6 alphanumeric</b> characters with no ' .
            'repeated consecutive characters).');
      }
      return @error;
   }

###############################################################################

   sub dateCheck
   {
      my $data = $_[0];
      my $name = $_[1];
      my @error;
      if ($data eq '')
      {
         my $msg = 'You have not entered a';
         $msg .= 'n' if $name =~ /^[AaEeIiOoUu]/;
         $msg .= ' <b>' . $name . '</b>.';
         push(@error, $msg);
         return @error;
      }
      unless ($data =~ /^(\d\d?\/){2}\d{4}$/)
      {
         push(@error, 'You have entered an <b>invalid ' . $name . '</b> ' .
            '(must be in the form <b>d/m/yyyy</b>).');
         return @error;
      }
      use Date::Calc('check_date');
      my ($checkDay, $checkMonth, $checkYear) = split(/\//, $_[0]);
      unless (check_date($checkYear, $checkMonth, $checkDay))
      {
         push(@error, 'You have entered a <b>non-existent ' . $name . '</b>.');
         return @error;
      }
      if (&dateHasExpired($data))
      {
         my $msg = 'You have entered a';
         $msg .= 'n' if $name =~ /^[AaEeIiOoUu]/;
         $msg .= ' <b>' . $name . '</b> in the past.';
         push(@error, $msg);
         return @error;
      }
      return my @noError;
   }

###############################################################################

#  Return true to indicate successful inclusion of the module
   TRUE;
