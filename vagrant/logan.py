#!/usr/bin/env python

import psycopg2
import datetime

DBNAME = "news"

# The following 3 functions are anatomically similar, so that only the first,
# "poparticles"-function, is commended and described in detail.


# (1) This function will print the three most popular articles.
def poparticles():
    # Connecting to the database
    db = psycopg2.connect(database=DBNAME)
    # Creating the cursor
    c = db.cursor()
    # Let the cursor execute our SQL query
    c.execute(
        "SELECT * from articleviews "
        "LIMIT 3;")
    # Fetch all the results, again with our cursor
    data = c.fetchall()
    # Format and print the fetched "data"
    for row in data:
        print row[0], "-", row[1], "views"
    # Close the connection to our database
    db.close


# (2) This function will print the most popular authors from our database.
def popauthors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "SELECT articleauthors.name, SUM(articleviews.sum) "
        "FROM articleauthors JOIN articleviews "
        "ON articleauthors.title = articleviews.title "
        "GROUP BY articleauthors.name "
        "ORDER BY sum DESC;")
    data = c.fetchall()
    for row in data:
        print row[0], "-", row[1], "views"
    db.close


# (3) This function will print the days, where more than 1% of all requests
# lead to errors.
def errorday():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "SELECT log_day, ROUND((100.0*errors/requests), 2) AS percentage "
        "FROM dailyrequests "
        "WHERE 100*errors/requests > 1;")
    data = c.fetchall()
    for row in data:
        print row[0].strftime('%B %m, %Y'), "-", row[1], "% errors"
    db.close

# The following code defines the output and adds headlines and delimiters to
# make the output more readable.
print "-----START-----"
print "\n"
print "The three most popular articles of all time:"
print "\n"
poparticles()
print "----------"
print "\n"
print "The most popular article authors of all time:"
print "\n"
popauthors()
print "----------"
print "\n"
print "Days where more than 1% of requests lead to errors:"
print "\n"
errorday()
print "----------"
print "-----END-----"
