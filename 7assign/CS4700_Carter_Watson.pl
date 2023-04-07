% First castle for testing
% The castle is a set of room facts of the form
% room(Castle, FromRoom, ToRoom, cost).
room(dunstanburgh, enter, foyer, 1).
room(dunstanburgh, foyer, livingRoom, 1).
room(dunstanburgh, foyer, hall, 2).
room(dunstanburgh, hall, kitchen, 4).
room(dunstanburgh, hall, garage, 3).
room(dunstanburgh, kitchen, exit, 1).

% Second castle for testing
room(windsor, enter, foyer, 1).
room(windsor, foyer, hall, 2).
room(windsor, foyer, dungeon, 1).
room(windsor, hall, throne, 1).
room(windsor, hall, stairs, 4).
room(windsor, stairs, dungeon, 3).
room(windsor, throne, stairs, 1).
room(windsor, dungeon, escape, 5).
room(windsor, escape, exit, 1).

% Third castle for testing
room(alnwick, enter, foyer, 1).
room(alnwick, foyer, hall, 2).
room(alnwick, hall, throne, 1).
room(alnwick, hall, stairs, 4).
room(alnwick, stairs, dungeon, 3).
room(alnwick, dungeon, foundry, 5).
room(alnwick, foyer, passage, 1).
room(alnwick, passage, foundry, 1).
room(alnwick, foundry, exit, 4).

printList([]).
printList([A|B]):-
    print(A),
    nl,
    printList(B).

% reachable(Castle, Room1, Room2)
% true if there exists a path from Room1 to Room2
isReachable(_, Room, Room, []).
isReachable(Castle, Room1, Room2, [Room1 | RestPath]):-
    room(Castle, Room1, RoomMid,_),
    isReachable(Castle, RoomMid, Room2, RestPath).

% solveRooms(Castle, VisitRooms)
% Find path to end of castle, through given rooms
solveRooms(Castle, RoomList) :-
    perm(RoomList, PermutedRoomList),
    tour(Castle, enter, PermutedRoomList, Route),
    append(Route, [exit], RouteFinal),
    printList(RouteFinal).

solveRooms(Castle, RoomList, Route) :-
    perm(RoomList, PermutedRoomList),
    tour(Castle, enter, PermutedRoomList, Route).

% tour(Castle, AtRoom, VisitRooms, Route)
% BASE CASE: no more rooms to visit
tour(Castle, AtRoom, [], Route) :-
    isReachable(Castle, AtRoom, exit, Route).
% check tour validity
tour(Castle, AtRoom, [NextRoom | RestRooms], Route) :-
    isReachable(Castle, AtRoom, NextRoom, Path),
    tour(Castle, NextRoom, RestRooms, RestRoute),
    append(Path, RestRoute, Route).

% perm & takeout from lecture/google
takeout(X,[X|R],R).  
takeout(X,[F|R],[F|S]) :-
    takeout(X,R,S).

perm([X|Y],Z) :-
    perm(Y,W),
    takeout(X,Z,W).
perm([],[]).


% ---COST IMPLEMENTATION---
% implementation without rooms
solveRoomsWithinCost(Castle, Limit) :-
    solveRooms(Castle, [], Route),
    append(Route, [exit], RouteFinal),
    findCost(Castle, RouteFinal, Cost),
    Cost =< Limit,
    write('Cost is '), write(Cost), write(' within the limit of '), write(Limit), nl,
    printList(RouteFinal).

% implementation with rooms
solveRoomsWithinCost(Castle, VisitRooms, Limit) :-
    solveRooms(Castle, VisitRooms, Route),
    append(Route, [exit], RouteFinal),
    findCost(Castle, RouteFinal, Cost),
    Cost =< Limit,
    write('Cost is '), write(Cost), write(' within the limit of '), write(Limit), nl,
    printList(RouteFinal).

% --cost helpers
% findCost(Castle, Rooms, Cost)
findCost(_, [], 0).
findCost(_, [_], 0).
% finds the total cost of a passes in route list
findCost(Castle, [Room1, Room2|RestRooms], TotalCost):-
  room(Castle, Room1, Room2, OneCost),
  findCost(Castle, [Room2|RestRooms], RestCost),
  TotalCost is OneCost + RestCost.
