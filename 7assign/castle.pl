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

%reachable(Castle, Room1, Room2)
%true if there exists a path from Room1 to Room2
isReachable(Castle, Room, Room).

isReachable(Castle, Room1, Room2):-
    room(Castle, Room1, RoomMid,_),
    isReachable(Castle, RoomMid, Room2).


printList([]).

% Add your comments here
solveRooms(Castle, L) :-
  printList(NL).

% Add your comments here
solveRoomsWithinCost(Castle, Limit) :-
  printList(NL).

