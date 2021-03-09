element(1).
listLen(empty, 0).
listLen(cons(E, L), K + 1) :- element(E); listLen(L, K); K < 5.
is5List(L) :- listLen(L, 5).

#show is5List/1.