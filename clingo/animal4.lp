%Current hypothesis:
%pet(X) :- animal(X), not mammal(X), wild(X).
%wild(X) :- animal(X).

ground(cat).
ground(fish).

bl(R, N, X) :- pbl(R, N, X).
bl(R, N, X) :- nbl(R, N, X).

% Additions to the BG from the hypothesis
rule(r1).
head(r1, pet(X)) :- ground(X).
pbl(r1, 1, animal(X)) :- ground(X).
nbl(r1, 2, mammal(X)) :- ground(X).
pbl(r1, 3, wild(X)) :- ground(X).

rule(r2).
head(r2, wild(X)) :- ground(X).
pbl(r2, 1, animal(X)) :- ground(X).

rule(r3).
head(r3, animal(cat)).
rule(r4).
head(r4, animal(fish)).
rule(r5).
head(r5, mammal(cat)).

in_AS(X) :- head(R, X), body_true(R, X).

body_exists(R) :- bl(R, N, X).
body_true(R, X) :- rule(R), head(R, X), not body_exists(R).

% same_subject is generated based on the given program, linking consecutive body literals, and the head literal with the last body literal.
same_subject(X, Y) :- X = animal(X_P), Y = mammal(Y_P), X_P = Y_P, ground(X_P), ground(Y_P).
same_subject(X, Y) :- X = mammal(X_P), Y = wild(Y_P), X_P = Y_P, ground(X_P), ground(Y_P).
same_subject(X, Y) :- X = pet(X_P), Y = wild(Y_P), X_P = Y_P, ground(X_P), ground(Y_P).
same_subject(X, Y) :- X = wild(X_P), Y = animal(Y_P), X_P = Y_P, ground(X_P), ground(Y_P).

bl_inbetween(R, X, Y) :- bl(R, N1, X), bl(R, N2, Y), bl(R, N3, Z), N1 < N3, N3 < N2.
bl_notlast(R, X) :- bl(R, N1, X), bl(R, N2, Y), N1 < N2.
bl_notfirst(R, X) :- bl(R, N, X), N > 1.

% if X (eg animal(cat)) is a pbl, then the first case would match, and we expect to see in_AS(animal(cat)) for the body of rule R to be true up to the Nth body literal.
satisfied(R, N, X, pos) :- pbl(R, N, X), in_AS(X).
% if X (eg mammal(fish)) is a nbl, then the second case would match, and we should not see in_AS(animal(cat)) for the body of rule R to be true up to Nth body literal.
satisfied(R, N, X, neg) :- nbl(R, N, X), not in_AS(X).

body_true_upto(R, N, X, T) :- satisfied(R, N, X, T), not bl_notfirst(R, X).
body_true_upto(R, N1, X, T1) :- satisfied(R, N1, X, T1), N2 < N1, body_true_upto(R, N2, Y, T2), not bl_inbetween(R, Y, X), same_subject(Y, X).

body_true(R, X) :- head(R, X), body_true_upto(R, N, Y, T), same_subject(X, Y), not bl_notlast(R, Y).
%pos_body_true_upto(R, X, Y, var(cat,X,Y)):-

order(r3, r4).
order(r4, r5). 
order(r5, r1).
order(r1, r2).
rule_not_first(R) :- order(R_OTHER, R), rule(R), rule(R_OTHER).
seen_rule(R) :- not rule_not_first(R), rule(R), in_AS(X), head(R, X).
seen_rule(R) :- not rule_not_first(R), rule(R), not in_AS(X), head(R, X).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), in_AS(X), head(R, X).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), not in_AS(X), head(R, X).


#show in_AS/1.
#show body_true/2.
#show body_true_upto/4.
#show bl_notlast/2.
#show seen_rule/1.
#show bl/3.