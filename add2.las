arc(1,2).
arc(2,3).
arc(2,4).
arc(3,6).
arc(4,6).
arc(3,5).
arc(6,5).

% Target program
% path(X,Y) :- arc(X,Y).
% path(X,Y) :- arc(X,Z); path(Z,Y).

% Initial program
% path(X,Y) :- arc(X,Y).
% path(X,Y) :- arc(X,Z).

#pos(p1,{path(1,2),path(1,6),path(2,6)},{path(5,1)}).
#neg(n1,{path(4,2)},{}).

path(X,Y) :- use_arc(1,1,X,Y), use_arc(1,2,X,Y), extension(1,X,Y).
path(X,Y) :- use_arc(2,1,X,Z), extension(2,X,Y,Z).

use_arc(1,1,X,Y) :- arc(X,Y), not del(1,1).
use_arc(1,1,1..6,1..6) :- del(1,1).
use_arc(1,2,X,Y) :- arc(Y,X), not del(1,2).
use_arc(1,2,1..6,1..6) :- del(1,2).
use_arc(2,1,X,Z) :- arc(X,Z), not del(2,1).
use_arc(2,1,1..6,1..6) :- del(2,1).
extension(1,1..6,1..6).
extension(2,1..6,1..6).

#modeh(del(1,const(c1))).
#modeh(del(2,const(c2))).
#modeh(extension(const(r))).
#constant(c1,1).
#constant(c1,2).
#constant(c2,1).
#constant(r,1).
#constant(r,2).
#modeb(arc(var(X))).
#modeb(path(var(X),var(X))).