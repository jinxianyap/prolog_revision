item(a).

cons(a,empty).
cons(a,L) :- cons(L).

#pos(p1,{listLen(cons(a,empty),1)},{listLen(cons(a,empty),0),listLen(cons(a,empty),2),listLen(cons(a,empty),3),listLen(cons(a,empty),4)}).
#pos(p2,{listLen(cons(a,con(a,empty)),2)},{listLen(cons(a,con(a,empty)),0),listLen(cons(a,con(a,empty)),1),listLen(cons(a,con(a,empty)),3)}).

% Sample Student Program
% listLen(empty, 0).
% listLen(cons(E, L), K + 1) :- item(E); listLen(L, K);

#modeh(1,listLen(const(e),const(k))).
#modeh(1,listLen(cons(var(item),var(cons)),var(k)+const(k))).

#modeb(1,item(var(item))).
#modeb(1,listLen(var(cons),var(k))).

#constant(e,empty).
#constant(k,0).
#constant(k,1).