% Background Knowledge
animal(cat).    animal(dog).    animal(fish).
eats(cat, fish).    eats(dog, cat).
0 { own(A) } 1 :- animal(A).

% Positive Examples
#pos(p1, { own(fish) }, { own(cat) }).
#pos(p2, { own(dog), own(fish) }, {}).
#pos(p3, { own(dog)}, {own(cat)}).
#neg(n1, {own(fish), own(cat)}, {}).

% Target Program
% :- eats(X, Y), own(X), own(Y).

% Student Program
% :- own(X), own(Y)W.

% Hypothesis Space
#modeb(1,use_own(1,1,var(animal))).
#modeb(1,use_own(1,2,var(animal))).
#modeb(ext_eats(1,var(animal),var(animal))).

use_own(1,1,X) :- own(X).
use_own(1,2,X) :- own(X).
ext_eats(1,X,Y) :- eats(X,Y), X != Y.

#maxv(2).



% for ext_?? rules, take in all variables present in the body but not in the head
% create ext for each possible predicate for each rule
% if for example ext_own, the possible variables X and Y are both represented by own(X) and own(Y) already in this rule, there is no need to extend this rule with a further own(?). In short, if the predicate represented by the ext_ predicate is already in the program, we will not add it to the BG, since it is represented by a dedicated use_ predicate.
% if there is a third variable Z for which we could possibly extend a rule by own(Z), with existing own(X) and own(Y), we need to enforce that ext_own implied by not use_own(_,_,X) and not use_own(_,_,Y).