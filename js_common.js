/*#############################################################################
#                                                                             #
#  js_common.js                                                               #
#                                                                             #
#  Written by Alex Peters, 25/9/2005-26/9/2005                                #
#  3105178 // apeters@cs.rmit.edu.au                                          #
#                                                                             #
#  Houses common JavaScript validation functions used on JobSurge pages.      #
#                                                                             #
#############################################################################*/

// Maximum number of errors to be displayed on any one page
   var maxErrors = 10;

// Variables to be accessed by the below functions
   var badField = null;
   var errors = new Array(maxErrors);
   var count = 0;

/*###########################################################################*/

   function noteError(field, msg)
// Effectively pushes the passed error message onto the end of the errors
// array. Flags the specified field as 'bad'.
   {
      errors[count++] = msg;
      if (badField == null)
         badField = field;
   }

/*###########################################################################*/

   function validateForm()
// Called when the form is submitted. Ensures that all fields contain valid
// data, preventing submission and displaying errors if not.
   {
   // Reset any existing errors
      badField = null;
      count = 0;

   // The findErrors() call is defined according to the page on which the form
   // is presented
      findErrors();

   // If no errors were found then the form can submit
      if (!count)
         return true;

   // This is how to display a single error
      var errorStr = errors[0];
   // This is how to display multiple errors
      if (count > 1)
      {
         errorStr = 'There are errors in your submission:\n';
         for (var i = 0; i < count; i++)
            errorStr += '\n*   ' + errors[i];
      }
   // Display errors
      alert(errorStr);
   // Draw attention to the 'bad field'
      if (badField != null)
      {
         badField.focus();
         badField.select();
      }
   // Prevent form submission
      return false;
   }

/*###########################################################################*/

   function checkEmpty(field, name)
// Notes an error if the specified field is empty. Prepend the name with white-
// space to circumvent vowel checking.
   {
   // Do nothing if the field consists of anything other than just white space
      if (field.value.search(/^\s*$/) != 0)
         return false;
      var msg = 'You have not entered a';
      if (name.search(/^[aeiou]/i) != -1)
         msg += 'n';
   // Trim whitespace from the beginning of the name
      name = name.replace(/^[\s]+/g, '');
      msg += ' ' + name + '.';
      noteError(field, msg);
      return true;
   }

/*###########################################################################*/

   function checkInt(field, name)
// Notes an error if the value of the specified field does not contain a valid
// (positive) integer.
   {
      if (checkEmpty(field, name))
         return;
      if (field.value.search(/^\d+$/) == -1)
         noteError(field, 'You have not entered a valid ' + name +
            ' (must be a positive integer).');
   }

/*###########################################################################*/

   function checkDate(field)
// Notes an error if the value of the specified field does not contain a valid
// date.
   {
      if (checkEmpty(field, 'date'))
         return;
      if (field.value.search(/^(\d\d?\/){2}\d{4}$/) == -1)
         noteError(field, 'You have not entered a valid date (must be in ' +
            'the form d/m/yyyy).');
   }

/*###########################################################################*/

   function checkPhone(field)
// Notes an error if the value of the specified field does not contain a valid
// phone number.
   {
      if (checkEmpty(field, 'phone number'))
         return;
      if (field.value.search(/^((\d{2}\-)?\d{8}|\d{4}\-\d{6})$/) == -1)
         noteError(field, 'You have not entered a valid contact phone ' +
            'number (must be in the form ########, ##-######## or ' +
            '####-######).');
   }

/*###########################################################################*/

   function checkEmail(field)
// Notes an error if the value of the specified field does not contain a valid
// Email address.
   {
      if (checkEmpty(field, 'Email address'))
         return;

      var correctTLD      = (field.value.search(/\.(au|com|net)$/) != -1);
      var adjacentSymbols = (field.value.search(/(\W)\1/         ) != -1);
      var moreThanOneAt   = (field.value.search(/\@.*\@/         ) != -1);
      var twoCharsAfterAt = (field.value.search(/\@.{2}/         ) != -1);

      var emailValid =
         correctTLD && twoCharsAfterAt &&
         !(adjacentSymbols || moreThanOneAt);

      if (!emailValid)
         noteError(field, 'You have not entered a valid Email address (must ' +
            'end in .au, .com or .net, must not have two adjacent ' +
            'non-alphanumeric characters and must contain precisely one @ ' +
            'symbol with at least two characters after it).');
   }

/*###########################################################################*/

   function checkUsername(field)
// Notes an error if the value of the specified field does not contain a valid
// username.
   {
      if (checkEmpty(field, ' username'))
         return;

      if (field.value.search(/^\w{6,}$/) == -1)
      noteError(field, 'You have not entered a valid username (must consist ' +
         'of at least 6 alphanumeric characters).');
   }

/*###########################################################################*/

   function checkPassword(field)
// Notes an error if the value of the specified field does not contain a valid
// password.
   {
      if (checkEmpty(field, 'password'))
         return;

      var hasAdjChars = (field.value.search(/(.)\1/) != -1);
      if (hasAdjChars || (field.value.search(/^\w{6,}$/) == -1))
      noteError(field, 'You have not entered a valid password (must consist ' +
         'of at least 6 alphanumeric characters with no repeated ' +
         'consecutive characters).');
   }
