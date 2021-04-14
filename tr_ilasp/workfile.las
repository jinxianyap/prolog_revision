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
ground(cat).
ground(dog).
ground(fish).
variable(var_x).
rule(r1).
head(r1, mammal(dog), var_vals(var_val(r1, var_x, dog), end)).
rule(r2).
head(r2, animal(cat), var_vals(var_val(r2, var_x, cat), end)).
rule(r3).
head(r3, animal(fish), var_vals(var_val(r3, var_x, fish), end)).
rule(r4).
head(r4, animal(dog), var_vals(var_val(r4, var_x, dog), end)).
rule(r5).
head(r5, mammal(cat), var_vals(var_val(r5, var_x, cat), end)).
rule(r6).
head(r6, pet(X), var_vals(var_val(r6, var_x, X), end)) :- ground(X).
order(r1, r2).
order(r2, r3).
order(r3, r4).
order(r4, r5).
order(r5, r6).
var_num(1..2).
var_max(2).
variable_list(variables(var_x, end)).
#constant(rule_id, r6).
#constant(variable, var_x).
#constant(ground_constant, cat).
#constant(ground_constant, dog).
#constant(ground_constant, fish).
#constant(position, 1).
#constant(var_vals_end, end).
#pos(p0, {in_AS(mammal(dog),r1,var_vals(var_val(r1,var_x,dog),end))}, {}, {}).
#pos(p1, {in_AS(mammal(cat),r5,var_vals(var_val(r5,var_x,cat),end))}, {}, {}).
#pos(p2, {in_AS(animal(fish),r3,var_vals(var_val(r3,var_x,fish),end))}, {}, {}).
#pos(p3, {in_AS(animal(dog),r4,var_vals(var_val(r4,var_x,dog),end))}, {}, {}).
#pos(p4, {in_AS(animal(cat),r2,var_vals(var_val(r2,var_x,cat),end))}, {}, {}).
#pos(p5, {in_AS(pet(cat),r6,var_vals(var_val(r6,var_x,cat),end))}, {}, {}).
#pos(p6, {in_AS(pet(dog),r6,var_vals(var_val(r6,var_x,dog),end))}, {}, {}).
#neg(n0, {in_AS(pet(fish),r6,var_vals(var_val(r6,var_x,fish),end))}, {}, {}).
#modeb(ground(var(ground))).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Deletion rules

#modeh(delete(const(revid_type), const(id_type))).
#constant(revid_type, rev1).
#constant(id_type, ground_X).

#bias(":- head(delete(_, _)), body(_).").

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Extension rules and mode declaration

#modeh(extension(rev1, v(var(ground)))).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Mode for revising heads
#modeh(head_delete(const(revid_type), const(hid_type))).
#constant(hid_type, pbl_r6_1_animal_X_var_vals_var_val_r6_var_x_X_end).

#modeh(head_extension(rev1, const(head_extension_type), pbl(r6, 1, mammal(var(ground)), var_vals(var_val(r6, var_x, var(ground)), end)))).
#constant(head_extension_type, pbl_r6_1_mammal_X_var_vals_var_val_r6_var_x_X_end).

#bias(":- head(head_delete(_, _)), body(_).").
#bias(":- head(head_extension(_, _, _)), body(_).").
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
prove(X) : possible_head(R, V, X) :- extension(R, V).
pbl(r6, 1, animal(X), var_vals(var_val(r6, var_x, X), end)) :- prove(pbl(r6, 1, animal(X), var_vals(var_val(r6, var_x, X), end))).
pbl(r6, 1, mammal(X), var_vals(var_val(r6, var_x, X), end)) :- prove(pbl(r6, 1, mammal(X), var_vals(var_val(r6, var_x, X), end))).

%Try and extension rules

possible_head(rev1, v(X), pbl(r6, 1, animal(X), var_vals(var_val(r6, var_x, X), end))) :-
	not head_delete(rev1, pbl_r6_1_animal_X_var_vals_var_val_r6_var_x_X_end),
	try(rev1, ground_X, ground(X)),
	extension(rev1, v(X)).

possible_head(rev1, v(X), pbl(r6, 1, mammal(X), var_vals(var_val(r6, var_x, X), end))) :-
	head_extension(rev1, pbl_r6_1_mammal_X_var_vals_var_val_r6_var_x_X_end, pbl(r6, 1, mammal(X), var_vals(var_val(r6, var_x, X), end))),
	try(rev1, ground_X, ground(X)),
	extension(rev1, v(X)).

possible_head(rev1, v(X), null) :-
	empty_head(rev1),
	ground(X).

possible_head(rev1, v(X), null) :-
	not empty_head(rev1),
	not possible_head(rev1, v(X), pbl(r6, 1, animal(X), var_vals(var_val(r6, var_x, X), end))),
	not possible_head(rev1, v(X), pbl(r6, 1, mammal(X), var_vals(var_val(r6, var_x, X), end))),
	ground(X).

empty_head(rev1) :-
	head_delete(rev1, pbl_r6_1_animal_X_var_vals_var_val_r6_var_x_X_end),
	not head_extension(rev1, pbl_r6_1_mammal_X_var_vals_var_val_r6_var_x_X_end, pbl(r6, 1, mammal(X), var_vals(var_val(r6, var_x, X), end))),
	ground(X).

:- empty_head(rev1),
	try(rev1, ground_X, ground(X)),
	extension(rev1, v(X)).

:- not empty_head(rev1),
	possible_head(rev1, v(X), null): ground(X).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
try(rev1, ground_X, ground(X)) :- 
	delete(rev1, ground_X),
	ground(X).

try(rev1, ground_X, ground(X)) :- 
	ground(X),
	not delete(rev1, ground_X),
	ground(X).

tried(rev1, ground_X) :- 
	try(rev1, ground_X, ground(X)),
	ground(X).

extended(rev1) :- 
	extension(rev1, v(X)),
	ground(X).

:- not tried(rev1, ground_X).

:- not extended(rev1).

