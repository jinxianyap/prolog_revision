% Initial Program
% p(X) :- c1(X), c2(X).

% Target Program
% p(X) :- c1(X).

% B
c1(a). c2(b).

% E
#pos(p1, {p(a)}, {p(b)}).
#neg(n1, {p(b)}, {}).

% M
#modeh(p(var(v1))).
#modeb(use_c1(1,1,var(v1))).
#modeb(use_c2(1,2,var(v1))).

% R
use_c1(1,1,X) :- c1(X).
use_c2(1,2,X) :- c2(X).