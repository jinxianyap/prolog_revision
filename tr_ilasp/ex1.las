%Mode Declaration
#modeb(c2(var(atom))).
#modeb(c3(var(atom))).

%Background theory
atom(a).
atom(b).
c2(X) :- c3(X).
c3(b).
c2(a).

%Examples
#pos(eg1, {q(a)}, {}, {}).
#pos(eg2, {r(a)}, {}, {}).
#neg(eg4, {q(b)}, {}, {}).
#neg(eg3, {p(a)}, {}, {}).

#revisable(rev1, (p(X) :- c2(X).), (X: atom, Y:atom)).
#modeh(q(var(atom))).
#modeh(r(var(atom))).


% Other ways to define possible head.
%#possible_head(rev1, {p(X), q(X)}).
%#possible_head_modeh(rev1, {q(var(atom)), r(var(atom))}).

% python revision.py --revise-type disjunctive ex1.las
