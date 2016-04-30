drop table marvelcharacter;
drop table marveledges;
drop table sumedge;

CREATE DATABASE test;
CREATE TABLE marveledges_test
(character1 varchar, character2 varchar, orders int);

COPY marveledges FROM '/data/marvel/marveledges_test.csv' DELIMITERS ',' quote '"' CSV;

\c test;

CREATE TABLE character_test
(character varchar, role varchar, orders int, comicid int, comictitle varchar);

COPY marvelcharacter FROM '/data/marvel/marvelchar_test.csv' DELIMITERS ',' quote '"' CSV;

CREATE TABLE sumedge_test AS
SELECT character1, character2, SUM(orders) as edgeweight
FROM marveledges
GROUP BY character1, character2;

COPY (SELECT character1, character2, SUM(orders) as edgeweight
FROM marveledges
GROUP BY character1, character2) To '/data/marvel/sumedges.csv' With CSV ;

#### most profitable Hero
SELECT character, SUM(orders) as totalorders
from marvelcharacter
group by character
order by totalorders DESC
limit 20;


#### most profitable villain
SELECT character, SUM(orders) as totalorders
from marvelcharacter
where role='Villainous'
group by character
order by totalorders DESC
limit 20;

###most sold with Avengers
select character1, character2, edgeweight
from sumedge
where character1='Avengers' AND character2 NOT IN ('Captain America', 'Avengers', 'Quicksilver', 'Scarlet Witch', 'Hulk', 'Black Widow', 'Hawkeye', 'Iron Man', 'Thor', 'Ant-man', 'Vision', 'Spider-Man')
ORDER BY edgeweight DESC
LIMIT 20;


#### most sold with Spider-Man
select character1, character2, edgeweight
from sumedge
where character1='Spider-Man'
ORDER BY edgeweight DESC
LIMIT 20;

#### most profitable character not in movies
SELECT character, SUM(orders) as totalorders
from marvelcharacter
where character NOT IN ('Captain America', 'Avengers', 'Wolverine', 'Cyclops', 'Quicksilver', 'Scarlet Witch', 'Hulk', 'Black Widow', 'Hawkeye', 'Iron Man', 'Thor', 'Ant-man', 'Cyclops', 'Jean Grey', 'Professor X', 'Charles Xavier', 'Colossus', 'Storm', 'Wasp', 'Magneto', 'Fantastic Four', 'Beast', 'Spider-Man', 'Deadpool', 'Venom', 'Rogue', 'Thing', 'Nightcrawler', 'Cage', 'Iceman', 'Sabretooth', 'Invisible Woman', 'Loki', 'Gambit', 'Thanos', 'Apocalypse')
group by character
order by totalorders DESC
limit 20;


#### most sold with existing Avengers

##### most sold with avenger members
select character1, character2, edgeweight
from sumedge
where character1 IN ('Captain America', 'Quicksilver', 'Scarlet Witch', 'Hulk', 'Black Widow', 'Hawkeye', 'Iron Man', 'Thor', 'Ant-man', 'Vision') AND character2 NOT IN ('Captain America', 'Avengers', 'Wolverine', 'Cyclops', 'Quicksilver', 'Scarlet Witch', 'Hulk', 'Black Widow', 'Hawkeye', 'Iron Man', 'Thor', 'Ant-man', 'Cyclops', 'Jean Grey', 'Professor X', 'Charles Xavier', 'Colossus', 'Storm', 'Wasp', 'Magneto', 'Beast', 'Vision');

ORDER BY edgeweight DESC
LIMIT 20;



#### combined sales of Cable
select character, SUM(orders)
from marvelcharacter
where character='Cable'
group by character;


### combined sales of Namor
select character, SUM(orders)
from marvelcharacter
where character='Namor'
group by character;
