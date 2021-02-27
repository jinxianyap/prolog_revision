%Target hypothesis:
%path(X, Y) :- arc(X, Y).
%path(X, Y) :- arc(X, Z), path(Z, Y).
%Current hypothesis:
%path(X, Y) :- arc(X, Y).
%path(X, Y) :- path(Y, Z).

node(1..6).

% Additions to the BG from the hypothesis
rule(r1).
rule(r2).
head(R, path(X, Y)) :- node(X), node(Y), rule(R).

%REVISABLE:
path(X,Y) :- head(R, path(X, Y)), pbl(r1, arc(X, Y)).
path(X,Y) :- head(R, path(X, Y)), pbl(r2, path(Y, X)).

%BG:
rule_bg(rbg1).
head(rbg1, arc(1,2)).
rule_bg(rbg2).
head(rbg2, arc(2,3)).
rule_bg(rbg3).
head(rbg3, arc(2,4)).
rule_bg(rbg4).
head(rbg4, arc(3,6)).
rule_bg(rbg5).
head(rbg5, arc(4,6)).
rule_bg(rbg6).
head(rbg6, arc(3,5)).
rule_bg(rbg7).
head(rbg7, arc(6,5)).


pbl(R, arc(X, Y)) :- head(R_bg, arc(X, Y)), rule_bg(R_bg), rule(R), node(X), node(Y).
% for recursive pbl
pbl(R, path(X, Y)) :- path(X, Y), rule(R), node(X), node(Y).

%Examples:
%#pos(p1,{path(1,2) path(2,3) path(2,4) path(3,6) path(4,6) path(3,5) path(6,5) path(1,3) path(1,4) path(2,6) path(2,5) path(4,5) path(1,6) path(1,5)},{}).
%#neg(n1,{path(4,2)},{}).

%Mode declarations:
%#modeb(pbl(const(rn), arc(var(node), var(node)))).
%#modeb(pbl(const(rn), path(var(node), var(node)))).
%#constant(rn, r1).
%#constant(rn, r2).
