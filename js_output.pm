###############################################################################
#                                                                             #
#  js_output.pm                                                               #
#  Written by Alex Peters, 28/8/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Imported by js_common.pm. Houses all page output functionality.            #
#                                                                             #
###############################################################################

#  Enforce declaration of variables
   use strict;

###############################################################################

   sub myForm #(paramHash)
#  Outputs HTML code for a customised form depending on the parameters passed
#  in the hash. Valid keys are -method (to override POST), -validation to
#  specify a JavaScript file that validates the form, -title to give the form
#  a bold heading, -hiddens to specify hidden variables to include, -elements
#  to specify the names and elements within the form and -button to specify the
#  button label.
   {
      my %params = getParamHash(\@_);
      my @hiddens = @{$params{-hiddens}} if $params{-hiddens};
      my $hiddenTags;
      while (@hiddens)
      {
         my $name = shift(@hiddens);
         my $value = shift(@hiddens);
         $hiddenTags .= hidden($name, $value);
      }
      return
         start_form(
            -method => ($params{-method} || 'post'),
            -onSubmit => ($params{-validation} && 'return validateForm()')
         ) .
         lrBox(
            -header => ($params{-title} && h2($params{-title})),
            -values => $params{-elements},
            -footer =>
               $hiddenTags .
               (
                  $params{-validation} &&
                  '<script type="text/javascript" src="js_common.js">' .
                  '</script><script type="text/javascript" src="' .
                  $params{-validation} . '"></script>'
               ) .
               submit(-name => 'submit', -value => $params{-button})
         ) .
         end_form();
   }

###############################################################################

   sub getParamHash #(arrayRef)
#  Returns a hash from an array. Useful for when hashes are used in an array
#  context (such as in calls to lrBox()).
   {
      my @array = @{shift()};
      my %hash;
      while (@array)
      {
         my $key = shift(@array);
         my $value = shift(@array);
         $hash{$key} = $value;
      }
      return %hash;
   }

###############################################################################

   sub lrBox #([-header => header,] -values => valueHash[, -footer => footer])
#  Outputs a two-column box. Valid keys are -values (mandatory), -header and
#  -footer where -values refers to a hash with keys as the left column and
#  values as the right column.
   {
   #  Read parameter hash
      my %params = getParamHash(\@_);

   #  Get values
      my @values = @{$params{-values}};

   #  Prepare headers and footers
      my $headerRow =
         Tr(td(
            {
               -colspan => 2,
               -style   => 'border-bottom: 1px solid #aaa; padding-bottom: 8px'
            },
            $params{-header}
         ))
         if $params{-header};
      my $footerRow =
         Tr(td(
            {
               -align => 'right',
               -style => 'border-top: 1px solid #aaa; padding-top: 8px'
            },
            $params{-footer}
         ))
         if $params{-footer};

   #  Prepare rows of values
      my $valueRows;
      while (@values)
      {
         $valueRows .=
            Tr(
               td(
                  {-align => 'right', -style => 'padding: 4px 16px 4px 0'},
                  shift(@values)
               ),
               td(
                  {-align => 'left', -style => 'padding: 4px 0'},
                  shift(@values)
               )
            );
      }

      return
         table(
            {-class => 'formBox'},
            $headerRow,
            Tr(td(
               {-align => 'center'},
               table(
                  {
                     -cellspacing => 0,
                     -style =>
                        ($headerRow && 'padding-top: 10px; ') .
                        ($footerRow && 'padding-bottom: 12px; ')
                  },
                  $valueRows
               )
            )),
            $footerRow
         );
   }

###############################################################################

   sub jobBox #(paramHash)
#  Outputs a job box containing the details specified in the hash. Valid keys
#  are -job (mandatory), -company and -footer where -job gives a reference to a
#  job hash, -company gives a reference to a company hash (used for job seeker
#  pages where this information is needed), and -footer offers a facility for
#  adding appropriate links (e.g. 'delete' or 'apply').
   {
   #  Read parameter hash
      my %params = getParamHash(\@_);

   #  Get access to passed hashes
      my %job = %{$params{-job}};
      my %company = %{$params{-company}} if $params{-company};
      my $footerRow;
      $footerRow =
         Tr(td(
            {
               -align   => 'right',
               -colspan => 2,
               -style   => 'padding-top: 8px'
            },
            $params{-footer}
         ))
         if $params{-footer};
      my $blurbCellStyle =
         'border-top: 1px solid #777; ' .
         (
            $footerRow ?
            'border-bottom: 1px solid #777; padding: 12px 0' :
            'padding-top: 12px'
         );

      return
         table(
            {-class => 'formBox', -width => '100%'},
            Tr(
               td(
                  h2($job{title})
               ),
               td(
                  {-align => 'right'},
                  "Job <b>$job{id}</b><br />Expires <b>$job{expiry}</b>"
               )
            ),
            Tr(td(
               {
                  -align   => 'center',
                  -colspan => 2,
                  -style   => $blurbCellStyle
               },
               table(Tr(td(
                  b($job{type}), 'position in', b($job{location}), 'area',
                  (defined(%company) && 'offered by ' . b($company{name})),
                  br(), b($job{experience}),
                  'years of software developer experience required', br(),
                  (friendlyList($job{skills}, TRUE) || b('No')),
                  'skills required', br(),
                  'Maximum salary of', b("\$$job{salary}"), 'offered'
               )))
            )),
            $footerRow
         );
   }

###############################################################################

   sub printPage #(title, page[, link[, link[, ...]]])
