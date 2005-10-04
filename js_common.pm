###############################################################################
#                                                                             #
#  js_common.pm                                                               #
#  Written by Alex Peters, 28/8/2005-24/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Houses functionality common to all scripts of the JobSurge package.        #
#                                                                             #
###############################################################################

#  Enforce declaration of variables within the module
   use strict;

#  Use CGI packages for easier HTML handling, error output and nicely formatted
#  HTML output
   use CGI(':standard');
   use CGI::Carp('fatalsToBrowser');
   use CGI::Pretty;

#  Import constants
   use js_constants;

#  Import configuration data
   use js_config;

#  Import other JobSurge modules
   use js_output;
   use js_validation;

###############################################################################

#  &idFromInt(prefix, int) -- returns a formulated ID with the given prefix
#  from the supplied integer
   sub idFromInt
   {
      my $prefix = $_[0];
      my $int    = $_[1];

      my $idDigits = 4;
      $int = "0$int" while length($int) < $idDigits;
      return "$prefix$int";
   }

###############################################################################

#  &intFromID(id) -- returns a number from a formulated ID
   sub intFromID
   {
      my $id = $_[0];
      $id = substr($id, 1) while !($id =~ /^\d*$/);
      return int($id);
   }

###############################################################################

   sub setCookie #(name, value)
#  Outputs a Set-Cookie header.
   {
      print 'Set-Cookie: ', cookie(-name => $_[0], -value => $_[1]), LF;
   }

###############################################################################

   sub deleteCookie #(name)
#  Outputs a Set-Cookie header with a past Expires attribute. Also outputs the
#  date to ensure that the delete operation is effective.
   {
      use HTTP::Date;
      print 'Set-Cookie: ',
         cookie(-name => $_[0], -value => '', -expires => '-1s'), LF;
      print 'Date: ', HTTP::Date::time2str(), LF;
   }

###############################################################################

   sub dateHasExpired #(date)
#  Returns TRUE if the given date (in D/M/YYYY format) occurred before today.
   {
      my ($checkDay, $checkMonth, $checkYear) = split('/', $_[0]);
      my ($day, $month, $year, $x);
      ($x, $x, $x, $day, $month, $year, $x) = localtime(time);
   #  Month is returned in 0-based format -- let's fix that
      $month += 1;
   #  Year initially gives number of years after 1900 -- let's fix that
      $year += 1900;
      
   #  The date HAS NOT expired if it is in a future year
      return FALSE if $checkYear > $year;
   #  The date HAS expired if it is in a past year
      return TRUE  if $checkYear < $year;
   #  The date HAS NOT expired if it is in a future month of this year
      return FALSE if $checkMonth > $month;
   #  The date HAS expired if it is in a past month of this year
      return TRUE  if $checkMonth < $month;
   #  The date HAS NOT expired if it is on a future day of this month
      return FALSE if $checkDay > $day;
   #  The date HAS expired if it is on a past day of this month
      return TRUE  if $checkDay < $day;
   #  The date represents today and therefore HAS NOT expired
      return FALSE;
   }

###############################################################################

   sub divert #(url[, msgID[, msgData]])
#  Redirects to the specified URL, optionally setting a message cookie of ID
#  msgID and message data from msgData.
   {
      my $url     = shift();
      my $msgID   = shift();
      my $msgData = shift();

      setCookie('msg_id', $msgID) if defined($msgID);
      setCookie('msg_data', $msgData) if defined($msgData);
      print redirect($url);
      exit;
   }

###############################################################################

   sub elementInArray #(element, arrayRef)
#  Returns TRUE if the given element occurs in the array referenced by
#  arrayRef.
   {
      my $element = shift();
      my @array = @{shift()};

      foreach my $arrayElement (@array)
      {
         return TRUE if $arrayElement eq $element;
      }
      return FALSE;
   }

###############################################################################

   sub getSkills
#  Returns an array of skills read from the XML file defined in js_config.pm.
   {
      use XML::Simple;
      my $xml = XMLin(FILE_SKILLS);
      return @{$xml->{'skill'}};
   }

