% Target program
% path(X,Y) :- arc(X,Y).
% path(X,Y) :- arc(X,Z); path(Z,Y).

% Initial program
% path(X,Y) :- arc(X,Y), arc(Y,X).
% path(X,Y) :- arc(X,Z).


% Background Knowledge
arc(1,2).
arc(2,3).
arc(2,4).
arc(3,6).
arc(4,6).
arc(3,5).
arc(6,5).


% ASP Meta-representation
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

% Fixes
extension(2,1..6,Y,Z) :- path(Z,Y).
del(1,2).