#  Outputs a complete HTML page with the specified information.
   {
   #  Read incoming parameters
      my $title = shift();
      my $page  = shift();
      my @links = @_;

   #  Convert links into a single HTML string
      my $linkCode = '';
      for (my $i = 0; $i < scalar(@links); $i++)
      {
         $linkCode .= '<nobr>';
         $linkCode .= '<font color="#aaaacc">&nbsp;|&nbsp;</font>' . LF if $i;
         $linkCode .= "$links[$i]</nobr>";
      }

   #  Process messages that could want to be displayed on no particular page
      my $login = cookie('login');
      if ($login == LOGIN_COMPANY) {
         $page = msgBox(POP_SMILE, h4('Welcome.'),
            'You have successfully logged in.') . $page; }
      if ($login == LOGIN_SEEKER)
      {
         my %seeker = getSeekerHash(cookie('seeker_id'));
         $page = msgBox(POP_SMILE, h4("Welcome $seeker{'fName'}."),
            'You have successfully logged in.') . $page;
      }
      deleteCookie('login') if defined(cookie('login'));

   #  Delete inter-page message cookies (they will have been processed by now)
      deleteCookie('msg_id');
      deleteCookie('msg_data');

   #  Print/complete the HTML header
      print
         header(),
         start_html(
            -title => "JobSurge: $title",
            -style => FILE_CSS
         );

   #  Output the HTML
       print
         table(
            {
               -cellpadding => 0,
               -cellspacing => 16,
               -width       => '100%',
               -class       => 'topBar'
            },
            Tr(
               td(h6('&nbsp;JobSurge&trade;'), h2($title)),
               td({-align => 'right'}, $linkCode)
            )
         ),
         table(
            {
               -cellpadding => 16,
               -cellspacing => 0,
               -width       => '100%',
            },
            Tr(td($page))
         ),
         end_html();
   }

###############################################################################

   sub formErrorPop #(errorArray)
#  Returns HTML code for a form submission error popup.
   {
      my $output = h4('There are errors in your submission.');
      $output .= $_[1] ? ul(li([@_])) : $_[0];
      return msgBox(POP_STOP, $output);
   }

###############################################################################

   sub myA #(text, url[, onClick])
#  Returns HTML code for a link.
   {
      my $text    = shift();
      my $url     = shift();
      my $onClick = shift();

      my %params;
      $params{-href} = $url;
      $params{-onClick} = $onClick if defined($onClick);
      return a(\%params, $text);
   }

###############################################################################

   sub msgBox #(styleID, msg)
#  Returns HTML code for a popup in the specified style with the given message.
   {
   #  Determine message box parameters
      my %styles =
         (
            (POP_INFO)  => ['infoPop', '<i>i</i>'            ],
            (POP_STOP)  => ['stopPop', '!'                   ],
            (POP_SMILE) => ['infoPop', '<i><sup>:)</sup></i>'],
            (POP_FROWN) => ['stopPop', '<i><sup>:(</sup></i>']
         );

   #  Get style ID
      my $id = shift();

   #  Assemble and return the message box
      return
         table(
            {
               -align       => 'center',
               -cellpadding => 0,
               -cellspacing => 8,
               -class       => $styles{$id}[0]
            },
            Tr(
               td(
                  '<font size="6" face="serif"><b>&nbsp;' . $styles{$id}[1] .
                  '&nbsp;</b></font>'
               ),
               td(@_)
            )
         );
   }

###############################################################################

#  &htmlEncode(data) -- converts raw data into HTML-outputtable data (can be
#  used to display form data without fear of malicious consequences)
   sub htmlEncode
   {
      use HTML::Entities;
      my $output;
      while (@_)
      {
         $output .= HTML::Entities::encode($_[0]);
         shift;
      }
      return $output;
   }

###############################################################################

   sub offeringTable #(title, jobArrayRef, appCountHashRef)
#  Constructs a table of jobs found in the array referenced by jobArrayRef.
#  A reference to an application count hash is expected because multiple calls
#  to this function may be made.
   {
   #  Get passed parameters
      my $title    =   shift();
      my @jobs     = @{shift()};
      my %appCount = %{shift()};

   #  Compute a table row for each job
      my $jobRows;
      foreach my $job (@jobs)
      {
         my ($jID, $jTitle, $jExp, $x);
         ($jID, $x, $jTitle, $x, $x, $jExp, $x) = split(DELIM_PRIMARY, $job);
         $jobRows .=
            Tr(
               td([
                  myA($jID, "company_viewjob.cgi?id=$jID"),
                  $jTitle,
                  $jExp,
                  int($appCount{$jID})
               ])
            );
      }

   #  Complete the table and return its HTML code
      return
         table(
            {
               -class=>'formBox',
               -width=>'100%'
            },
            Tr(
               td(
                  {
                     -colspan => 4,
                     -style   => 'padding-bottom: 8px'
                  },
                  h2($title),
                  'Click a job ID for more information'
               )
            ),
            Tr(
               th([
                  'ID',
                  'Title',
                  'Expiry',
                  'Applications'
               ])
            ),
            $jobRows
         );
   }

###############################################################################

   sub friendlyList #(arrayRef[, boolBold])
#  Returns a 'friendly' string of an array elements, where a friendly string of
#  the array ('Java', 'Perl', 'XML') is 'Java, Perl and XML'. Elements will be
#  wrapped in <b></b> tags if boolBold evaluates to true.
   {
      my @array = @{shift()};
      my $bold  =   shift();

      my $output;
      for (my $i = 0; $i <= $#array; $i++)
      {
         if ($i)
         {
            if ($i == $#array) {
               $output .= ' and '; }
            else {
               $output .= ', '; }
         }
         $output .= ($bold && '<b>');
         $output .= htmlEncode($array[$i]);
         $output .= ($bold && '</b>');
      }
      return $output;
   }

###############################################################################

#  Return true to indicate successful inclusion of the module
   TRUE;
