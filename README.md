# Logs Analysis Project
#### _by Sebastian Pütz_
This project contains a python programm, that creates requests to a PSQL-database and prints them into the console.

## Program's design
The python-file logan.py (LOGs-ANalysis) mainly contains 3 functions, that are
 anatomically similar. Each function connects to the given news-database, creates a
 cursor and executes a SQL-query. These queries are requesting data from one or
 more tables (including manually created views) inside our db and connect, count, filter, select etc. this data.
 The result is getting fetched into a readable format and printed to the console.
 The db-connection gets closed after each function.
 The last part of "logan.py" is defined by the function-calls themselves, aswell
 as some more formatting and organizing of the output, including headlines, delimiters and an "End"-statement for letting us know, when the programm finished.


## Install and run

1. Install [VirtualBox](virtualbox.com)

2. Install [Vagrant](vagrantup.com)

3. Clone/Fork this repository, connect to vagrant and navigate into the shared
folger "vagrant"
```sh
$ git clone https://github.com/codebasti/Logs-Analysis/
$ cd logs-analysis-project
$ vagrant up
$ vagrant ssh
$ cd /vagrant
```

4. Download this [Zip-File](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
and extract it. Take the file "newsdata.sql" and move it into your vagrant directory.
Run these commands to get the data in your local machine up and running:   
(Make sure, you are connected to the virtual machine with vagrant ssh and
inside our vagrant folder!)
```
$vagrant@vagrant:/vagrant$ psql -d news -f newsdata.sql
```

5. Now you have access to the whole setup, but the logan.py programm needs some views to work properly.
Continue with step 6.

6. To create the views, simply go into the database terminal by executing the
following commands:
```
psql -d news
```
**View 1 - Each articles' total views**  
```
CREATE VIEW articleviews AS
SELECT articles.title,
COUNT(log.path) AS sum
FROM articles, log
WHERE log.path LIKE '%'||articles.slug
GROUP BY articles.title
ORDER BY sum DESC;
```
**View 2 - Each authors' total articleviews**  
```
CREATE VIEW articleauthors AS
SELECT articles.title, articles.author, authors.name
FROM articles join authors
ON articles.author = authors.id;
```
**View 3 - Days where more than 1% of requests lead to errors**  
```
CREATE VIEW dailyrequests AS
SELECT date(log.time) AS log_day,
COUNT (CASE WHEN status LIKE '%200 OK%' THEN 1 END) AS views,
COUNT (CASE WHEN status LIKE '%404%' THEN 1 END) AS errors,
COUNT (method) AS requests
FROM log
GROUP BY date(log.time)
ORDER BY log_day;
```
Quit the pSQL-Session with ```\q```
7. The installation and setup is done. Our python programm now has everything to work properly.   
Run:
```
python logan.py
```
The programm could need some time. The programm prints our "-----END-----" as soon as
it is finished.

## Known Bugs
None so far - Please send a message to basti.puetz@web.de if you find one.
