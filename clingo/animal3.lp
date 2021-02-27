%Current hypothesis:
%pet(X) :- animal(X).
%wild(X) :- mammal(X).

ground(cat).
ground(fish).

% Additions to the BG from the hypothesis
rule(r1).
head(r1, pet(X)) :- ground(X).
pbl(r1, 1, animal(X)) :- ground(X).
pbl(r1, 2, mammal(X)) :- ground(X).
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

% how to get predicate and constant from X????????????
in_AS(X) :- head(R, X), pos_body_true(R), not neg_body_false(R).
in_AS(X) :- head(R, X), pos_body_true(R, X), not neg_body_false(R).
pos_body_exists(R) :- pbl(R, N, X).
pos_body_true(R) :- rule(R), not pos_body_exists(R).

same_subject(X, Y) :- X = animal(X_P), Y = mammal(Y_P), X_P = Y_P, ground(X_P), ground(Y_P).
same_subject(X, Y) :- X = mammal(X_P), Y = wild(Y_P), X_P = Y_P, ground(X_P), ground(Y_P).
same_subject(X, Y) :- X = pet(X_P), Y = wild(Y_P), X_P = Y_P, ground(X_P), ground(Y_P).
same_subject(X, Y) :- X = wild(X_P), Y = animal(Y_P), X_P = Y_P, ground(X_P), ground(Y_P).

pbl_inbetween(R, X, Y) :- pbl(R, N1, X), pbl(R, N2, Y), pbl(R, N3, Z), N1 < N3, N3 < N2.
pbl_notlast(R, X) :- pbl(R, N1, X), pbl(R, N2, Y), N1 < N2.
pbl_notfirst(R, X) :- pbl(R, N, X), N > 1.

pos_body_true_upto(R, N, X) :- pbl(R, N, X), not pbl_notfirst(R, X), in_AS(X).
pos_body_true_upto(R, N1, X) :- pos_body_true_upto(R, N2, Y), pbl(R, N1, X), in_AS(X), N2 < N1, not pbl_inbetween(R, Y, X), same_subject(Y, X).

pos_body_true(R, X) :- pos_body_true_upto(R, N, Y), same_subject(X, Y), not pbl_notlast(R, X).

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
#show pos_body_true/1.
#show pos_body_true_upto/3.
#show pbl_notlast/2.
#show seen_rule/1.