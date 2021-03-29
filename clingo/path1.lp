%path(X, Y) :- arc(X, Y).
%path(X, Y) :- arc(X, Z), path(Z, Y).

ground(1..6).

bl(R, N, X) :- pbl(R, N, X, VARS).
bl(R, N, X) :- nbl(R, N, X, VARS).

rule(r1).
head(r1, path(X, Y), vars(X, vars(Y, end))) :- ground(X), ground(Y).
pbl(r1, 1, arc(X, Y), vars(X, vars(Y, end))) :- ground(X), ground(Y).

rule(r2).
head(r2, path(X, Y), vars(X, vars(Y, vars(Z, end)))) :- ground(X), ground(Y), ground(Z).
pbl(r2, 1, arc(X, Z), vars(X, vars(Z, end))) :- ground(X), ground(Z).
pbl(r2, 2, path(Z, Y), vars(Z, vars(Y, end))) :- ground(Y), ground(Z).

rule(r3).
head(r3, arc(2,4), vars(2, vars(4, end))).
rule(r4).
head(r4, arc(3,6), vars(3, vars(6, end))).
rule(r5).
head(r5, arc(4,6), vars(4, vars(6, end))).
rule(r6).
head(r6, arc(3,5), vars(3, vars(5, end))).
rule(r7).
head(r7, arc(6,5), vars(6, vars(5, end))).
rule(r8).
head(r8, arc(1,2), vars(1, vars(2, end))).
rule(r9).
head(r9, arc(2,3), vars(2, vars(3, end))).

order(r3, r4).
order(r4, r5).
order(r5, r6).
order(r6, r7).
order(r7, r8).
order(r8, r9).
order(r9, r1).
order(r1, r2).

% ------------------------------------------------------------------------------------------------------------------
% CHECKING FOR SUBSETS

var_num(1..4).
length(end, 0, MAX) :- var_num(MAX).
length(vars(X, XS), N, MAX) :- ground(X), length(XS, N - 1, MAX), var_num(MAX), N < MAX.

defined_length(end, 0).
defined_length(vars(X, XS), N1) :- length(vars(X, XS), N1, MAX), var_num(N1), var_num(MAX).
check_sets_length(X, Y) :- var_num(N1), var_num(N2), N1 <= N2, defined_length(X, N1), defined_length(Y, N2).

in_set(X, vars(Y, YS), YS) :- ground(X), ground(Y), X = Y, defined_length(YS, N).
in_set(X, vars(Y, YS), vars(Y, YSS)) :- ground(X), ground(Y), X != Y, in_set(X, YS, YSS), var_num(N), defined_length(YS, N).

is_subset_helper(end, Y) :- defined_length(Y, _).
is_subset_helper(vars(X, XS), Y) :- check_sets_length(vars(X, XS), Y), ground(X), in_set(X, Y, YS), is_subset_helper(XS, YS).

is_subset(X, Y) :- pbl(R1, N1, P1, X), head(R2, N2, Y), is_subset_helper(X, Y).
is_subset(X, Y) :- nbl(R1, N1, P1, X), head(R2, N2, Y), is_subset_helper(X, Y).

% ------------------------------------------------------------------------------------------------------------------
% PRESERVING ORDERING OF BODY LITERALS AND RULES

in_AS(X, R, VARS) :- head(R, X, VARS), body_true(R, VARS).

body_exists(R) :- bl(R, N, X).
body_true(R, VARS) :- rule(R), head(R, X, VARS), not body_exists(R).

bl_inbetween(R, X, Y) :- bl(R, N1, X), bl(R, N2, Y), bl(R, N3, Z), N1 < N3, N3 < N2.
bl_notlast(R, X) :- bl(R, N1, X), bl(R, N2, Y), N1 < N2.
bl_notfirst(R, X) :- bl(R, N, X), N > 1.

satisfied(R, N, X, VARS, pos) :- is_subset(BODY_VARS, VARS), pbl(R, N, X, BODY_VARS), in_AS(X, R1, BODY_VARS), rule(R1).
satisfied(R, N, X, VARS, neg) :- is_subset(BODY_VARS, VARS), nbl(R, N, X, BODY_VARS), not in_AS(X, _, _).

body_true_upto(R, N, X, VARS, T) :- satisfied(R, N, X, VARS, T), not bl_notfirst(R, X).
body_true_upto(R, N1, X, VARS, T1) :- satisfied(R, N1, X, VARS, T1), N2 < N1, body_true_upto(R, N2, Y, VARS, T2), not bl_inbetween(R, Y, X).
body_true(R, VARS) :- body_true_upto(R, N, Y, VARS, T), not bl_notlast(R, Y).

rule_not_first(R) :- order(R_OTHER, R), rule(R), rule(R_OTHER).
seen_rule(R) :- not rule_not_first(R), rule(R), in_AS(X, R, SUBJECT), head(R, X, SUBJECT).
seen_rule(R) :- not rule_not_first(R), rule(R), not in_AS(X, R, SUBJECT), head(R, X, SUBJECT).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), in_AS(X, R, SUBJECT), head(R, X, SUBJECT).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), not in_AS(X, R, SUBJECT), head(R, X, SUBJECT).

% ------------------------------------------------------------------------------------------------------------------


#show in_AS/3.
%#show body_true/2.
%#show body_true_upto/5.
%#show bl_notlast/2.
%#show seen_rule/1.
%#show bl/3.
%#show is_subset/2.

%#show satisfied/5.
