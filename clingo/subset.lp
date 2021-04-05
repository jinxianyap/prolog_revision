var_num(1..4).
var_max(4).

ground(1).
ground(2).
ground(3).
variable(var_x).
variable(var_y).
variable(var_z).

variable_list(variables(var_x, end)).
variable_list(variables(var_x, variables(var_y, end))).
variable_list(variables(var_x, variables(var_y, variables(var_z, end)))).
variable_list(variables(var_x, variables(var_z, end))).
variable_list(variables(var_y, end)).
variable_list(variables(var_y, variables(var_z, end))).
variable_list(variables(var_z, end)).

rule(r1).

var_val(R, V, T) :- rule(R), variable(V), ground(T).
is_var_val(var_val(R, V, T)) :- rule(R), variable(V), ground(T).
var_val_equal(VVX, VVY) :- is_var_val(VVX), is_var_val(VVY), VVX = var_val(R, V, T), VVY = var_val(R, V, T).
valid_var_val(RULE_NO, var_val(R, V, T), VAR) :- variable(VAR), rule(R), R = RULE_NO, V = VAR, ground(T).

length(R, end, 0, MAX, end) :- var_max(MAX), rule(R).
length(R, var_vals(VV, VVS), N, MAX, variables(V, VS)) :- valid_var_val(R, VV, V), length(R, VVS, N - 1, MAX, VS), var_max(MAX), N < MAX.

defined_length(R, end, 0) :- rule(R).
defined_length(R, VVS, N) :- variable_list(VS), length(R, VVS, N, MAX, VS), var_num(N), var_num(MAX).
check_sets_length(R, VVXS, VVYS) :- defined_length(R, VVXS, NX), defined_length(R, VVYS, NY), var_num(NX), var_num(NY), NX <= NY.

%#show length/5.
#show check_sets_length/3.