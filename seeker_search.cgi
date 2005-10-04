#! /usr/local/bin/perl -w

###############################################################################
#                                                                             #
#  seeker_search.cgi                                                          #
#                                                                             #
#  Written by Alex Peters, 3/9/2005-26/9/2005                                 #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Verifies that a job seeker is logged in. Allows a user to search for jobs  #
#  based on location and/or skills. Filters out jobs that have expired and    #
#  jobs for which the user has already applied.                               #
#                                                                             #
###############################################################################

   use strict;
   use js_common;

#  Ensure that a job seeker is logged in; get their ID if so
   my %seeker = assertSeekerLogin();

#  Form variables
   my ($fLoc, $fType, @fSkills);
   my (@errors, $pageData);

   if (param())
   {
   #  Form has been submitted
   #  Read the form into variables
      $fLoc = param('location');
      @fSkills = param('skills');

   #  Validate location
      push(@errors, choiceCheck($fLoc, 'location', JOB_LOCATIONS, 'Any'));

      unless (@errors)
      {
      #  Filter out any specified skills that aren't presented on the form
      #  (i.e. hacked ones)
         my @fProperSkills;
         foreach my $fSkill (@fSkills)
         {
            push(@fProperSkills, $fSkill)
               if elementInArray($fSkill, [getSkills()]);
         }
         @fSkills = @fProperSkills;
         undef @fProperSkills;
   
      #  Load all jobs matching the specified location (load all jobs if
      #  matching any location)
         open(JOBS, FILE_JOBS);
         flock(JOBS, LOCK_SH);
         my @jobs;
         while (my $job = <JOBS>)
         {
            chomp($job);
            if ($fLoc eq 'Any')
            {
               push(@jobs, $job);
            }
            else
            {
               my @fields = split(DELIM_PRIMARY, $job);
               push(@jobs, $job) if $fields[4] eq $fLoc;
            }
         }
         close(JOBS);
   
      #  Get job IDs for which the user has already applied
         my @appJobs = getAppIDs($seeker{'id'});
   
      #  Determine results from remaining jobs
         my @results;      
         for (my $i = 0; $i < @jobs; $i++)
         {
            my @fields = split(DELIM_PRIMARY, $jobs[$i]);
         #  Discard expired jobs
            if (dateHasExpired($fields[5]))
            {
               undef $jobs[$i];
               next;
            }
         #  Discard jobs not requiring any of the skills specified for the
         #  search(skip this if no skills were specified, which means dis-
         #  regard skills)
            if (@fSkills)
            {
               my @jSkills = split(DELIM_SECONDARY, $fields[7]);
               my $discardJob = TRUE;
               foreach my $fSkill (@fSkills) {
                  $discardJob = FALSE if elementInArray($fSkill, \@jSkills); }
               if ($discardJob)
               {
                  undef $jobs[$i];
                  next;
               }
            }
         #  Discard jobs for which the user has already applied
            if (elementInArray($fields[0], \@appJobs))
            {
               undef $jobs[$i];
               next;
            }
         #  Reaching this point means that the job is a search result
            push(@results, $jobs[$i]);
            undef $jobs[$i];
         }
         undef @jobs;
   
      #  Continue
         $pageData .= msgBox(POP_INFO,
            'You searched for jobs in',
            ($fLoc eq 'Any' ? b('any') . ' location' : b($fLoc)),
            'matching',
            (
               @fSkills ?
               'the skills ' . friendlyList(\@fSkills, TRUE) . '.' :
               b('any') . ' skills.'
            )
            );
      #  Populate a hash of company ID/name pairs
         my %cNames = getCompanyIDNameHash();
   
      #  Output results table
         if (@results)
         {
         #  Compute table rows
            my $jobRows;
            foreach my $result (@results)
            {
               my ($jID, $jCID, $jTitle, $jType, $jLoc, $jExp, $jYrs, $jSkills,
                  $jSalary, $x) = split(DELIM_PRIMARY, $result);
               $jobRows .=
                  Tr(
                     td(
                        {-style => 'padding: 0 8px'},
                        [
                           myA($jID, "seeker_apply.cgi?id=$jID"),
                           $cNames{$jCID},
                           $jTitle,
                           $jType,
                           $jLoc,
                           $jExp,
                           $jYrs,
                           join(', ', split(DELIM_SECONDARY, $jSkills))
                        ]
                     ),
                     td(
                        {-style => 'padding: 0 8px', -align => 'right'},
                        "\$$jSalary"
                     )
                  );
            }
            $pageData .=
               table(
                  {-class => 'formBox'},
                  Tr(td(
                     {-colspan => 8, -style => 'padding-bottom: 8px'},
                     h2(
                        @results > 1 ?
                        scalar(@results) . ' results' :
                        'One result'
                     ),
                     'Select a job ID to apply'
                  )),
                  Tr(th([
                     'ID',
                     'Company',
                     'Title',
                     'Type',
                     'Location',
                     'Expiry',
                     'Experience',
                     'Skills',
                     'Salary'
                  ])),
                  $jobRows
               );
         }
         else
         {
            $pageData .=
               msgBox(
                  POP_FROWN,
                  h4('No job offerings match this criteria.'),
                  (@fSkills ? 'Have you tried ' .
                  '<a href="seeker_search.cgi?location=' . $fLoc .
                  '">matching <b>any</b> skills</a>?' :
                  'Jobs are constantly added so please check back soon!')
               );
         }
      }
      $pageData .= formErrorPop(@errors) if @errors;
   }

#  Prepare search form
   my $skillHTML = checkbox_group('skills', [getSkills()], [@fSkills], FALSE);
   $pageData .=
      myForm(
         -method => 'get',
         -elements =>
            [
               'Location' =>
                  popup_menu('location', ['Any', JOB_LOCATIONS], $fLoc),
               'Skills' . br() . '(select none' . br() . 'to match any)' =>
                  $skillHTML
            ],
         -button => 'Search'
      );

#  Output page
   printPage(
      'Search for jobs', $pageData,
      myA('Main menu', 'seeker.cgi'),
      myA('Apply', 'seeker_apply.cgi'),
      myA('Log out', 'seeker_login.cgi')
      );
