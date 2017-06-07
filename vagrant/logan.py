#!/usr/bin/env python

import psycopg2
import datetime

# (0) This function connects to the database "news" and creates a cursor
# It also returns both db and cursor if the method gets called
def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("NOPE!")

# The following 3 functions are anatomically similar, so that only the first,
# "poparticles"-function, is commended and described in detail.
# (1) This function will print the three most popular articles.
def poparticles():
    # Call the connect method from above
    db, cursor = connect()
    # Enter the SQL statement
    query = "SELECT * from articleviews LIMIT 3;"
    # Execute the query
    cursor.execute(query)
    # Fetch all the results
    data = cursor.fetchall()
    # Format and print the fetched "data"
    for row in data:
        print row[0], "-", row[1], "views"
    # Close the connection to our database
    db.close

# (2) This function will print the most popular authors from our database.
def popauthors():
    db, cursor = connect()
    query = ("SELECT articleauthors.name, SUM(articleviews.sum) "
        "FROM articleauthors JOIN articleviews "
        "ON articleauthors.title = articleviews.title "
        "GROUP BY articleauthors.name "
        "ORDER BY sum DESC;")
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        print row[0], "-", row[1], "views"
    db.close

# (3) This function will print the days, where more than 1% of all requests
# lead to errors.
def errorday():
    db, cursor = connect()
    query = ("SELECT log_day, ROUND((100.0*errors/requests), 2) AS percentage "
        "FROM dailyrequests "
        "WHERE 100*errors/requests > 1;")
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        print row[0].strftime('%B %m, %Y'), "-", row[1], "% errors"
    db.close

# The following code defines the output and adds headlines and delimiters to
# make the output more readable.
if __name__ == "__main__":
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
