% Target Program
% tails(V1) :- coin(V1); not heads(V1).
% heads(V1) :- coin(V1); not tails(V1).

% Student Program
% tails(V1) :- not heads(V1).
% heads(V1) :- not tails(V1).

#pos({heads(c1), tails(c2), heads(c3)}, {tails(c1), heads(c2), tails(c3)}).
#pos({heads(c1), heads(c2), tails(c3)}, {tails(c1), tails(c2), heads(c3)}).

coin(c1).
coin(c2).
coin(c3).

#modeh(heads(var(coin))).
#modeh(tails(var(coin))).

#modeb(1,use_heads(1,1,var(coin))).
#modeb(1,use_tails(2,1,var(coin))).

#modeb(ext_tails(1,var(coin))).
#modeb(ext_coin(1,var(coin))).

#modeb(ext_heads(2,var(coin))).
#modeb(ext_coin(2,var(coin))).

use_heads(1..2,1,X) :- heads(X).
ext_tails(1,X) :- tails(X).
ext_heads(2,X) :- heads(X).
ext_coin(1..2,X) :- coin(X).

% from this example we have 2 problems.
% (1) sometimes the ext_ predicates replace the original use_ predicates.
% (2) wrong rule index.