% Target Program
% tails(V1) :- coin(V1); not heads(V1).
% heads(V1) :- coin(V1); not tails(V1).

% Student Program
% tails(V1) :- not heads(V1).
% heads(V1) :- not tails(V1).

% Background Knowledge
coin(c1).
coin(c2).
coin(c3).


% ASP Meta-representation
tails(X) :- not use(1,1,X), extension(1,X).
heads(X) :- not use(2,1,X), extension(2,X).

use(1,1,X) :- heads(X), not del(1,1).
use(1,1,c1) :- del(1,1).
use(1,1,c2) :- del(1,1).
use(1,1,c3) :- del(1,1).
use(2,1,X) :- tails(X), not del(2,1).
use(2,1,c1) :- del(2,1).
use(2,1,c2) :- del(2,1).
use(2,1,c3) :- del(2,1).
extension(1..2,c1).
extension(1..2,c2).
extension(1..2,c3).


% Fixes
extension(1,X) :- coin(X).
extension(2,X) :- coin(X).