% Initial Program
% p(X) :- c1(X); c2(X).

% Target Program
% p(X) :- c2(X); c3(X).

% B
c2(X) :- c3(X).
c3(b).
c2(a).

% E
#pos(p1, {p(b)}, {p(a)}).

% M
#modeh(p(var(v1))).
#modeb(c1(var(v1))).
#modeb(c2(var(v1))).
#modeb(c3(var(v1))).

% R
p(X) :- try(1,1); try(1,2); extension(1).
try(1,1) :- use(1,1).
try(1,1) :- not use(1,1).
try(1,2) :- use(1,2).
try(1,2) :- not use(1,2).
use(X,Y) :- not del(X,Y).

% M'
#modeh(extension(const(x))).
#modeh(del(const(x),const(x))).
#constant(x,1).


