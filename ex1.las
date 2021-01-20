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
% :- own(X), own(Y), own(Z).

% Hypothesis Space
#modeb(1,use_own(1,1,var(animal))).
#modeb(1,use_own(1,2,var(animal))).
#modeb(1,use_own(1,3,var(animal))).
#modeb(ext_eats(1,var(animal),var(animal))).

use_own(1,1,X) :- own(X).
use_own(1,2,X) :- own(X).
use_own(1,3,X) :- own(X).
ext_eats(1,X,Y) :- eats(X,Y), X != Y.

#maxv(2).