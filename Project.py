# !/usr/bin/env python
import psycopg2
DBNAME = "news"  # database name to connect

query1 = """SELECT title FROM articles"""

query2 = """SELECT articles.title,count(*) AS views
            FROM articles
            JOIN log
               ON log.path
            LIKE '/article/' || articles.slug
            GROUP by articles.title
            ORDER by views DESC
            LIMIT 3"""

query3 = """SELECT authors.name,count(log.path) AS views
            FROM articles , log , authors
            WHERE (log.path like '/article/' || articles.slug)
            AND (authors.id=articles.author)
            GROUP BY articles.slug,authors.name"""

query4 = """SELECT day,rate
            FROM(
                 SELECT B.count/cast(A.count as float)*100 AS rate,
                 A.time as day
                 FROM log_view A , log_view B
                 WHERE A.count != B.count
                 AND A.time = B.time AND A.count > B.count) AS temp
            WHERE rate > 1.0"""


def db_connect(database_name):
    try:
        db = psycopg2.connect(dbname=database_name)
        return db
    except psycopg2.Error as e:
        print ("Unable to connect to database")
        sys.exit(1)


def show_articles_title():  # show list of available articles
    db = db_connect(DBNAME)
    c = db.cursor()
    c.execute(query1)  # database query
    articles = c.fetchall()
    db.close()
    articles_list = zip(*articles)[0]  # convert tuple to list
    print "List Of Articles Titles Available:-"
    print "------------------------------------"
    for i in range(len(articles_list)):  # print elements of list line by line
        print '-' + articles_list[i]
    print "____________________________________"


def most_viewed_articles():  # answer of question 1
    db = db_connect(DBNAME)
    c = db.cursor()
    c.execute(query2)
    result1 = c.fetchall()
    db.close()
    print "Top 3 Viewed Articles:-"
    print "------------------------"
    print "Title" + "\t\t\t\t\tViews"
    print "------" + "\t\t\t\t\t-----"
    a, b = zip(*result1)  # seperate tuple into 2 elements to print them
    for i in range(len(result1)):
        print a[i]+'\t'+str(b[i])
    print "_________________________________________________"


def most_viewed_authors():  # answer of question 2
    db = db_connect(DBNAME)
    c = db.cursor()
    # query returns each articles and its author and views
    c.execute(query3)
    temp1 = c.fetchall()
    db.close()
    # counting authors row into one row to count the views of each author
    # based on their articles
    s = set([i[0] for i in temp1])
    temp2 = []
    for i in s:
        sum = 0
        for j in temp1:
            if i == j[0]:
                sum += j[1]
        temp2.append(sum)
    result2 = zip(s, temp2)
    print "Most Popular Authors:-"
    print "-----------------------"
    # sort in descending order
    result2.sort(key=lambda x: x[1], reverse=True)
    print "Author" + "\t\t\tViews"
    print "----" + "\t\t\t-----"
    a, b = zip(*result2)
    for i in range(len(result2)):
        if i == 0 or i == 3:
            print a[i]+'\t\t'+str(b[i])
        else:
            print a[i]+'\t'+str(b[i])
    print "____________________________________"


def error_request():  # answer of question 3
    db = db_connect(DBNAME)
    c = db.cursor()
    c.execute(query4)
    result3 = c.fetchall()
    db.close()
    print "More Than 1% HTTP Request Error:-"
    print "----------------------------------"
    a, b = zip(*result3)
    print "Date\t\tRate"
    print "-----\t\t-----"
    for i in range(len(result3)):
        print str(a[i]) + '\t' + str('%.2f' % b[i]) + '%'


print "*****Internal Reporting Tool*****\n"


def main():
    show_articles_title()
    most_viewed_articles()
    most_viewed_authors()
    error_request()


main()  # run all scripts included in main()
