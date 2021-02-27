%Current hypothesis:
%pet(X) :- animal(X).
%wild(X) :- mammal(X).

ground(cat).
ground(fish).

% Additions to the BG from the hypothesis
rule(r1).
head(r1, pet(X)) :- ground(X).
pbl(r1, 1, animal(X)) :- ground(X).

rule(r2).
head(r2, wild(X)) :- ground(X).
pbl(r2, 1, animal(X)) :- ground(X).

rule(r3).
head(r3, animal(cat)).
rule(r4).
head(r4, animal(fish)).
rule(r5).
head(r5, mammal(cat)).

in_AS(R, animal(X)) :- rule(R), head(R, animal(X)).
in_AS(R, mammal(X)) :- rule(R), head(R, mammal(X)).

%REVISABLE:
in_AS(R, pet(X)) :- head(R, pet(X)), pbl(R, 1, animal(X)).
in_AS(R, wild(X)) :- head(R, wild(X)), pbl(R, 1, animal(X)).

pet(X) :- in_AS(R, pet(X)), animal(X).
wild(X) :- in_AS(R, wild(X)), animal(X).
animal(X) :- in_AS(R, animal(X)).
mammal(X) :- in_AS(R, mammal(X)).

order(r3, r4).
order(r4, r5). 
order(r5, r1).
order(r1, r2).
rule_not_first(R) :- order(R_OTHER, R), rule(R), rule(R_OTHER).

% rule-specific condition: when is a rule considered as seen, aside requiring all previous rules to be seen first???????
% a rule is seen whether or not the head turns out to be true, so now we need to link the revisable rules to their semantics.
seen_rule(R) :- not rule_not_first(R), rule(R), in_AS(R, X).
seen_rule(R) :- not rule_not_first(R), rule(R), not in_AS(R, _).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), in_AS(R, X).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), not in_AS(R, _).



%Examples:
%#pos(eg1, {pet(cat)}, {}).
%#neg(eg2, {pet(fish)}, {}).

%Mode declarations:
%#modeb(pbl(const(rn), animal(var(ground)))).
%#modeb(pbl(const(rn), mammal(var(ground)))).
%#constant(rn, r1).
