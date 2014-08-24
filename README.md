# Absolute Dates

UF VIVO has more than 66,000 date time values, but they represent only 7,700 distinct dates.  Treat
dates as first class entities.  If two dates with different URI have the same datetime value and
datetime precisions, they are the same date.  So merge and standardize.

## Process

1. Tabulate all instances of all datetime values
1. Merge all redundant values to single URIs
1. Provide datetime values for year values, year/month values and 
year/month/day values.  Ingests and other processes can then use these 
existing dates without proliferating copies of dates.

## Notes

1. VIVO screen-based processes create new dates.  Absolute Dates can be 
run at any time to collapse back to canonical dates.

