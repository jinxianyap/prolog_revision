% animal(cat).

% DEFINING GROUND TERMS AND VARIABLES.

ground(cat).
ground(table).
ground(pencil).

bl(R, N, X) :- pbl(R, N, X, VARS).
bl(R, N, X) :- nbl(R, N, X, VARS).

var_val(R, X, V) :- rule(R), var(X), ground(V).
is_var_val(var_val(R, X, V)) :- rule(R), var(X), ground(V).
var_val_equal(VVX, VVY) :- is_var_val(VVX), is_var_val(VVY), VVX = var_val(R, X, V), VVY = var_val(R, X, V).

% ------------------------------------------------------------------------------------------------------------------
% PROGRAM-SPECIFIC

rule(r1).
head(r1, animal(cat), end) :- ground(cat).

% ------------------------------------------------------------------------------------------------------------------
% CHECKING FOR SUBSETS

var_list(vars(x, end)).
var_list(vars(y, end)).
var_list(vars(z, end)).
var_list(vars(x, vars(y, end))).
var_list(vars(x, vars(z, end))).
var_list(vars(y, vars(z, end))).
var_list(vars(x, vars(y, vars(z, end)))).

var_num(1..4).
var_max(4).

valid_var_val(RULE_NO, var_val(R, X, V), VAR) :- var(VAR), rule(R), R = RULE_NO, X = VAR, ground(V). 
length(R, end, 0, MAX, end) :- var_max(MAX), rule(R).
length(R, var_vals(X, XS), N, MAX, vars(V, VS)) :- valid_var_val(R, X, V), length(R, XS, N - 1, MAX, VS), var_max(MAX), N < MAX.

defined_length(R, end, 0) :- rule(R).
defined_length(R, LS, N1) :- var_list(VS), length(R, LS, N1, MAX, VS), var_num(N1), var_num(MAX).
check_sets_length(R, X, Y) :- defined_length(R, X, N1), defined_length(R, Y, N2), var_num(N1), var_num(N2), N1 <= N2.

is_subset_helper(R, end, Y) :- defined_length(R, Y, _).
is_subset_helper(R, var_vals(X, XS), var_vals(Y, YS)) :- check_sets_length(R, var_vals(X, XS), var_vals(Y, YS)), var_val_equal(X, Y), is_subset_helper(R, XS, YS).
is_subset_helper(R, var_vals(X, XS), var_vals(Y, YS)) :- check_sets_length(R, var_vals(X, XS), var_vals(Y, YS)), not var_val_equal(X, Y), is_subset_helper(R, var_vals(X, XS), YS).

is_subset(R, X, Y) :- pbl(R, N1, P1, X), head(R, N2, Y), is_subset_helper(R, X, Y).
is_subset(R, X, Y) :- nbl(R, N1, P1, X), head(R, N2, Y), is_subset_helper(R, X, Y).

% ------------------------------------------------------------------------------------------------------------------
% PRESERVING ORDERING OF BODY LITERALS AND RULES

in_AS(X, R, VARS) :- head(R, X, VARS), body_true(R, VARS).

body_exists(R) :- bl(R, N, X).
body_true(R, VARS) :- rule(R), head(R, X, VARS), not body_exists(R).

bl_inbetween(R, X, Y) :- bl(R, N1, X), bl(R, N2, Y), bl(R, N3, Z), N1 < N3, N3 < N2.
bl_notlast(R, X) :- bl(R, N1, X), bl(R, N2, Y), N1 < N2.
bl_notfirst(R, X) :- bl(R, N, X), N > 1.

satisfied(R, N, X, VARS, pos) :- is_subset(R, BODY_VARS, VARS), pbl(R, N, X, BODY_VARS), in_AS(X, R1, OTHER_VARS), rule(R1).
satisfied(R, N, X, VARS, neg) :- is_subset(R, BODY_VARS, VARS), nbl(R, N, X, BODY_VARS), not in_AS(X, _, _).

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