###############################################################################

   sub getMsg
#  Returns a message ID from the user's cookie, and deletes the cookie.
   {
      my $msg;
      if (defined(cookie('msg_id')))
      {
         $msg = cookie('msg_id');
      #  deleteCookie('msg_id');
      }
      return $msg;
   }

###############################################################################

   sub getSIDFullNameHash #()
#  Returns a hash of job seeker ID/full name pairs.
   {
      my %output;
      open(RECORDS, '<' . FILE_SEEKERS);
      flock(RECORDS, LOCK_SH);
      while (my $record = <RECORDS>)
      {
         my ($sID, $sFName, $sLName, $x) = split(DELIM_PRIMARY, $record);
         $output{$sID} = "$sFName $sLName";
      }
      close(RECORDS);
      return %output;
   }

###############################################################################

   sub getAppsForJob #(jID)
#  Returns an array of applications matching the given job ID.
   {
      my $jID = shift();
      my @output;

      open(APPS, FILE_APPLICATIONS);
      flock(APPS, LOCK_SH);
      while (my $app = <APPS>)
      {
         my ($ajID, $x) = split(DELIM_PRIMARY, $app);
         push(@output, $app) if $ajID eq $jID;
      }
      close(APPS);
      return @output;
   }

###############################################################################

   sub getAppsForSeeker #(sID)
#  Returns an array of applications matching the given job seeker ID.
   {
      my $sID = shift();
      my @output;

      open(APPS, FILE_APPLICATIONS);
      flock(APPS, LOCK_SH);
      while (my $app = <APPS>)
      {
         my @fields = split(DELIM_PRIMARY, $app);
         push(@output, $fields[0]) if $fields[1] eq $sID;
      }
      close(APPS);
      return @output;
   }

###############################################################################

   sub getJobAppCountHash #()
#  Returns a hash of job ID/application count pairs.
   {
      my %output;
      open(APPS, '<' . FILE_APPLICATIONS);
      flock(APPS, LOCK_SH);
      while (my $app = <APPS>)
      {
         my ($jID, $x) = split(DELIM_PRIMARY, $app);
         $output{$jID}++;
      }
      close(APPS);
      return %output;
   }

###############################################################################

   sub getCompanyHash #(cID)
#  Returns a hash of information on the company with the specified ID.
   {
      my $cID = shift();
      my %output;

      open(FILE, FILE_COMPANIES);
      flock(FILE, LOCK_SH);
      while (my $record = <FILE>)
      {
         chomp($record);
         my @fields = split(DELIM_PRIMARY, $record);
         if ($fields[0] eq $cID)
         {
            $output{id}      = $fields[0];
            $output{name}    = $fields[1];
            $output{abn}     = $fields[2];
            $output{type}    = $fields[3];
            $output{address} = $fields[4];
            $output{contact} = $fields[5];
            $output{phone}   = $fields[6];
            $output{email}   = $fields[7];
            $output{user}    = $fields[8];
            $output{pass}    = $fields[9];
            last;
         }
      }
      close(FILE);
      return %output;
   }

###############################################################################

   sub getSeekerHash #(sID)
#  Returns a hash of information on the job seeker with the specified ID.
   {
      my $sID = shift();
      my %output;

      open(SEEKERS, '<' . FILE_SEEKERS);
      flock(SEEKERS, LOCK_SH);
      while (my $seeker = <SEEKERS>)
      {
         chomp($seeker);
         my @fields = split(DELIM_PRIMARY, $seeker);
         if ($fields[0] eq $sID)
         {
            $output{id}      = $fields[0];
            $output{fName}   = $fields[1];
            $output{lName}   = $fields[2];
            $output{phone}   = $fields[3];
            $output{address} = $fields[4];
            $output{email}   = $fields[5];
            $output{user}    = $fields[6];
            $output{pass}    = $fields[7];
            last;
         }
      }
      close(SEEKERS);
      return %output;
   }

