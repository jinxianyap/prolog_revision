% Background Knowledge
animal(cat).    animal(dog).    animal(fish).
eats(cat, fish).    eats(dog, cat).
0 { own(A) } 1 :- animal(A).

% Positive Examples
#pos(p1, { own(fish) }, { own(cat) }).               #pos(p2, { own(dog), own(fish) }, {}).

#neg(n1, {own(fish), own(cat)}, {}).

% Sample Student Program
% :- eats(X, Y); own(X); own(Y).

% Hypothesis Space
#modeb(2,own(var(animal))).
#modeb(1,eats(var(animal),var(animal)), (anti_reflexive)).


