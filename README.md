# Logs-Analysis
### Brief Description:
  >This an internal reporting tool for a newspaper site which contains articles
 and their authors and log view that contains http requests statistics .
  * Project Output:
    * Titles of list of articles.
    * Titles of top 3 most viewed articles.
    * Most viewed authors.
    * Error rate more than 1% of daily http request. 	
### Installation:
  * User can run this project from gitbash terminal with vagrant installed.
  * First user should navigate to the directory where the vagrant exists by
  typing 'cd vagrant' then login to vagrant by 'vagrant ssh' then 
  'cd /vagrant' and running python code 'Python Project.py'.
  
### Usage:
   * Internal reporting tool uses information from the database to discover
  what kind of articles that the site readers like.

### Methodology:
  * The program use queries to fetch results from the database then using
  python coding styling and some changes are made to the results to print
  it on the screen.
  * The program contain four methods each contain a query that return the
  result and then processing it.
  * db_connect method connects the database and returns the connection if
  established and terminate the program if connection failed.
  * main method calls the program methods and by call main() project runs.
  * In the answer of third question view to the database is added.
  * From bash terminal type "psql -d news" to type commands in the database.
  * View query: 
  "create view log_view as
               select count(status),time::timestamp::date from log
               where status like '%NOT%' GROUP BY log.time::timestamp::date
               UNION
               select count(status) , time::timestamp::date from log
               group by log.time::timestamp::date;"
  