###############################################################################

   sub getJobHash #(jID)
#  Returns a hash of information on the job with the specified ID.
   {
      my $jID = shift();
      my %output;

      open(JOBS, '<' . FILE_JOBS);
      flock(JOBS, LOCK_SH);
      while (my $job = <JOBS>)
      {
         my @fields = split(DELIM_PRIMARY, $job);
         if ($fields[0] eq $jID)
         {
            $output{id}         = $fields[0];
            $output{cID}        = $fields[1];
            $output{title}      = $fields[2];
            $output{type}       = $fields[3];
            $output{location}   = $fields[4];
            $output{expiry}     = $fields[5];
            $output{experience} = $fields[6];
            $output{skills}     = [split(DELIM_SECONDARY, $fields[7])];
            $output{salary}     = $fields[8];
            last;
         }
      }
      close(JOBS);
      return %output;
   }

###############################################################################

   sub getAppHash #(jID, sID)
#  Returns a hash of information on the application for the specified job by
#  the specified job seeker.
   {
      my $jID = shift();
      my $sID = shift();
      my %output;

      open(APPS, '<' . FILE_APPLICATIONS);
      flock(APPS, LOCK_SH);
      while (my $app = <APPS>)
      {
         my @fields = split(DELIM_PRIMARY, $app);
         if ($fields[0] eq $jID && $fields[1] eq $sID)
         {
            $output{jID}        = $fields[0];
            $output{sID}        = $fields[1];
            $output{position}   = $fields[2];
            $output{experience} = $fields[3];
            $output{skills}     = [split(DELIM_SECONDARY, $fields[4])];
            $output{salary}     = $fields[5];
            last;
         }
      }
      close(APPS);
      return %output;
   }

###############################################################################

   sub getSeekers #(jID)
#  Returns an array of IDs of job seekers who have applied for the specified
#  job.
   {
      my $jID = shift();
      my @output;
      open(APPS, FILE_APPLICATIONS);
      flock(APPS, LOCK_SH);
      while (my $app = <APPS>)
      {
         my ($aJID, $aSID, $x) = split(DELIM_PRIMARY, $app);
         push(@output, $aSID) if $aJID eq $jID;
      }
      close(APPS);
      return @output;
   }

###############################################################################

   sub getAppIDs #(sID)
#  Returns an array of job IDs for which the specified job seeker has applied.
   {
      my $sID = shift();
      my @output;

      open(APPS, '<' . FILE_APPLICATIONS);
      flock(APPS, LOCK_SH);
      while (my $app = <APPS>)
      {
         my @fields = split(DELIM_PRIMARY, $app);
         push(@output, $fields[0]) if $fields[1] eq $sID;
      }
      close(APPS);

      return @output;
   }

###############################################################################

   sub assertCompanyLogin
#  Ensures that a company user is logged in. Returns a hash of company infor-
#  mation if so; diverts to the company login page if not.
   {
   #  Attempt to read the company ID cookie
      my $id = cookie('company_id');
   #  If a job seeker is logged in then redirect to their main page
   #  (This is for when companies and job seekers will share one login cookie)
      if ($id =~ /s\d{4}/) {
         divert('seeker.cgi', MSG_NOT_A_COMPANY); }
   #  Anything else not matching a company ID must mean no login session
      my %details = getCompanyHash($id);
      unless (%details) {
         divert('company_login.cgi', MSG_NOT_LOGGED_IN, self_url()); }
   #  All is well; return the ID
      return %details;
   }

###############################################################################

   sub assertSeekerLogin
#  Ensures that a job seeker is logged in. Returns a hash of job seeker infor-
#  mation if so; diverts to the job seeker login page if not.
   {
   #  Attempt to read the company ID cookie
      my $id = cookie('seeker_id');
   #  If a company user is logged in then redirect to their main page
   #  (This is for when companies and job seekers will share one login cookie)
      if ($id =~ /c\d{4}/) {
         divert('company.cgi', MSG_NOT_A_SEEKER); }
   #  Anything else not matching a job seeker ID must mean no login session
      my %details = getSeekerHash($id);
      unless (%details) {
         divert('seeker_login.cgi', MSG_NOT_LOGGED_IN, self_url()); }
   #  All is well; return the ID
      return %details;
   }

