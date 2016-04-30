drop table marvelcharacter;
drop table marveledges;
drop table sumedge;



CREATE DATABASE marvel;
\c marvel;

CREATE TABLE marvelcharacter
(character varchar, role varchar, orders int, comicid int, comictitle varchar);
\i char_sql.sql


CREATE TABLE marveledges
(character1 varchar, character2 varchar, orders int);

\i edge_sql.sql





CREATE TABLE sumedge AS
SELECT character1, character2, SUM(orders) as edgeweight
FROM marveledges
GROUP BY character1, character2;

#COPY (SELECT character1, character2, SUM(orders) as edgeweight
#FROM marveledges
#GROUP BY character1, character2) To 'sumedges.csv' With CSV ;
