child(sam,laura).
child(teddy, laura).
exists_child(X,Y):- child(X,Y).
only_child(X,Y):- child(X,Y), not exists_child(Z,Y), X!=Z.

rule(r3).
head(r3, only_child(X, Y)).
pbl(r3, 1, child(X, Y)).
nbl(r3, 2, exists_child(Z, Y)).
