# sqlalchemy-challenge
Homework for Module 10 - Advanced SQL

For this assignment, we were provided with a sqlite database comprised of data within 2 CSV files.

This module is all about using SQLAlchemy to perform analysis, so all code is using the SQLAlchemy ORM syntax.

While many of these functions could also be performed with a literal SQL query, I wanted to ensure that only the ORM syntax was used.

The jupyter notebook comprises Part 1 of the assignment, so the majority of the coding was implemented and tested there first.

With the "starter" jupyter notebook providing guidance and example results, I coded each cell to attain a desired result.

After verifying that the code works as expected in the notebook, I moved on to the python application to create a basic API using functions that were created in the notebook.

All endpoints have been tested multiple times to ensure functionality.

The <start> and <start>/<end> endpoints are expecting a date format of YYYY-MM-DD to be input into the URL.

If no date values are found after the input "start" date, results will return with null values.

Sources:
https://stackoverflow.com/questions/14659240/angle-bracket-without-triggering-html-code
https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
https://stackoverflow.com/questions/26763344/convert-pandas-column-to-datetime
https://stackoverflow.com/questions/53158423/between-clause-in-sqlalchemy-with-seleted-columns
https://stackoverflow.com/questions/53158423/between-clause-in-sqlalchemy-with-seleted-columns
https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending