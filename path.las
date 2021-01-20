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

#pos(p1,{path(1,2),path(1,6),path(2,6)},{path(5,1)}).
#neg(n1,{path(4,2)},{}).

#modeh(1,path(var(node),var(node)),(anti_reflexive)).
#modeb(1,arc(var(node),var(node)),(anti_reflexive)).
#modeb(1,path(var(node),var(node)),(anti_reflexive)).