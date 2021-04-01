%Target hypothesis:
arc(2,4).
arc(4,6).
arc(3,5).
arc(6,5).
arc(1,2).
arc(2,3).
arc(3,6).

path(X, Y) :- arc(X, Y).
path(X, Y) :- arc(X, Z), path(Z, Y).