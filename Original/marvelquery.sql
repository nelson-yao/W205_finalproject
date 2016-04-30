

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
