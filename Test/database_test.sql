drop table marvelcharacter;
drop table marveledges;
drop table sumedge;

CREATE DATABASE test;
\c marvel;

CREATE TABLE marvelcharacter_test
(character varchar, role varchar, orders int, comicid int, comictitle varchar);
\i char_sql_test.sql

CREATE TABLE marveledges_test
(character1 varchar, character2 varchar, orders int);

\i char_sql_edges.sql



CREATE TABLE sumedge_test AS
SELECT character1, character2, SUM(orders) as edgeweight
FROM marveledges_test
GROUP BY character1, character2;

#COPY (SELECT character1, character2, SUM(orders) as edgeweight
#FROM marveledges
#GROUP BY character1, character2) To 'sumedges.csv' With CSV ;