###############################################################################

   sub expiryCheck
   {
      my $data = $_[0];
      my @error;
      if ($data eq '')
      {
         push(@error, 'You have not entered an <b>expiry date</b>.');
         return @error;
      }
      unless ($data =~ /^(\d{1,2}\/){2}\d{4}$/)
      {
         push(@error, 'You have not entered a <b>valid expiry date</b> (must' .
            ' be in the form <b>d/m/yyyy</b>).');
      }
      return @error;
   }

###############################################################################

   sub abnCheck
   {
      my $data = $_[0];
      my @error;
      if ($data eq '')
      {
         push(@error, 'You have not entered an <b>ABN</b>.');
         return @error;
      }
      unless ($data =~ /^\d{2}([\,\ ]?)(\d{3}\1){2}\d{3}$/)
      {
         push(@error, 'You have not entered a <b>valid ABN</b> (must be in ' .
            'the form <b>###########</b>, <b>## ### ### ###</b> or ' .
            '<b>##,###,###,###</b>).');
      }
      return @error;
   }

###############################################################################

   sub companyLogin #(user, pass)
#  Called by the company registration and login scripts. Establishes a login
#  cookie based on the given credentials. Returns TRUE if the session can be
#  established or FALSE if not.
   {
      my $user = $_[0];
      my $pass = $_[1];

   #  Delete any existing related cookies
      &deleteCookie('company_id');

      open(RECORDS, '<' . FILE_COMPANIES);
      flock(RECORDS, LOCK_SH);
      my @records = <RECORDS>;
      close(RECORDS);

      foreach my $record (@records)
      {
         chomp($record);
         my @fields = split(DELIM_PRIMARY, $record);
         my $rID = $fields[0];
         my $rUser = $fields[8];
         my $rPass = $fields[9];

         if ($rUser eq $user)
         {
         #  The username has been found
            return FALSE unless $rPass eq $pass;
         #  The password is correct -- establish login cookie
            &setCookie('company_id', $rID);
            return TRUE;
         }
      }
   #  The username was not found
      return FALSE;
   }

###############################################################################

   sub seekerLogin #(user, pass)
#  Called by the job seeker registration and login scripts. Establishes a login
#  cookie based on the given credentials. Returns TRUE if the session can be
#  established or FALSE if not.
   {
      my $user = $_[0];
      my $pass = $_[1];

   #  Delete any existing related cookies
      &deleteCookie('seeker_id');

      open(RECORDS, FILE_SEEKERS);
      flock(RECORDS, LOCK_SH);
      my @records = <RECORDS>;
      close(RECORDS);

      foreach my $record (@records)
      {
         chomp($record);
         my @fields = split(DELIM_PRIMARY, $record);
         my $rID = $fields[0];
         my $rUser = $fields[6];
         my $rPass = $fields[7];

         if ($rUser eq $user)
         {
         #  The username has been found
            return FALSE unless $rPass eq $pass;
         #  The password is correct -- establish login cookie
            setCookie('seeker_id', $rID);
            return TRUE;
         }
      }
   #  The username was not found
      return FALSE;
   }

###############################################################################

   sub getCompanyIDNameHash #()
#  Returns a hash of company ID/name pairs.
   {
      my %output;
      open(COMPANIES, FILE_COMPANIES);
      flock(COMPANIES, LOCK_SH);
      while (my $company = <COMPANIES>)
      {
         my ($cID, $cName, $x) = split(DELIM_PRIMARY, $company);
         $output{$cID} = $cName;
      }
      close(COMPANIES);
      return %output;
   }

###############################################################################

#  Return true to indicate successful inclusion of the module
   TRUE;
