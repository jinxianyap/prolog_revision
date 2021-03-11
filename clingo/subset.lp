var_num(1).
ground(cat).
ground(fish).
%ground(dog).

%length(end, 0).
%length(var(X, XS), N + 1) :- ground(X), length(XS, N), var_num(n).

length(end, 0, MAX) :- var_num(MAX).
length(vars(X, XS), N, MAX) :- ground(X), length(XS, N - 1, MAX), var_num(MAX), N < MAX.

defined_length(end, 0).
defined_length(vars(X, XS), N1) :- length(vars(X, XS), N1, MAX), var_num(N1), var_num(MAX).
check_sets_length(X, Y) :- var_num(N1), var_num(N2), N1 <= N2, defined_length(X, N1), defined_length(Y, N2).

%is_subset_helper(end, Y) :- defined_length(Y, _).
%is_subset_helper(vars(X, XS), vars(Y, YS)) :- check_sets_length(vars(X, XS), vars(Y, YS)), ground(X), ground(Y), X = Y, is_subset_helper(XS, YS).
%is_subset_helper(vars(X, XS), vars(Y, YS)) :- check_sets_length(vars(X, XS), vars(Y, YS)), ground(X), ground(Y), X != Y, is_subset_helper(vars(X, XS), YS).

is_subset_helper(end, Y) :- defined_length(Y, _).
is_subset_helper(vars(X, XS), Y) :- check_sets_length(vars(X, XS), Y), ground(X), in_set(X, Y, YS), is_subset_helper(XS, YS).

in_set(X, vars(Y, YS), YS) :- ground(X), ground(Y), X = Y, defined_length(YS, N).
in_set(X, vars(Y, YS), vars(Y, YSS)) :- ground(X), ground(Y), X != Y, in_set(X, YS, YSS), var_num(N), defined_length(YS, N).


%#show is_subset_helper/2.
#show in_set/3.