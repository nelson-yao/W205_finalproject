from sys import argv
import psycopg2
import re

nargs = len(argv)
conn = psycopg2.connect(database="marvel", user="postgres",
                        password="pass", host="localhost", port="5432")
cur = conn.cursor()

if nargs==3 and str(argv[1])=="totalsales":
    querychar=argv[2]
    cur.execute("select character, SUM(orders) from marvelcharacter where character=%s group by character;" %querychar)
    result=cur.fetchall()
    for item in result:
        print item
        #print "%s has %s comic books sold" %(result[0], result[1])

if nargs==2 and str(argv[1])=="most_profitable_character":

    cur.execute("  SELECT character, SUM(orders) as totalorders from marvelcharacter group by character order by totalorders DESC limit 10;")
    result=cur.fetchall()
    for item in result:
        print "%s has %s comic books sold" %(result[0], result[1])

if nargs==2 and str(argv[1])=="most_profitable_villain":

    cur.execute(" SELECT character, SUM(orders) as totalorders from marvelcharacter where role='Villainous' group by character order by totalorders DESC limit 10;")
    result=cur.fetchall()
    for item in result:
        print "%s has %s comic books sold" %(result[0], result[1])

if nargs==3 and str(argv[1])=="most_sold_with":
    querychar=argv[2]
    cur.execute("select character1, character2, edgeweight from sumedge where character1='%s' ORDER BY edgeweight DESC LIMIT 10;" %querychar)
    result=cur.fetchall()
    for item in result:
        print "%s and %s sold %s comic books together" %(result[0], result[1], result[2])
