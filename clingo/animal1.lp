%Target hypothesis:
%pet(X) :- animal(X), mammal(X).
%Current hypothesis:
%pet(X) :- animal(X).

ground(cat).
ground(fish).

rule(r1).
head(r1, pet(X)) :- ground(X).
pbl(R, animal(X)) :- animal(X), rule(R).
pbl(R, mammal(X)) :- mammal(X), rule(R).

%REVISABLE:
pet(X) :- head(R, pet(X)), pbl(R, animal(X)), pbl(R, mammal(X)), rule(R).

%BG:
rule_bg(r2).
head(r2, animal(cat)).
rule_bg(r3).
head(r3, animal(fish)).
rule_bg(r4).
head(r4, mammal(cat)).

animal(X) :- head(R, animal(X)), rule_bg(R), ground(X).
mammal(X) :- head(R, mammal(X)), rule_bg(R), ground(X).


%Examples:
%pos(pet(cat))
%neg(pet(fish))

%Mode declarations:
%#modeb(animal(X))
%#modeb(mammal(X))
%#modeb(pbl(const(R), animal(var(X))).
%#modeb(pbl(const(R), mammal(var(X))).

%#constant(R,  r1)
