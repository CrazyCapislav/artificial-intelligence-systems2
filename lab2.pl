% Facts about characters (one argument)
main_character(kratos).
main_character(arthas).
% God of War characters
character(kratos).
character(zeus).
character(hades).
character(poseidon).
character(heimdall).
character(ares).
character(baldur).
character(hefest).
character(athena).

% Warcraft characters
character(arthas).
character(uther).
character(sylwana).
character(antonidas).
character(malganis).



% Facts about items (one argument)

% God of War items
item(leviathan).
item(bladesOfChaos).
item(draupnir).
item(bladeOfOlympus).

% Warcraft items
item(frostmourne).
item(helmOfDomination).

% Facts about owners (two argument)

% God of War
owns(kratos, leviathan).
owns(kratos, bladesOfChaos).
owns(kratos, draupnir).
owns(kratos, bladeOfOlympus).
% Warcraft
owns(arthas, frostmourne).
owns(arthas, helmOfDomination).

% Facts about murderers (two argument)

% God of War
murderer(kratos, zeus).
murderer(kratos, hades).
murderer(zeus, kratos).
murderer(kratos, poseidon).
murderer(kratos, heimdall).
murderer(kratos, heracles).
murderer(kratos, ares).
murderer(kratos, baldur).
murderer(kratos, athena).
murderer(kratos, hefest).

% Warcraft
murderer(arthas, uther).
murderer(arthas, sylwana).
murderer(arthas, antonidas).
murderer(arthas, malganis).

% Факты о предметах
keeperOf(baldur, leviathan).
keeperOf(athena, bladeOfOlympus).
keeperOf(hefest, draupnir).
keeperOf(uther, frostmourne).
keeperOf(helmOfDomination, malganis).

% Факты о защитниках
guardOf(ares,zeus).
guardOf(hades,zeus).
guardOf(poseidon,zeus).

% Факты об уязвимостях
hasWeakness(ares,leviathan).
hasWeakness(zeus,bladeOfOlympus).
hasWeakness(heimdall,draupnir).
hasWeakness(sylwana,helmOfDomination).
hasWeakness(malganis,frostmourne).

% Факты о целях
kratos_goal(defeat_zeus).
kratos_goal(defeat_heimdall).
kratos_goal(defeat_ares).
kratos_goal(obtain_leviathan).

arthas_goal(defeat_uther).
arthas_goal(defeat_sylwana).
arthas_goal(obtain_frostmourne).
arthas_goal(obtain_helm_of_domination).

% Rules
% Archenemies rule: Defines two characters as archenemies if they have killed each other
archenemies(Character1, Character2) :- murderer(Character1, Character2), murderer(Character2, Character1).

% god_slayer_weapon rule: Defines an item as a god-slayer weapon if Kratos owns it
god_slayer_weapon(Item) :- owns(kratos, Item).

% lich_king_attributes rule: Defines items associated with the Lich King if Arthas owns them
lich_king_attributes(Item) :- owns(arthas, Item).

% from_godOfWar rule: Defines a character as being from the God of War universe if they have a connection to Kratos
from_godOfWar(Character) :- (murderer(kratos, Character); murderer(Character, kratos)).

% from_warcraft rule: Defines a character as being from the Warcraft universe if they have a connection to Arthas
from_warcraft(Character) :- (murderer(arthas, Character); murderer(Character, arthas)).


% 1. Простые запросы к базе знаний для поиска фактов

% 1.1 Найти всех персонажей
% Запрос возвращает все факты, определяющие персонажей.
% ?- character(X).

% 1.2 Найти все предметы
% Запрос возвращает все факты, определяющие предметы.
% ?- item(X).

% 1.3 Найти всех владельцев и их предметы
% Запрос возвращает пары владельцев и принадлежащих им предметов.
% ?- owns(Owner, Item).


% 2. Запросы с использованием логических операторов (и, или, не)

% 2.1 Найти все легендарные предметы
% Использует логический оператор "или".
?- god_slayer_weapon(Item); lich_king_attributes(Item).

% 2.2 Найти персонажей из God of War, но не являющихся убийцами Кратоса
% Использует логический оператор "и" и "не".
?- from_godOfWar(Character), \+ murderer(Character, kratos).

% 2.3 Найти персонажей, которые являются арченемизами между собой
% Использует правило archenemies, которое требует, чтобы оба персонажа убили друг друга.
% ?- archenemies(X, Y).

% 3. Cложные запросы
% 3.1 Поиск мультиубийц из двух вселенных.
% ?- murderer(Character, Victim1), murderer(Character, Victim2), Victim1 \= Victim2, murderer(Character2, Victim3), murderer(Character2, Victim4), Victim3 \= Victim4, Character2 \= Character.