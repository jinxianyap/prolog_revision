% Target Program
% safe([[],_]) :- !.
% safe([H,Z]) :- length(Z,X),length(H,Y),Y>=X;

% Student Program from sheet7
% safe([[], _]):- !.
% safe([H, Z]):- length(Z, X), length(H, Y), Y >= X.

built-ins: list(), listend(), length(), hole(), cut(), member(), append() + can specify others if needed (need to specify arity and possibly the arg types)
->  list(X) list(X,Y,....) list(X|Y)
    these built-ins act similarly to a var()/const()
    both list variants interchangeable

% Rule 1
#modeh(1,safe(list(X),hole())).
#modeb(1,cut()).

% Rule 2
#modeh(1,safe(list(X,Y))).
#modeb(2,length(X,Y)).
#modeb(1,var(X)>=var(Y)).

% Target Program
% crossing([b | NBank]-SBank, Move, NBankNew-[b | SBankNew]):- pick(NBank, Move, NBankNew), add_new(Move, SBank, SBankNew).
% crossing(NBank-[b | SBank], Move, [b | NBankNew]-SBankNew):- pick(SBank, Move, SBankNew), add_new(Move, NBank, NBankNew).

% Target Program Rep
% Rule 1
% dash is a custom term with arity 2 that we need for this question
#modeh(1, crossing(dash(list(X|Y),Z), M, dash(A,list(X|B))).
#modeb(1, pick(Y,M,A)).
#modeb(1, add_new(M,Z,B)).

% Rule 2
#modeh(1, crossing(dash(Y, list(X|Z)), M, dash(list(X|A), B)).
#modeb(1, pick(Z,M,B)).
#modeb(1, add_new(M,Y,A)).

% Student Program (sheet4)
% crossing( [b, Humans1, Zombies1] - NorthBank, Move, SouthBank - [b, Humans2, Zombies2]) :- !, pick([Humans1, Zombies1], Move, SouthBank), 
%   add_new(Move, NorthBank, [Humans2, Zombies2]).
% crossing(NorthBank - SouthBank, Move, NewNorthBank - NewSouthBank) :- crossing(SouthBank - NorthBank, Move, NewSouthBank - NewNorthBank).

% Student Program Rep
% Rule 1
% dash is a custom term with arity 2 that we need for this question
#modeh(1, crossing(dash(list(B,H1,Z1),N), M, dash(S,list(B,H2,Z2))).
#modeb(1, cut()).
#modeb(1, pick(list(H1,Z1),M,S)).
#modeb(1, add_new(M,N,list(H2,Z2))).

% Rule 2
#modeh(1, crossing(dash(N,S), M, dash(NN,NS)).
#modeb(1, crossing(dash(S,N), M, dash(NS,NN)).

-----------------------------------------------

At this point, we have the 'structure' of the student's program, so we can compare to that of the target program. 1. If the student is missing any clauses/predicates, we can point that out as hints.
2. If all the clauses/predicates match in general, then the problem is with the variables + how they are represented (particularly with lists). We can then compare the structure of the list variables, and indicate which are wrong.

* cannot recognise helpers

General flow: we will parse each line, turning each line into objects so we can keep track of the predicates, its location (head or body), how many times it occurs, arity, arguments, and shape of arguments. (can be a custom object/don't have to use mode declarations like ILASP) This approach is purely syntactic, and does not interpret the program semantically. Unable to find existing approaches for semantic analysis + program repair of lists.

Feedback generated: can only tell students missing clauses/suggest which to use, and also indicate that a particular variable is wrong. Can potentially suggest replacements without the exact variables used (ie safe([[x,x,x],[x,x]]) instead of safe([[h,h,h],[z,z]])) just because we don't know what the actual elements in the list might be. Then again we can use a global repo of object mapped to variable names, and from here try to unify/identify mismatched variables! 

Main drawback of syntactic analysis: cannot give suggestions for an unseen approach.

Requirements: Distance measure to decide which target program to use for feedback generation. A simplistic approach would be assigning weighted scores to length of program, differences in predicates,arity,clauses,list lengths etc. And combined with differences between derivable facts from common queries (disregard if the program is unsatisfiable/erroneous).

