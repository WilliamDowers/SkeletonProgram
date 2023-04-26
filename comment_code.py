# Skeleton Program code for the AQA A Level Paper 1 Summer 2023 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.9 programming environment
# to use random now you have to do random.randint(start, stop) weird
import random

# Dastan explained https://youtu.be/0hJCHhh2gOs


class Dastan:
    def __init__(self, R, C, NoOfPieces):  # intialised at the start with (6,6,4)
        self._Board = []
        self._Players = []
        self._MoveOptionOffer = []
        self._Players.append(
            Player("Player One", 1)
        )  # instantiates two player objects, appends them to _Players list
        self._Players.append(Player("Player Two", -1))
        self.__CreateMoveOptions()  # populates each players move option queue.
        self._NoOfRows = R
        self._NoOfColumns = C
        self._MoveOptionOfferPosition = 0
        self.__CreateMoveOptionOffer()  # creates a list of move option offers
        self.__CreateBoard()  # populates the _BoardQueue using the Sqaure and Kolta Class
        self.__CreatePieces(NoOfPieces)
        self._CurrentPlayer = self._Players[
            0
        ]  # player 1 will always start, initialised as the current player

    def __DisplayBoard(self):
        print("\n" + "   ", end="")
        for Column in range(1, self._NoOfColumns + 1):
            print(str(Column) + "  ", end="")  # 1,2,3,4,5,6 on the columns
        print("\n" + "  ", end="")
        for Count in range(1, self._NoOfColumns + 1):
            print("---", end="")
        print("-")
        for Row in range(1, self._NoOfRows + 1):
            print(str(Row) + " ", end="")  # 1,2,3,4,5,6 on rows
            for Column in range(1, self._NoOfColumns + 1):
                Index = self.__GetIndexOfSquare(Row * 10 + Column)
                print("|" + self._Board[Index].GetSymbol(), end="")
                PieceInSquare = self._Board[Index].GetPieceInSquare()
                if PieceInSquare is None:
                    print(" ", end="")
                else:
                    print(PieceInSquare.GetSymbol(), end="")
            print("|")
        print("  -", end="")
        for Column in range(1, self._NoOfColumns + 1):
            print("---", end="")
        print()
        print()

    def __DisplayState(self):
        self.__DisplayBoard()
        print(
            "Move option offer: " + self._MoveOptionOffer[self._MoveOptionOfferPosition]
        )
        print()
        print(self._CurrentPlayer.GetPlayerStateAsString())
        print("Turn: " + self._CurrentPlayer.GetName())
        print()

    def __GetIndexOfSquare(
        self, SquareReference
    ):  # converts the square reference to row and column e.g. input(23) row = 23//2 = 2 col = 23%10 = 3 return(1*6 + 2 = 8) WORKS!
        Row = SquareReference // 10
        Col = SquareReference % 10
        return (Row - 1) * self._NoOfColumns + (Col - 1)

    def __CheckSquareInBounds(self, SquareReference):
        Row = SquareReference // 10                   #gets the row and column through normal methods of integer division by 2 and mod 10 respectively
        Col = SquareReference % 10
        if Row < 1 or Row > self._NoOfRows:     # checks against the parameters initialised for dastan at the beginning
            return False
        elif Col < 1 or Col > self._NoOfColumns:
            return False
        else:
            return True

    def __CheckSquareIsValid(self, SquareReference, StartSquare):
        if not self.__CheckSquareInBounds(SquareReference):    # if not in bounds it will return false
            return False
        PieceInSquare = self._Board[
            self.__GetIndexOfSquare(SquareReference)
        ].GetPieceInSquare()                           # checks whether a piece exists within that square using the board list, and square class.
        if PieceInSquare is None:
            if StartSquare:
                return False          # if there is no piece in the square, and this is the startsquare( the piece YET to be moved) then not valid
            else:                 
                return True           # if its the place its going to move to, its fine. THIS is why you lose your go if you dont enter a correct place, since it justs returns tru
        elif self._CurrentPlayer.SameAs(PieceInSquare.GetBelongsTo()):
            if StartSquare:  # if its the start square , it must belong to the player for check to be valid
                return True
            else:
                return False # returns false since you cant move onto another piece. NO STACKING G
        else:
            if StartSquare:
                return False # REVERSE HAPPENS IF THE square you pick does not belong to you.
            else:
                return True

    def __CheckIfGameOver(self):
        Player1HasMirza = False
        Player2HasMirza = False
        for S in self._Board:
            PieceInSquare = S.GetPieceInSquare()
            if PieceInSquare is not None:
                if (
                    S.ContainsKotla()
                    and PieceInSquare.GetTypeOfPiece() == "mirza"
                    and not PieceInSquare.GetBelongsTo().SameAs(S.GetBelongsTo())    # game is over if the other has stuck his mirza in ur kolta
                ):
                    return True
                elif (
                    PieceInSquare.GetTypeOfPiece() == "mirza"
                    and PieceInSquare.GetBelongsTo().SameAs(self._Players[0])
                ):
                    Player1HasMirza = True # if one of the squares on the board has a mirza that belongs to u then this variable is set to true
                elif (
                    PieceInSquare.GetTypeOfPiece() == "mirza"
                    and PieceInSquare.GetBelongsTo().SameAs(self._Players[1])
                ):
                    Player2HasMirza = True # same for player 2^^
        return not (Player1HasMirza and Player2HasMirza)  # if both mirza is alive, the game not over, otherwise the game is over

    def __GetSquareReference(self, Description):   # sets up the input question for the user
        SelectedSquare = int(
            input(
                "Enter the square "
                + Description
                + " (row number followed by column number): "
            )
        )
        return SelectedSquare

    def __UseMoveOptionOffer(self):
        ReplaceChoice = int(
            input("Choose the move option from your queue to replace (1 to 5): ")
        )
        self._CurrentPlayer.UpdateMoveOptionQueueWithOffer(     # Player class method used 
            ReplaceChoice - 1,
            self.__CreateMoveOption( # gets the name of the move option to replace
                self._MoveOptionOffer[self._MoveOptionOfferPosition],    
                self._CurrentPlayer.GetDirection(),
            ),
        )
        self._CurrentPlayer.ChangeScore(-(10 - (ReplaceChoice * 2)))      # score changes the further away you pick. If you pick the 5th option you lose 0 points
        self._MoveOptionOfferPosition = random.randint(0, 4) # the next offer is randomly generated

    def __GetPointsForOccupancyByPlayer(self, CurrentPlayer):
        ScoreAdjustment = 0
        for S in self._Board:
            ScoreAdjustment += S.GetPointsForOccupancy(CurrentPlayer) # loops through each square within the board list, remember S is a square object
        return ScoreAdjustment

    def __UpdatePlayerScore(self, PointsForPieceCapture):
        self._CurrentPlayer.ChangeScore(
            self.__GetPointsForOccupancyByPlayer(self._CurrentPlayer)     # gets p
            + PointsForPieceCapture
        )

    def __CalculatePieceCapturePoints(self, FinishSquareReference):
        if (
            self._Board[
                self.__GetIndexOfSquare(FinishSquareReference)
            ].GetPieceInSquare()
            is not None
        ):
            return (
                self._Board[self.__GetIndexOfSquare(FinishSquareReference)]    # if there is a piece that it has landed on, it will use the square class and the values for capture whitch are declared in the createpieces() function
                .GetPieceInSquare()
                .GetPointsIfCaptured()
            )
        return 0       # if there is no piece that it has landed on it returns 0

    def PlayGame(self):
        GameOver = False
        while not GameOver:
            self.__DisplayState()  # displays scores, move option, option queue, name
            SquareIsValid = False
            Choice = 0
            while Choice < 1 or Choice > 3:  # choice must be between 1 and 3
                Choice = int(
                    input(
                        "Choose move option to use from queue (1 to 3) or 9 to take the offer: "
                    )
                )
                if Choice == 9:
                    self.__UseMoveOptionOffer() # functionality for using the move option
                    self.__DisplayState()
            while not SquareIsValid:
                StartSquareReference = self.__GetSquareReference(
                    "containing the piece to move"
                )
                SquareIsValid = self.__CheckSquareIsValid(
                    StartSquareReference, True
                )  # this checks if the user has entered a valid position on board. enters the users input and true as parameters

            SquareIsValid = False
            while not SquareIsValid:
                FinishSquareReference = self.__GetSquareReference(
                    "to move to"
                )  # checks if the position the user wants to MOVE to is valid
                SquareIsValid = self.__CheckSquareIsValid(FinishSquareReference, False)   # set to false since this is not the start square, rather the end square
            MoveLegal = self._CurrentPlayer.CheckPlayerMove(
                Choice, StartSquareReference, FinishSquareReference     # checks if the move is a legal one
            )
            if MoveLegal:
                PointsForPieceCapture = self.__CalculatePieceCapturePoints(        # calculates capture points
                    FinishSquareReference
                )
                self._CurrentPlayer.ChangeScore(-(Choice + (2 * (Choice - 1))))  # loss of points for move goes 1, 3, 9 respective on choice made by user from 1-3
                self._CurrentPlayer.UpdateQueueAfterMove(Choice) # moves the move to the back of __Queue
                self.__UpdateBoard(StartSquareReference, FinishSquareReference) # changes the positions of the pieces 
                self.__UpdatePlayerScore(PointsForPieceCapture) # adds points for occupancy plus the points for capture using the variable assigned 4 lines above ^^
                print("New score: " + str(self._CurrentPlayer.GetScore()) + "\n") # prints the new score out to the user
            if self._CurrentPlayer.SameAs(self._Players[0]):
                self._CurrentPlayer = self._Players[1]    # changes the current player to 1 if its 2 and vice versa
            else:
                self._CurrentPlayer = self._Players[0]
            GameOver = self.__CheckIfGameOver() # if the game us over, the loop will end, otherwise it will continue
        self.__DisplayState() # displays the usual shit, explained above
        self.__DisplayFinalResult() # tells the user who wone the game, DONE!!

    def __UpdateBoard(self, StartSquareReference, FinishSquareReference):
        self._Board[self.__GetIndexOfSquare(FinishSquareReference)].SetPiece(
            self._Board[self.__GetIndexOfSquare(StartSquareReference)].RemovePiece()   # sets the position of the new piece into a square using the board queue, removes the piece from its former position
        )

    def __DisplayFinalResult(self): # self explanatory icl
        if self._Players[0].GetScore() == self._Players[1].GetScore():
            print("Draw!")
        elif self._Players[0].GetScore() > self._Players[1].GetScore():
            print(self._Players[0].GetName() + " is the winner!")
        else:
            print(self._Players[1].GetName() + " is the winner!")

    def __CreateBoard(self):
        for Row in range(1, self._NoOfRows + 1):
            for Column in range(1, self._NoOfColumns + 1):
                if (
                    Row == 1 and Column == self._NoOfColumns // 2
                ):  # inputs the kolta if the column is the number of colomns divided by 2. integer division
                    S = Kotla(self._Players[0], "K")
                elif Row == self._NoOfRows and Column == self._NoOfColumns // 2 + 1:
                    S = Kotla(self._Players[1], "k")
                else:
                    S = Square()  # composition with Square class
                self._Board.append(
                    S
                )  # instance of the square class created in board list

    def __CreatePieces(
        self, NoOfPieces
    ):  # private function to create the peices, takes in the parameter used in the constructor for dastan
        for Count in range(1, NoOfPieces + 1):
            CurrentPiece = Piece(
                "piece",
                self._Players[0],
                1,
                "!",  # player 1 has "!" as their pieces, sets the points if captured to 1. Type of piece is set to "piece"
            )  # aggregation to players class as it takes the players object as argument
            self._Board[
                self.__GetIndexOfSquare(
                    2 * 10 + Count + 1
                )  # converts the index into a  row and column input
            ].SetPiece(  # using the square class to set piece. (each element in the _Board list is an object of the square class)
                CurrentPiece
            )
        CurrentPiece = Piece(
            "mirza", self._Players[0], 5, "1"
        )  # setting the mirza for player 1 as a "1", sets points for capture to 5
        self._Board[self.__GetIndexOfSquare(10 + self._NoOfColumns // 2)].SetPiece(
            CurrentPiece  # looks for the kolta square for player 1 and inserts the mirza here.
        )
        for Count in range(1, NoOfPieces + 1):  # basically repeats for player 2
            CurrentPiece = Piece("piece", self._Players[1], 1, '"')
            self._Board[
                self.__GetIndexOfSquare((self._NoOfRows - 1) * 10 + Count + 1)
            ].SetPiece(CurrentPiece)
        CurrentPiece = Piece("mirza", self._Players[1], 5, "2")
        self._Board[
            self.__GetIndexOfSquare(self._NoOfRows * 10 + (self._NoOfColumns // 2 + 1))
        ].SetPiece(CurrentPiece)

    def __CreateMoveOptionOffer(self):
        self._MoveOptionOffer.append("jazair")
        self._MoveOptionOffer.append("chowkidar")
        self._MoveOptionOffer.append("cuirassier")
        self._MoveOptionOffer.append("ryott")
        self._MoveOptionOffer.append("faujdar")

    def __CreateRyottMoveOption(self, Direction):
        NewMoveOption = MoveOption("ryott")
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)     # we are appending to the possible move list, within the move option class
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateFaujdarMoveOption(self, Direction):
        NewMoveOption = MoveOption("faujdar")
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateJazairMoveOption(self, Direction):
        NewMoveOption = MoveOption("jazair")
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateCuirassierMoveOption(self, Direction):
        NewMoveOption = MoveOption("cuirassier")
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateChowkidarMoveOption(self, Direction):
        NewMoveOption = MoveOption("chowkidar")
        NewMove = Move(1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateMoveOption(self, Name, Direction):
        if Name == "chowkidar":
            return self.__CreateChowkidarMoveOption(Direction)
        elif Name == "ryott":
            return self.__CreateRyottMoveOption(Direction)
        elif Name == "faujdar":
            return self.__CreateFaujdarMoveOption(Direction)
        elif Name == "jazair":
            return self.__CreateJazairMoveOption(Direction)
        else:
            return self.__CreateCuirassierMoveOption(Direction)

    def __CreateMoveOptions(self):
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", 1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", -1))


class Piece:
    def __init__(self, T, B, P, S):
        self._TypeOfPiece = T
        self._BelongsTo = B
        self._PointsIfCaptured = P
        self._Symbol = S

    def GetSymbol(self):
        return self._Symbol

    def GetTypeOfPiece(self):
        return self._TypeOfPiece

    def GetBelongsTo(self):
        return self._BelongsTo

    def GetPointsIfCaptured(self):
        return self._PointsIfCaptured


class Square:
    def __init__(self):
        self._PieceInSquare = None
        self._BelongsTo = None
        self._Symbol = " "

    def SetPiece(self, P):
        self._PieceInSquare = P  # aggregation using parameter p. Setter for protected attribute piece in square

    def RemovePiece(self):
        PieceToReturn = self._PieceInSquare # makes a temporary copy of the piece in square attribute to piece to return, then sets it to null and returns it
        self._PieceInSquare = None
        return PieceToReturn

    def GetPieceInSquare(self):
        return self._PieceInSquare

    def GetSymbol(self):
        return self._Symbol

    def GetPointsForOccupancy(self, CurrentPlayer):
        return 0

    def GetBelongsTo(self):
        return self._BelongsTo

    def ContainsKotla(self):
        if self._Symbol == "K" or self._Symbol == "k":
            return True
        else:
            return False


class Kotla(Square):
    def __init__(self, P, S):
        super(
            Kotla, self
        ).__init__()  # inherits methods and attributesfrom the square class
        self._BelongsTo = P
        self._Symbol = S

    def GetPointsForOccupancy(
        self, CurrentPlayer
    ):  # overrides getpointsforoccupancy method
        if self._PieceInSquare is None:
            return 0
        elif self._BelongsTo.SameAs(CurrentPlayer):
            if CurrentPlayer.SameAs(
                self._PieceInSquare.GetBelongsTo()
            ) and (  # checks if the piece belongs to the player
                self._PieceInSquare.GetTypeOfPiece() == "piece"
                or self._PieceInSquare.GetTypeOfPiece()
                == "mirza"  # can either be a mirza or the players piece to obtain points. if it is ur kolta square u get 5 points
            ):
                return 5
            else:
                return 0
        else:
            if CurrentPlayer.SameAs(
                self._PieceInSquare.GetBelongsTo()
            ) and (  # if you occuypy ur opponenets kolta square with mirza or any or ur playing piece s u get one point
                self._PieceInSquare.GetTypeOfPiece() == "piece"
                or self._PieceInSquare.GetTypeOfPiece() == "mirza"
            ):
                return 1
            else:
                return 0


class MoveOption:
    def __init__(self, N):
        self._Name = N
        self._PossibleMoves = []

    def AddToPossibleMoves(self, M):
        self._PossibleMoves.append(M)

    def GetName(self):
        return self._Name

    def CheckIfThereIsAMoveToSquare(self, StartSquareReference, FinishSquareReference):
        StartRow = (
            StartSquareReference // 10
        )  # rows are integer divided by 10 to calculate
        StartColumn = StartSquareReference % 10  # columns are modded by 10 to calculate
        FinishRow = FinishSquareReference // 10
        FinishColumn = FinishSquareReference % 10
        for M in self._PossibleMoves:    # goes through each possible move, if the row and column changes match up to the finish row and finish column it is fine
            if (
                StartRow + M.GetRowChange() == FinishRow
                and StartColumn + M.GetColumnChange() == FinishColumn
            ):
                return True
        return False


class Move:
    def __init__(self, R, C):
        self._RowChange = R
        self._ColumnChange = C

    def GetRowChange(self):
        return self._RowChange

    def GetColumnChange(self):
        return self._ColumnChange


class MoveOptionQueue:
    def __init__(self):
        self.__Queue = []

    def GetQueueAsString(self):
        QueueAsString = ""
        Count = 1
        for M in self.__Queue:
            QueueAsString += str(Count) + ". " + M.GetName() + "   "
            Count += 1
        return QueueAsString

    def Add(self, NewMoveOption):
        self.__Queue.append(NewMoveOption)

    def Replace(self, Position, NewMoveOption):
        self.__Queue[Position] = NewMoveOption # replaces an item within an array with another

    def MoveItemToBack(self, Position):
        Temp = self.__Queue[Position]
        self.__Queue.pop(Position)     # uses pop and append to move the item to the back
        self.__Queue.append(Temp)

    def GetMoveOptionInPosition(self, Pos):
        return self.__Queue[Pos]


class Player:
    def __init__(
        self, N, D
    ):  # direction of Player 1 is 1 and direction if Player 2 is -1
        self.__Score = 100
        self.__Name = N
        self.__Direction = D
        self.__Queue = (
            MoveOptionQueue()
        )  # queue object is instantiated from move option queueu

    def SameAs(self, APlayer):
        if APlayer is None:
            return False
        elif APlayer.GetName() == self.__Name:
            return True
        else:
            return False

    def GetPlayerStateAsString(self):
        return (
            self.__Name
            + "\n"
            + "Score: "
            + str(self.__Score)
            + "\n"
            + "Move option queue: "
            + self.__Queue.GetQueueAsString()
            + "\n"
        )

    def AddToMoveOptionQueue(self, NewMoveOption):
        self.__Queue.Add(NewMoveOption)

    def UpdateQueueAfterMove(
        self, Position
    ):  # using moveoptionqueue methods using __queue object
        self.__Queue.MoveItemToBack(Position - 1)

    def UpdateMoveOptionQueueWithOffer(self, Position, NewMoveOption):
        self.__Queue.Replace(Position, NewMoveOption)

    def GetScore(self):
        return self.__Score

    def GetName(self):
        return self.__Name

    def GetDirection(self):
        return self.__Direction

    def ChangeScore(self, Amount):    # simply adds the amount to the pricate attribute score which is in player class.
        self.__Score += Amount

    def CheckPlayerMove(self, Pos, StartSquareReference, FinishSquareReference):
        Temp = self.__Queue.GetMoveOptionInPosition(Pos - 1)  # gets the move option from the position they chose
        return Temp.CheckIfThereIsAMoveToSquare( #uses move option class to check if there is a move to square
            StartSquareReference, FinishSquareReference
        )


def Main():
    ThisGame = Dastan(6, 6, 4)
    ThisGame.PlayGame()
    print("Goodbye!")
    input()


if __name__ == "__main__":
    Main()
