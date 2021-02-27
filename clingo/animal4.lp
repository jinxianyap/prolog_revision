%Current hypothesis:
%pet(X) :- animal(X).
%wild(X) :- mammal(X).

ground(cat).
ground(fish).

% Additions to the BG from the hypothesis
rule(r1).
head(r1, pet(X)) :- ground(X).
pbl(r1, animal(X)) :- ground(X).
pbl(r1, mammal(X)) :- ground(X).
pbl(r1, wild(X)) :- ground(X).

rule(r2).
head(r2, wild(X)) :- ground(X).
pbl(r2, animal(X)) :- ground(X).

rule(r3).
head(r3, animal(cat)).
rule(r4).
head(r4, animal(fish)).
rule(r5).
head(r5, mammal(cat)).

in_AS(X) :- head(R, X), pos_body_true(R), not neg_body_false(R).
pos_body_exists(R) :- pbl(R, X).
pos_body_true(R) :- rule(R), not pos_body_exists(R).

pbl_inbetween(R, X, Y) :- pbl(R, X), pbl(R, Y), pbl(R, Z), X < Z, Z < Y.
pbl_notlast(R, X) :- pbl(R, X), pbl(R, Y), X < Y.
pbl_notfirst(R, X) :- pbl(R, X), pbl(R, Y), Y < X.
% comparison done on lexicographical order
% how to enforce that the subject of predicates X Y and Z should be the same?

pos_body_true_upto(R, X) :- pbl(R, X), not pbl_notfirst(R, X), in_AS(X).
pos_body_true_upto(R, X) :- pos_body_true_upto(R, Y), pbl(R, X), in_AS(X), Y < X, not pbl_inbetween(R, Y, X).
pos_body_true(R) :- pos_body_true_upto(R, X), not pbl_notlast(R, X).

#show in_AS/1.
#show pos_body_true/1.
#show pos_body_true_upto/2.
#show pbl_notlast/2.