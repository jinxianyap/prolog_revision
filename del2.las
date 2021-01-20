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
% path(X,Y) :- arc(X,Y), arc(Y,X).
% path(X,Y) :- arc(X,Z), path(Z,Y), path(Y,Z).

#pos(p1,{path(1,2),path(1,6),path(2,6)},{path(5,1)}).
#neg(n1,{path(4,2)},{}).

#modeh(path(var(x),var(y)), (anti_reflexive)).
#modeb(1, use_arc(1,1,var(x),var(y)), (anti_reflexive)).
#modeb(1, use_arc(1,2,var(x),var(y)), (anti_reflexive)).
#modeb(1, use_arc(2,1,var(x),var(z)), (anti_reflexive)).
#modeb(1, use_path(2,2,var(y),var(z)), (anti_reflexive)).
#modeb(1, use_path(2,3,var(y),var(z)), (anti_reflexive)).

use_arc(1,1,X,Y) :- arc(X,Y).
use_arc(1,2,X,Y) :- arc(Y,X).
use_arc(2,1,X,Z) :- arc(X,Z).
use_path(2,2,Y,Z) :- path(Z,Y).
use_path(2,3,Y,Z) :- path(Y,Z).
