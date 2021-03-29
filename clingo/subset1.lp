ground(1..6).
var(x).
var(y).
var(z).
rule(r1).
rule(r2).

var_list(vars(x, end)).
var_list(vars(y, end)).
var_list(vars(z, end)).
var_list(vars(x, vars(y, end))).
var_list(vars(x, vars(z, end))).
var_list(vars(y, vars(z, end))).
%var_list(vars(y, vars(x, end))).
%var_list(vars(z, vars(y, end))).
%var_list(vars(z, vars(x, end))).
var_list(vars(x, vars(y, vars(z, end)))).
%var_list(vars(x, vars(z, vars(y, end)))).
%var_list(vars(y, vars(x, vars(z, end)))).
%var_list(vars(y, vars(z, vars(x, end)))).
%var_list(vars(z, vars(x, vars(y, end)))).
%var_list(vars(z, vars(y, vars(x, end)))).

var_val(R, X, V) :- rule(R), var(X), ground(V).
is_var_val(var_val(R, X, V)) :- rule(R), var(X), ground(V).
var_val_equal(VVX, VVY) :- is_var_val(VVX), is_var_val(VVY), VVX = var_val(R, X, V), VVY = var_val(R, X, V).

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


#show is_subset_helper/3.