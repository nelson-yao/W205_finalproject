drop table if exists marvelcharacter_test;
drop table if exists marveledges_test;
drop table if exists sumedge_test;
drop database if exists test

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
