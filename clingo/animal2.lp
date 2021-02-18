%Target hypothesis:
%pet(X) :- animal(X), mammal(X).
%Current hypothesis:
%pet(X) :- animal(X).

ground(cat).
ground(fish).

% Additions to the BG from the hypothesis
rule(r1).
head(r1, pet(X)) :- ground(X).

%REVISABLE:
pet(X) :- head(R, pet(X)), pbl(R, animal(X)).

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
%#pos(eg1, {pet(cat)}, {}).
%#neg(eg2, {pet(fish)}, {}).

%Mode declarations:
%#modeb(pbl(const(rn), animal(var(ground)))).
%#modeb(pbl(const(rn), mammal(var(ground)))).
%#constant(rn, r1).
