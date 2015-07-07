# ANDS_GrantValidator
Check ANDS grant IDs against the [ANDS grants API](http://developers.ands.org.au/services/getgrants/) to ensure they are valid.
Singular lookups should probably be performed via the [ANDS grants widget](http://developers.ands.org.au/widgets/grant_widget/)

#### Language:
Python 3.4

### Input:
Tab delimited table as either text file or csv.

### Use:
python grant_validator.py example_input.txt

### Output:
Will output a tab-delimited txt file with a new column 'resolved', possible values TRUE, FALSE, Too Many Results.

### Problems:
This code is really rough; currently testing is performed only by checking the number of responses. 0: False, 1: True, (!0 or !1): Too may results.

False positives may occur when a partial ID is provided and there is only 1 grant which shares the same starting number.

'Too many results' will also trigger on any negative result but as I cannot find a reference to such within the documentation so, should be fine?

