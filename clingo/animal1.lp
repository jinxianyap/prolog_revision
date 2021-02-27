%Current hypothesis:
%pet(X) :- animal(X), mammal(X).

ground(cat).
ground(fish).

rule(r1).
head(r1, pet(X)) :- ground(X).

%REVISABLE:
pet(X) :- head(r1, pet(X)), pbl(r1, animal(X)), pbl(r1, mammal(X)).

%BG:
rule_bg(r2).
head(r2, animal(cat)).
rule_bg(r3).
head(r3, animal(fish)).
rule_bg(r4).
head(r4, mammal(cat)).

pbl(R, animal(X)) :- head(R_bg, animal(X)), rule_bg(R_bg), rule(R), ground(X).
pbl(R, mammal(X)) :- head(R_bg, mammal(X)), rule_bg(R_bg), rule(R), ground(X).

%Examples:
%pos(pet(cat))
%neg(pet(fish))

%Mode declarations:
%#modeb(animal(X))
%#modeb(mammal(X))
%#modeb(pbl(const(R), animal(var(X))).
%#modeb(pbl(const(R), mammal(var(X))).

%#constant(R,  r1)
