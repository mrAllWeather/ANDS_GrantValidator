# ANDS_GrantValidator
Check ANDS grant IDs against the [ANDS grants API](http://developers.ands.org.au/services/getgrants/) to ensure they are valid.
Singular lookups should probably be performed via the [ANDS grants widget](http://developers.ands.org.au/widgets/grant_widget/).

Please note you will need an ANDS API key to use this script. You may sign up for one at [API Key Registration](http://researchdata.ands.org.au/registry/services/register/).

#### Language:
Python 3.4

### Input:
Tab delimited table as either text file or csv.

### Use:
python grant_validator.py example_input.txt

### Output:
Will output a tab-delimited txt file with a new column 'resolved', possible values TRUE, FALSE, Too Many Results.

### Process:
The code primarily checks numFound to determine result, then some additional checks are performed to increase accuracy of results.

NumFound = 0: 
* False (Occasionally IDs may not be on ANDS yet)

NumFound = 1:
* Search ID == Response ID:
  * True
* Search ID != Response ID:
  * "False: Partial String!" (partial match of ID)

NumFound > 1:
* "Too many Results"

NumFound is Other:
* "ERROR: {Other} invalid input"
