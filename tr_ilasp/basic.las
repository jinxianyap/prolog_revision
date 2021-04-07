bl(R, P, X) :- pbl(R, P, X, VARS).
bl(R, P, X) :- nbl(R, P, X, VARS).
var_val(R, V, T) :- rule(R), variable(V), ground(T).
is_var_val(var_val(R, V, T)) :- rule(R), variable(V), ground(T).
var_val_equal(VVX, VVY) :- is_var_val(VVX), is_var_val(VVY), VVX = var_val(R, V, T), VVY = var_val(R, V, T).
valid_var_val(RULE_NO, var_val(R, V, T), VAR) :- variable(VAR), rule(R), R = RULE_NO, V = VAR, ground(T).
length(R, end, 0, MAX, end) :- var_max(MAX), rule(R).
length(R, var_vals(VV, VVS), N, MAX, variables(V, VS)) :- valid_var_val(R, VV, V), length(R, VVS, N - 1, MAX, VS), var_max(MAX), N < MAX.
defined_length(R, end, 0) :- rule(R).
defined_length(R, VVS, N) :- variable_list(VS), length(R, VVS, N, MAX, VS), var_num(N), var_num(MAX).
check_sets_length(R, VVXS, VVYS) :- defined_length(R, VVXS, NX), defined_length(R, VVYS, NY), var_num(NX), var_num(NY), NX <= NY.
is_subset_helper(R, end, VVYS) :- defined_length(R, VVYS, _).
is_subset_helper(R, var_vals(VVX, VVXS), var_vals(VVY, VVYS)) :- check_sets_length(R, var_vals(VVX, VVXS), var_vals(VVY, VVYS)), var_val_equal(VVX, VVY), is_subset_helper(R, VVXS, VVYS).
is_subset_helper(R, var_vals(VVX, VVXS), var_vals(VVY, VVYS)) :- check_sets_length(R, var_vals(VVX, VVXS), var_vals(VVY, VVYS)), not var_val_equal(VVX, VVY), is_subset_helper(R, var_vals(VVX, VVXS), VVYS).
is_subset(R, VVXS, VVYS) :- pbl(R, PX, X, VVXS), head(R, Y, VVYS), is_subset_helper(R, VVXS, VVYS).
is_subset(R, VVXS, VVYS) :- nbl(R, PX, X, VVXS), head(R, Y, VVYS), is_subset_helper(R, VVXS, VVYS).
rule_not_first(R) :- order(R_OTHER, R), rule(R), rule(R_OTHER).
seen_rule(R) :- not rule_not_first(R), rule(R), in_AS(X, R, VVXS), head(R, X, VVXS).
seen_rule(R) :- not rule_not_first(R), rule(R), not in_AS(X, R, VVXS), head(R, X, VVXS).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), in_AS(X, R, VVXS), head(R, X, VVXS).
seen_rule(R) :- seen_rule(R_PREV), order(R_PREV, R), rule(R), rule(R_PREV), not in_AS(X, R, VVXS), head(R, X, VVXS).
in_AS(X, R, VVXS) :- head(R, X, VVXS), body_true(R, VVXS).
bl_inbetween(R, X, Y) :- bl(R, PX, X), bl(R, PY, Y), bl(R, PZ, Z), PX < PZ, PZ < PY.
bl_notlast(R, X) :- bl(R, PX, X), bl(R, PY, Y), PX < PY.
bl_notfirst(R, X) :- bl(R, PX, X), PX > 1.
satisfied(R, PX, X, VVYS, pos) :- is_subset(R, VVXS, VVYS), pbl(R, PX, X, VVXS), in_AS(X, R_OTHER, VVS_OTHER), rule(R_OTHER).
satisfied(R, PX, X, VVYS, neg) :- is_subset(R, VVXS, VVYS), nbl(R, PX, X, VVXS), not in_AS(X, _, _).
body_true_upto(R, PX, X, VVYS, PN) :- satisfied(R, PX, X, VVYS, PN), not bl_notfirst(R, X).
body_true_upto(R, PX, X, VVS, PNX) :- satisfied(R, PX, X, VVS, PNX), PX > PY, body_true_upto(R, PY, Y, VVS, PNY), not bl_inbetween(R, Y, X).
body_exists(R) :- bl(R, P, X).
body_true(R, VVS) :- rule(R), head(R, X, VVS), not body_exists(R).
body_true(R, VVS) :- body_true_upto(R, P, X, VVS, PN), not bl_notlast(R, X).
ground(table).
ground(cat).
ground(chair).
variable(var_x).
rule(r1).
head(r1, living(cat), var_vals(var_val(r1, var_x, cat), end)).
rule(r2).
head(r2, furniture(table), var_vals(var_val(r2, var_x, table), end)).
rule(r3).
head(r3, furniture(chair), var_vals(var_val(r3, var_x, chair), end)).
rule(r4).
head(r4, animal(X), var_vals(var_val(r4, var_x, X), end)) :- ground(X).
%pbl(r4, 1, living(X), var_vals(var_val(r4, var_x, X), end)) :- ground(X).
#revisable(rev1, (pbl(r4, 1, furniture(X), var_vals(var_val(r4, var_x, X), end)) :- ground(X).), (X: ground)).
order(r1, r2).
order(r2, r3).
order(r3, r4).
var_num(1..2).
var_max(2).
variable_list(variables(var_x, end)).



%#show in_AS/3.

#pos(eg1, {in_AS(animal(cat), r4, var_vals(var_val(r4, var_x, cat), end))}, {}, {}).
#neg(eg2, {in_AS(animal(chair), r4, var_vals(var_val(r4, var_x, chair), end))}, {}, {}).
#neg(eg3, {in_AS(animal(table), r4, var_vals(var_val(r4, var_x, table), end))}, {}, {}).

#modeh(pbl(const(rule), const(pos), living(var(ground)), var_vals(var_val(const(rule), const(variable), var(ground)), const(var_vals_end)))).

#constant(rule, r4).
#constant(pos, 1).
#constant(variable, var_x).
#constant(var_vals_end, end).