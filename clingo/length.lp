var_num(1..5).
ground(item).

length(end, 0, MAX) :- var_num(MAX).
length(var(X, XS), N + 1, MAX) :- ground(X), length(XS, N, MAX), var_num(MAX), N < MAX.
check_length(var(X, XS), N) :- list(var(X, XS)), length(var(X, XS), N, N).

list(var(item, end)).
