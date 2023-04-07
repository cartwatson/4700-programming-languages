test1() :- writeln('solveRoomsWithinCost(dunstanburgh, 8)'),
           solveRoomsWithinCost(dunstanburgh, 8).
test2() :- writeln('solveRoomsWithinCost(windsor, 13)'),
           solveRoomsWithinCost(windsor, 13).
test3() :- writeln('solveRoomsWithinCost(alnwick, 15)'),
           solveRoomsWithinCost(alnwick, 15).
test4() :- writeln('solveRooms(dunstanburgh, [foyer, kitchen])'),
           solveRooms(dunstanburgh, [foyer, kitchen]).
test5() :- writeln('solveRooms(windsor, [stairs])'),
           solveRooms(windsor, [stairs]).
test6() :- writeln('solveRooms(alnwick, [foyer, hall])'),
           solveRooms(alnwick, [foyer, hall]).
test7() :- writeln('solveRooms(alnwick, [foyer, passage])'),
           solveRooms(alnwick, [foyer, passage]).
test8() :- writeln('fails: solveRooms(alnwick, [foyer, throne, escape])'),
           solveRooms(alnwick, [foyer, throne, passage]).
test9() :- writeln('fails: solveRoomsWithinCost(alnwick, [foyer, foundry], 4)'),
           solveRoomsWithinCost(alnwick, [foyer, foundry], 4).
test10() :- writeln('solveRoomsWithinCost(alnwick, [foyer, foundry], 20)'),
           solveRoomsWithinCost(alnwick, [foyer, foundry], 20).
test11() :- writeln('solveRoomsWithinCost(alnwick, [foyer, foundry], 8)'),
           solveRoomsWithinCost(alnwick, [foyer, foundry], 8).

