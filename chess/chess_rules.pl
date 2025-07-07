% chess_rules.pl: Define chess move rules in Prolog

% Fact: piece(Color, Type, Row, Col) - Piece at position (Row, Col)
% Color: white, black; Type: pawn, king
% Row, Col: 0..7 (matches ChessEngine.py coordinates)

% Check if a square is empty
empty(Row, Col) :- 
    \+ piece(_, _, Row, Col),
    Row >= 0, Row =< 7, Col >= 0, Col =< 7.

% Valid moves for pawn (white moves up, black moves down)
valid_pawn_move(white, StartRow, StartCol, EndRow, EndCol) :-
    piece(white, pawn, StartRow, StartCol),
    StartRow > 0,
    EndRow is StartRow - 1, EndCol = StartCol,
    empty(EndRow, EndCol).
valid_pawn_move(white, StartRow, StartCol, EndRow, EndCol) :-
    piece(white, pawn, StartRow, StartCol),
    StartRow = 6,
    EndRow is StartRow - 2, EndCol = StartCol,
    empty(EndRow, EndCol),
    MidRow is StartRow - 1, empty(MidRow, EndCol).
valid_pawn_move(white, StartRow, StartCol, EndRow, EndCol) :-
    piece(white, pawn, StartRow, StartCol),
    StartRow > 0,
    EndRow is StartRow - 1,
    (EndCol is StartCol - 1 ; EndCol is StartCol + 1),
    piece(black, _, EndRow, EndCol).

valid_pawn_move(black, StartRow, StartCol, EndRow, EndCol) :-
    piece(black, pawn, StartRow, StartCol),
    StartRow < 7,
    EndRow is StartRow + 1, EndCol = StartCol,
    empty(EndRow, EndCol).
valid_pawn_move(black, StartRow, StartCol, EndRow, EndCol) :-
    piece(black, pawn, StartRow, StartCol),
    StartRow = 1,
    EndRow is StartRow + 2, EndCol = StartCol,
    empty(EndRow, EndCol),
    MidRow is StartRow + 1, empty(MidRow, EndCol).
valid_pawn_move(black, StartRow, StartCol, EndRow, EndCol) :-
    piece(black, pawn, StartRow, StartCol),
    StartRow < 7,
    EndRow is StartRow + 1,
    (EndCol is StartCol - 1 ; EndCol is StartCol + 1),
    piece(white, _, EndRow, EndCol).

% En passant move for pawn
valid_enpassant_move(white, StartRow, StartCol, EndRow, EndCol, EnPassantRow, EnPassantCol) :-
    piece(white, pawn, StartRow, StartCol),
    StartRow = 3,
    EndRow = 2,
    (EndCol is StartCol - 1 ; EndCol is StartCol + 1),
    piece(black, pawn, StartRow, EndCol),
    empty(EndRow, EndCol),
    EnPassantRow = StartRow, EnPassantCol = EndCol.
valid_enpassant_move(black, StartRow, StartCol, EndRow, EndCol, EnPassantRow, EnPassantCol) :-
    piece(black, pawn, StartRow, StartCol),
    StartRow = 4,
    EndRow = 5,
    (EndCol is StartCol - 1 ; EndCol is StartCol + 1),
    piece(white, pawn, StartRow, EndCol),
    empty(EndRow, EndCol),
    EnPassantRow = StartRow, EnPassantCol = EndCol.

% Pawn promotion
valid_pawn_promotion(white, StartRow, StartCol, EndRow, EndCol) :-
    piece(white, pawn, StartRow, StartCol),
    StartRow = 1,
    EndRow = 0,
    EndCol = StartCol,
    empty(EndRow, EndCol).
valid_pawn_promotion(black, StartRow, StartCol, EndRow, EndCol) :-
    piece(black, pawn, StartRow, StartCol),
    StartRow = 6,
    EndRow = 7,
    EndCol = StartCol,
    empty(EndRow, EndCol).

% Valid moves for king
valid_king_move(Color, StartRow, StartCol, EndRow, EndCol) :-
    piece(Color, king, StartRow, StartCol),
    member((DeltaRow, DeltaCol), [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]),
    EndRow is StartRow + DeltaRow, EndCol is StartCol + DeltaCol,
    EndRow >= 0, EndRow =< 7, EndCol >= 0, EndCol =< 7,
    (empty(EndRow, EndCol) ; piece(OtherColor, _, EndRow, EndCol), OtherColor \= Color).

% General valid move check
valid_move(Color, Type, StartRow, StartCol, EndRow, EndCol) :-
    piece(Color, Type, StartRow, StartCol),
    (Type = pawn, valid_pawn_move(Color, StartRow, StartCol, EndRow, EndCol) ;
     Type = pawn, valid_enpassant_move(Color, StartRow, StartCol, EndRow, EndCol, _, _) ;
     Type = pawn, valid_pawn_promotion(Color, StartRow, StartCol, EndRow, EndCol) ;
     Type = king, valid_king_move(Color, StartRow, StartCol, EndRow, EndCol)).

% Query to get all valid moves
get_valid_moves(Color, Type, StartRow, StartCol, EndRow, EndCol) :-
    valid_move(Color, Type, StartRow, StartCol, EndRow, EndCol).