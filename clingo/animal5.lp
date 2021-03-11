%pet(X) :- animal(X), not mammal(X), wild(X).
%wild(X) :- animal(X).

ground(cat).
ground(fish).

bl(R, N, X) :- pbl(R, N, X, VARS).
bl(R, N, X) :- nbl(R, N, X, VARS).

rule(r1).
head(r1, pet(X), vars(X, end)) :- ground(X).
pbl(r1, 1, animal(X), vars(X, end)) :- ground(X).
nbl(r1, 2, mammal(X), vars(X, end)) :- ground(X).
pbl(r1, 3, wild(X), vars(X, end)) :- ground(X).

rule(r2).
head(r2, wild(X), vars(X, end)) :- ground(X).
pbl(r2, 1, animal(X), vars(X, end)) :- ground(X).

rule(r3).
head(r3, animal(cat), vars(cat, end)).
rule(r4).
head(r4, animal(fish), vars(fish, end)).
rule(r5).
head(r5, mammal(cat), vars(cat, end)).

%------------------------------------------------------------------------------------------------------------------
% is_subset(X, Y) checks that the set/list of variables X is a subset of Y.
var_num(1..5).
length(end, 0, MAX) :- var_num(MAX).
length(vars(X, XS), N, MAX) :- ground(X), length(XS, N - 1, MAX), var_num(MAX), N < MAX.

defined_length(end, 0).
defined_length(vars(X, XS), N1) :- length(vars(X, XS), N1, MAX), var_num(N1), var_num(MAX).
check_sets_length(X, Y) :- var_num(N1), var_num(N2), N1 <= N2, defined_length(X, N1), defined_length(Y, N2).

in_set(X, vars(Y, YS), YS) :- ground(X), ground(Y), X = Y, defined_length(YS, N).
in_set(X, vars(Y, YS), vars(Y, YSS)) :- ground(X), ground(Y), X != Y, in_set(X, YS, YSS), var_num(N), defined_length(YS, N).

is_subset_helper(end, Y) :- defined_length(Y, _).
is_subset_helper(vars(X, XS), Y) :- check_sets_length(vars(X, XS), Y), ground(X), in_set(X, Y, YS), is_subset_helper(XS, YS).

is_subset(X, Y) :- pbl(R1, N1, P1, X), head(R1, N2, Y), is_subset_helper(X, Y).
is_subset(X, Y) :- nbl(R1, N1, P1, X), head(R1, N2, Y), is_subset_helper(X, Y).

in_AS(X, R, VARS) :- head(R, X, VARS), body_true(R, VARS).

body_exists(R) :- bl(R, N, X).
body_true(R, VARS) :- rule(R), head(R, X, VARS), not body_exists(R).

bl_inbetween(R, X, Y) :- bl(R, N1, X), bl(R, N2, Y), bl(R, N3, Z), N1 < N3, N3 < N2.
bl_notlast(R, X) :- bl(R, N1, X), bl(R, N2, Y), N1 < N2.
bl_notfirst(R, X) :- bl(R, N, X), N > 1.

% instead of using same_subject to ensure that for example, in wild(X) :- animal(X) the X variable is the same in both literals, we use is_subset.
% The head literal of each rule has a VARS set, which is the set of ALL variables appearing in that rule. (eg path(X, Y) :- arc(X,Z), path(Z,Y) would give head(R, path(X, Y), vars(X, vars(Y, vars(Z, end))))).
% VARS is passed down from the head literal of the rule R, so we check that BODY_VARS (all variables appearing in the body literal), also appear in VARS. For example, if we have head(r1, pet(cat), vars(cat, end)), then for every pbl(r1, N, X, BODY_VARS) BODY_VARS must be a subset of vars(cat, end).
% The 'list' representation of vars(X, vars(Y, vars(Z, ........ end))) is to cater for cases where there is more than one variable in a rule, and where each body literal can have different numbers of variables.
satisfied(R, N, X, VARS, pos) :- is_subset(BODY_VARS, VARS), pbl(R, N, X, BODY_VARS), in_AS(X, R1, VARS), rule(R1).
satisfied(R, N, X, VARS, neg) :- is_subset(BODY_VARS, VARS), nbl(R, N, X, BODY_VARS), not in_AS(X, _, _).

body_true_upto(R, N, X, VARS, T) :- satisfied(R, N, X, VARS, T), not bl_notfirst(R, X).
body_true_upto(R, N1, X, VARS, T1) :- satisfied(R, N1, X, VARS, T1), N2 < N1, body_true_upto(R, N2, Y, VARS, T2), not bl_inbetween(R, Y, X).
body_true(R, VARS) :- body_true_upto(R, N, Y, VARS, T), not bl_notlast(R, Y).

order(r3, r4).
order(r4, r5). 
order(r5, r1).
order(r1, r2).
rule_not_first(R) :- order(R_OTHER, R), rule(R), rule(R_OTHER).
seen_rule(R) :- not rule_not_first(R), rule(R), in_AS(X, R, SUBJECT), head(R, X, SUBJECT).
seen_rule(R) :- not rule_not_first(R), rule(R), not in_AS(X, R, SUBJECT), head(R, X, SUBJECT).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), in_AS(X, R, SUBJECT), head(R, X, SUBJECT).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), not in_AS(X, R, SUBJECT), head(R, X, SUBJECT).


#show in_AS/3.
#show body_true/2.
#show body_true_upto/5.
%#show satisfied/5.
%#show is_subset/2.
%#show is_subset_helper/2.
%#show pbl/4.

