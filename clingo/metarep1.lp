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
ground(3).
ground(4).
ground(6).
ground(5).
ground(1).
ground(2).
variable(var_x).
variable(var_y).
variable(var_z).
rule(r1).
head(r1, arc(2,4), var_vals(var_val(r1, var_x, 2), var_vals(var_val(r1, var_y, 4), end))).
rule(r2).
head(r2, arc(4,6), var_vals(var_val(r2, var_x, 4), var_vals(var_val(r2, var_y, 6), end))).
rule(r3).
head(r3, arc(3,5), var_vals(var_val(r3, var_x, 3), var_vals(var_val(r3, var_y, 5), end))).
rule(r4).
head(r4, arc(6,5), var_vals(var_val(r4, var_x, 6), var_vals(var_val(r4, var_y, 5), end))).
rule(r5).
head(r5, arc(1,2), var_vals(var_val(r5, var_x, 1), var_vals(var_val(r5, var_y, 2), end))).
rule(r6).
head(r6, arc(2,3), var_vals(var_val(r6, var_x, 2), var_vals(var_val(r6, var_y, 3), end))).
rule(r7).
head(r7, arc(3,6), var_vals(var_val(r7, var_x, 3), var_vals(var_val(r7, var_y, 6), end))).
rule(r8).
head(r8, path(X, Y), var_vals(var_val(r8, var_x, X), var_vals(var_val(r8, var_y, Y), end))) :- ground(X), ground(Y).
pbl(r8, 1, arc(X, Y), var_vals(var_val(r8, var_x, X), var_vals(var_val(r8, var_y, Y), end))) :- ground(X), ground(Y).
rule(r9).
head(r9, path(X, Y), var_vals(var_val(r9, var_x, X), var_vals(var_val(r9, var_y, Y), var_vals(var_val(r9, var_z, Z), end)))) :- ground(X), ground(Y), ground(Z).
pbl(r9, 1, arc(X, Z), var_vals(var_val(r9, var_x, X), var_vals(var_val(r9, var_z, Z), end))) :- ground(X), ground(Z).
pbl(r9, 2, path(Z, Y), var_vals(var_val(r9, var_y, Y), var_vals(var_val(r9, var_z, Z), end))) :- ground(Z), ground(Y).
order(r1, r2).
order(r2, r3).
order(r3, r4).
order(r4, r5).
order(r5, r6).
order(r6, r7).
order(r7, r8).
order(r8, r9).
var_num(1..4).
var_max(4).
variable_list(variables(var_x, end)).
variable_list(variables(var_x, variables(var_y, end))).
variable_list(variables(var_x, variables(var_y, variables(var_z, end)))).
variable_list(variables(var_x, variables(var_z, end))).
variable_list(variables(var_y, end)).
variable_list(variables(var_y, variables(var_z, end))).
variable_list(variables(var_z, end)).
#show in_AS/3.
