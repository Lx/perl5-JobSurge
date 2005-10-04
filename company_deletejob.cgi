#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  company_deletejob.cgi                                                      #
#                                                                             #
#  Written by Alex Peters, 29/8/2005-24/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Verifies that a company user is logged in. Deletes a job and its corres-   #
#  ponding applications, ensuring first that it belongs to the company        #
#  accessing it. Outputs a confirmation prompt if confirmation not given.     #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Ensure that a company user is logged in; get their ID if so
   my %company = assertCompanyLogin();

#  Get passed data
   my ($jID, $confirm) = (param('id'), param('confirm'));

#  Attempt to get information pertaining to the given job
   my %job = getJobHash($jID);

#  Redirect to the main company page if a job ID wasn't passed, doesn't exist
#  or doesn't belong to the company accessing it
   if (!$jID || !%job || $job{'cID'} ne $company{'id'}) {
      divert('company.cgi', MSG_BAD_JOB); }

   if ($confirm eq 'yes')
   {
   #  Action has been confirmed; go ahead with job deletion
   #  Read records to remain and then output them over the old ones
      my @keptJobs;
      open(RECORDS, '+<' . FILE_JOBS);
      flock(RECORDS, LOCK_EX);
      while (my $record = <RECORDS>)
      {
         my @fields = split(DELIM_PRIMARY, $record);
         push(@keptJobs, $record) if $fields[0] ne $jID;
      }
   #  Rewind to the beginning of the file and delete its contents; this is done
   #  to prevent the exclusive lock from being released
      seek(RECORDS, 0, 0);
      truncate(RECORDS, 0);
   #  File is now ready for writing
      print RECORDS $_ foreach (@keptJobs);
      close(RECORDS);
   #  Delete corresponding entries in the applications file
   #  Also delete the necessary summary text files
      my @keptApps;
      open(RECORDS, '+<' . FILE_APPLICATIONS);
      flock(RECORDS, LOCK_EX);
      while (my $record = <RECORDS>)
      {
         my ($aJID, $aSID, $x) = split(DELIM_PRIMARY, $record);
         if ($aJID eq $jID)
         {
            unlink(PATH_SUMMARIES . "/$jID$aSID.txt");
         }
         else
         {
            push(@keptApps, $record);
         }
      }
   #  Rewind to the beginning of the file and delete its contents; this is done
   #  to prevent the exclusive lock from being released
      seek(RECORDS, 0, 0);
      truncate(RECORDS, 0);
   #  File is now ready for writing
      print RECORDS $_ foreach (@keptApps);
      close(RECORDS);
   #  Indicate completion
      divert('company.cgi', MSG_JOB_REMOVED);
   }
   else
   {
   #  Action has not yet been confirmed
   #  Assemble a confirmation prompt
   my $pageData =
      p(
         "Job <b>$jID</b> and all corresponding applications will be deleted.",
         'Confirm?'
      ) .
      myA(
         'Yes -- delete the job',
         "company_deletejob.cgi?id=$jID&confirm=yes"
      );
   #  Output the prompt
      printPage(
         "Delete '$job{'title'}' offering",
         $pageData,
         myA('Job details', "company_viewjob.cgi?id=$jID"),
         myA('Main menu',   'company.cgi'),
         myA('Log out',     'company_login.cgi')
         );
   }
