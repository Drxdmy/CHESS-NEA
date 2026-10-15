from fontTools.ttLib import TTFont

font = TTFont("ChessText.ttf")

pos = [
    "r","n","b","q","k","b","n","r",
    "p","p","p","p","p","p","p","p",
    " "," "," "," "," "," "," "," ",
    " "," "," "," "," "," "," "," ",
    " "," "," "," "," "," "," "," ",
    " "," "," "," "," "," "," "," ",
    "P","P","P","P","P","P","P","P",
    "R","N","B","Q","K","B","N","R"]

knightmoves = [(-2, -1),(-2, 1),(-1, -2),(-1, 2),(1, -2),(1, 2),(2, -1),(2, 1)]
wpawnmoves = [(-1, 0), (-1, -1), (-1, 1)]
wpawnattacks = [(-1, -1), (-1, 1)]
bpawnattacks = [(1, -1), (1, 1)]
bpawnmoves = [(1, 0), (1, -1), (1, 1)]
kingmoves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
queenmoves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

cords = ["a8","b8","c8","d8","e8","f8","g8","h8","a7","b7","c7","d7","e7","f7","g7","h7","a6","b6","c6","d6","e6","f6","g6","h6","a5","b5","c5","d5","e5","f5","g5","h5","a4","b4","c4","d4","e4","f4","g4","h4","a3","b3","c3","d3","e3","f3","g3","h3","a2","b2","c2","d2","e2","f2","g2","h2","a1","b1","c1","d1","e1","f1","g1","h1"]

def legalmove(index, moves):
    row = index // 8
    col = index % 8

    legalmoves = []

    for dr, dc in moves:
        newrow = row + dr
        newcol = col + dc

        if 0 <= newrow < 8 and 0 <= newcol < 8:
            destination = newrow * 8 + newcol
            legalmoves.append(destination)

    return legalmoves


def gameboard(pos):

    board =f"""
      a b c d e f g h
    8 {pos[0]} {pos[1]} {pos[2]} {pos[3]} {pos[4]} {pos[5]} {pos[6]} {pos[7]}
    7 {pos[8]} {pos[9]} {pos[10]} {pos[11]} {pos[12]} {pos[13]} {pos[14]} {pos[15]}
    6 {pos[16]} {pos[17]} {pos[18]} {pos[19]} {pos[20]} {pos[21]} {pos[22]} {pos[23]}
    5 {pos[24]} {pos[25]} {pos[26]} {pos[27]} {pos[28]} {pos[29]} {pos[30]} {pos[31]}
    4 {pos[32]} {pos[33]} {pos[34]} {pos[35]} {pos[36]} {pos[37]} {pos[38]} {pos[39]}
    3 {pos[40]} {pos[41]} {pos[42]} {pos[43]} {pos[44]} {pos[45]} {pos[46]} {pos[47]}
    2 {pos[48]} {pos[49]} {pos[50]} {pos[51]} {pos[52]} {pos[53]} {pos[54]} {pos[55]}
    1 {pos[56]} {pos[57]} {pos[58]} {pos[59]} {pos[60]} {pos[61]} {pos[62]} {pos[63]}
    """
    return board


#checkmate next. code needs to recognise that the king has no legal moves left and no way to block. 
#thinking of doing something like checking kings legal moves
#also gotta code two kings distance from eachother.

def checkmate(pos, colour):
    if colour == "black":
        kingindex = pos.index("k")
        pieces = ["p", "r", "n", "b", "q", "k"]
    if colour == "white":
        kingindex = pos.index("K")
        pieces = ["P", "R", "N", "B", "Q", "K"]
    if incheck(pos, colour):
        for index in range(64):
            if pos[index] in pieces:
                piece = pos[index]
                if piece == "N" or piece == "n":
                    indexidentify = index
                    possiblemoves = legalmove(index, knightmoves)
                    for indexmake in possiblemoves:
                        takenpiece = pos[indexmake]
                        
                        if takenpiece in pieces:
                            continue
                        
                        pos[indexmake] = piece
                        pos[indexidentify] = " "
                        
                        stillincheck = incheck(pos, colour)
                        
                        pos[indexidentify] = piece
                        pos[indexmake] = takenpiece
                        
                        if not stillincheck:
                            return False
                if piece == "P" or piece == "p":
                    indexidentify = index
                    if colour == "black":
                        possiblemoves = legalmove(index, bpawnmoves)
                    if colour == "white":
                        possiblemoves = legalmove(index, wpawnmoves)
                    for indexmake in possiblemoves:
                        takenpiece = pos[indexmake]

                        if takenpiece in pieces:
                            continue

                        pos[indexmake] = piece
                        pos[indexidentify] = " "

                        stillincheck
                            
                        
                        

def incheck(pos, colour):
    if colour == "black":
        kingindex = pos.index("k")
        enemy = ["P", "R", "N", "B", "Q"]
    if colour == "white":
        kingindex = pos.index("K")
        enemy = ["p", "r", "n", "b", "q"]
        
    adjacent = legalmove(kingindex, kingmoves)
    
    for square in adjacent:
        if pos[square] in enemy:
            piece = pos[square]
            
            if piece == "Q" or piece == "q":
                return True
            if piece == "R" or piece == "r":
                if abs(square - kingindex) == 1 or abs(square - kingindex) == 8:
                    return True
            if piece == "B" or piece == "b":
                if abs(square - kingindex) == 7 or abs(square - kingindex) == 9:
                    return True
        
    for index in range(64):
        if pos[index] in enemy:
            piece = pos[index]
            if piece == "N" or piece == "n":
                attack = legalmove(index, knightmoves)
                if kingindex in attack:
                    return True
        
            elif piece == "P":
                attack = legalmove(index, wpawnattacks)
                if kingindex in attack:
                    return True
                    
            elif piece == "p":
                attack = legalmove(index, bpawnattacks)
                if kingindex in attack:
                    return True
            
            elif piece == "R" or piece == "r":
                rookindex = index
                rrow = rookindex // 8
                rcol = rookindex % 8
                krow = kingindex // 8
                kcol = kingindex % 8
                
                if rrow == krow:
                    if rcol < kcol:
                        rdistance = kcol - rcol
                    if rcol > kcol:
                        rdistance = rcol - kcol
                    
                    totrange = kingindex - rookindex
                    rangepermove = totrange // rdistance
           
                    rookindex = rookindex + rangepermove
                    for i in range(rdistance-1):
                        if pos[rookindex] == " " and rookindex != kingindex:
                            rookindex = rookindex + rangepermove
                        elif pos[rookindex] != " " and rookindex != kingindex:
                            break
                        if rookindex == kingindex:
                            return True
                            break
                        
                if rcol == kcol:
                    if rrow < krow:
                        cdistance = krow - rrow
                    if rrow> krow:
                        cdistance = rrow - krow
                    
                    totrange = kingindex - rookindex
                    rangepermove = totrange // cdistance 
                    
                    rookindex = rookindex + rangepermove
                    for i in range(cdistance-1):
                        if pos[rookindex] == " " and rookindex != kingindex:
                            rookindex = rookindex + rangepermove
                        elif pos[rookindex] != " " and rookindex != kingindex:
                            break
                        if rookindex == kingindex:
                            return True
                            break
                        
            elif piece == "B" or piece == "b":
                bishopindex = index
                colbishop = bishopindex // 8
                colking = kingindex // 8
                if colbishop > colking:
                    coldistance = colbishop - colking
                elif colbishop < colking:
                    coldistance = colking - colbishop
           
                rowbishop = bishopindex % 8
                rowking = kingindex % 8
                if rowbishop > rowking:
                    rowdistance = rowbishop - rowking
                elif rowbishop < rowking:
                    rowdistance = rowking - rowbishop

                if rowdistance == coldistance:
                    totrange = kingindex - bishopindex
                    rangepermove = totrange // rowdistance
                
                    bishopindex = bishopindex + rangepermove
                    for i in range(rowdistance-1):
                        if pos[bishopindex] == " " and bishopindex != kingindex:
                            bishopindex = bishopindex + rangepermove
                        elif pos[bishopindex] != " " and bishopindex != kingindex:
                            break
                        if bishopindex == kingindex:
                            return True
                            break 
            
            elif piece == "Q" or piece == "q":
                queenindex = index
                Qrow = queenindex // 8
                Qcol = queenindex % 8
                krow = kingindex // 8
                kcol = kingindex % 8
                
                if Qrow == krow:
                    if Qcol < kcol:
                        rdistance = kcol - Qcol
                    if Qcol > kcol:
                        rdistance = Qcol - kcol
                    
                    totrange = kingindex - queenindex
                    rangepermove = totrange // rdistance
           
                    queenindex = queenindex + rangepermove
                    for i in range(rdistance-1):
                        if pos[queenindex] == " " and queenindex != kingindex:
                            queenindex = queenindex + rangepermove
                        elif pos[queenindex] != " " and queenindex != kingindex:
                            break
                        if queenindex == kingindex:
                            return True
                            break
                        
                elif Qcol == kcol:
                    if Qrow < krow:
                        cdistance = krow - Qrow
                    if Qrow> krow:
                        cdistance = Qrow - krow
                    
                    totrange = kingindex - queenindex
                    rangepermove = totrange // cdistance 
                    
                    queenindex = queenindex + rangepermove
                    for i in range(cdistance-1):
                        if pos[queenindex] == " " and queenindex != kingindex:
                            queenindex = queenindex + rangepermove
                        elif pos[queenindex] != " " and queenindex != kingindex:
                            break
                        if queenindex == kingindex:
                            return True
                            break
                        
                else:
                    if Qrow > krow:
                        coldistance = Qrow - krow
                    if Qrow < krow:
                        coldistance = krow - Qrow
           
                    if Qcol > kcol:
                        rowdistance = Qcol - kcol
                    elif Qcol < kcol:
                        rowdistance = kcol - Qcol

                    if rowdistance == coldistance:
                        totrange = kingindex - queenindex
                        rangepermove = totrange // rowdistance
                
                        queenindex = queenindex + rangepermove
                        for i in range(rowdistance-1):
                            if pos[queenindex] == " " and queenindex != kingindex:
                                queenindex = queenindex + rangepermove
                            elif pos[queenindex] != " " and queenindex != kingindex:
                                break
                            if queenindex == kingindex:
                                return True
                                break 
                
def wmove(gameboard, pos, cords):
    whitep = ["P", "R", "N", "B", "K", "Q"]
    identifymove = input("White to move. Enter the co ordinates of the piece you would like to move: ").lower()
    while identifymove not in cords:
        identifymove = input("Move not valid. White to move. Enter the co ordinates of the piece you would like to move: ").lower()
    indexidentify = cords.index(identifymove)
    piece = pos[indexidentify]
    makemove = input("What space would you like to move it to?: ").lower()
    while makemove not in cords:
        makemove = input("Input not on the board! What space would you like to move it to?: ").lower()
    indexmake = cords.index(makemove)
    takenpiece = pos[indexmake]
       

    if pos[indexidentify] not in whitep:
        print("You did not select your own piece!")
        wmove(gameboard, pos, cords)
        
    
   
    if piece == "P":
        legal = legalmove(indexidentify, wpawnmoves)
        if indexidentify not in [55, 54, 53, 52, 51, 50, 49, 48]:
            if indexmake not in [indexidentify - 8, indexidentify - 7, indexidentify - 9] :
                print("Cannot move there!")
                return wmove(gameboard, pos, cords)

               
            elif indexmake in [indexidentify - 8]:
                if pos[indexmake] == " ":
                    pos[indexmake] = pos[indexidentify]
                    pos[indexidentify] = " "
                else:
                    print("Cannot move there!")
                    wmove(gameboard, pos, cords)

            elif indexmake in [indexidentify - 9, indexidentify - 7]:
                if indexmake in legal:
                    if takenpiece != " " and takenpiece not in whitep:
                        print(f"{takenpiece} has been taken! ")
                        pos[indexmake] = pos[indexidentify]
                        pos[indexidentify] = " "
                    else:
                        print("Cannot move there!")
                        wmove(gameboard, pos, cords)
                else:
                    print("Cannot move there!")
                    wmove(gameboard, pos, cords)
                   
        else:
            if indexmake in [indexidentify - 8]:
                if pos[indexmake] == " ":
                    pos[indexmake] = pos[indexidentify]
                    pos[indexidentify] = " "
                else:
                    print("Cannot move there!")
                    wmove(gameboard, pos, cords)

            elif indexmake in [indexidentify - 9, indexidentify - 7]:
                if indexmake in legal:
                    if takenpiece != " " and takenpiece not in whitep:
                        print(f"{takenpiece} has been taken! ")
                        pos[indexmake] = pos[indexidentify]
                        pos[indexidentify] = " "
                    else:
                        print("Cannot move there!")
                        wmove(gameboard, pos, cords)
                else:
                    print("Cannot move there!")
                    wmove(gameboard, pos, cords)
           
            elif indexmake in [indexidentify - 8, indexidentify - 16]:
                if indexmake == indexidentify - 8:
                    if pos[indexmake] != " ":
                        print("Cannot move there!")
                        wmove(gameboard, pos, cords)
                    else:
                        pos[indexmake] = pos[indexidentify]
                        pos[indexidentify] = " "
                elif indexmake == indexidentify - 16:
                    if pos[indexmake] != " " or pos[(indexmake + 8)] != " ":
                        print("Cannot move there!")
                        wmove(gameboard, pos, cords)
                    else:
                        pos[indexmake] = pos[indexidentify]
                        pos[indexidentify] = " "
            else:
                print("Cannot move there!")
                wmove(gameboard, pos, cords)
               
               
    if piece == "N":
        legal = legalmove(indexidentify, knightmoves)
        if indexmake not in legal:
            print("Cannot move there!")
            wmove(gameboard, pos, cords)

        elif takenpiece in whitep:
            print("Cannot move there!")
            wmove(gameboard, pos, cords)

        else:
            if takenpiece != " ":
                print(f"{takenpiece} has been taken!")
            pos[indexmake] = pos[indexidentify]
            pos[indexidentify] = " "
           
    if piece == "B":
        ogindexidentify = indexidentify
        colidentify = indexidentify // 8
        colmake = indexmake // 8
        if colidentify > colmake:
            coldistance = colidentify - colmake
        elif colidentify < colmake:
            coldistance = colmake - colidentify
           
        rowidentify = indexidentify % 8
        rowmake = indexmake % 8
        if rowidentify > rowmake:
            rowdistance = rowidentify - rowmake
        elif rowidentify < rowmake:
            rowdistance = rowmake - rowidentify

        if rowdistance == coldistance:
            totrange = indexmake - indexidentify
            rangepermove = totrange // rowdistance
           

            indexidentify = indexidentify + rangepermove
            for i in range(rowdistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    wmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in whitep:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                   
        else:
            print("Cannot move there!")
            wmove(gameboard, pos, cords)
               
                   
    if piece == "R":
        ogindexidentify = indexidentify
        colidentify = indexidentify // 8
        colmake = indexmake // 8
        rowidentify = indexidentify % 8
        rowmake = indexmake % 8
       
        if colidentify == colmake:
            if rowidentify > rowmake:
                rowdistance = rowidentify - rowmake
            elif rowmake > rowidentify:
                rowdistance = rowmake - rowidentify
           
            totrange = indexmake - indexidentify
            rangepermove = totrange // rowdistance
           
            indexidentify = indexidentify + rangepermove
            for i in range(rowdistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    wmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in whitep:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
       
       
        if rowidentify == rowmake:
            if colidentify > colmake:
                coldistance = colidentify - colmake
            elif colmake > colidentify:
                coldistance = colmake - colidentify
           
            totrange = indexmake - indexidentify
            rangepermove = totrange // coldistance
               
            indexidentify = indexidentify + rangepermove
            for i in range(coldistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    wmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in whitep:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "

       
    if piece == "K":
        legal = legalmove(indexidentify, kingmoves)
        if indexmake in legal:
            if pos[indexmake] != " " and indexmake not in whitep:
                print(f"{takenpiece} has been taken!")
                pos[indexmake] = pos[indexidentify]
                pos[indexidentify] = " "
            elif pos[indexmake] == " ":
                pos[indexmake] = pos[indexidentify]
                pos[indexidentify] = " "
        else:
            print("Cannot move there!")
            wmove(gameboard, pos, cords)
       
       
    if piece == "Q":
        legal = legalmove(indexidentify, queenmoves)
        ogindexidentify = indexidentify
        colidentify = indexidentify // 8
        colmake = indexmake // 8
        rowidentify = indexidentify % 8
        rowmake = indexmake % 8
        if colidentify == colmake:
            if rowidentify > rowmake:
                rowdistance = rowidentify - rowmake
            elif rowmake > rowidentify:
                rowdistance = rowmake - rowidentify
           
            totrange = indexmake - indexidentify
            rangepermove = totrange // rowdistance
           
            indexidentify = indexidentify + rangepermove
            for i in range(rowdistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    wmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in whitep:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
       
       
        elif rowidentify == rowmake:
            if colidentify > colmake:
                coldistance = colidentify - colmake
            elif colmake > colidentify:
                coldistance = colmake - colidentify
           
            totrange = indexmake - indexidentify
            rangepermove = totrange // coldistance
               
            indexidentify = indexidentify + rangepermove
            for i in range(coldistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    wmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in whitep:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "

        else:
            if colidentify > colmake:
                coldistance = colidentify - colmake
            elif colidentify < colmake:
                coldistance = colmake - colidentify
           
            rowidentify = indexidentify % 8
            rowmake = indexmake % 8
            if rowidentify > rowmake:
                rowdistance = rowidentify - rowmake
            elif rowidentify < rowmake:
                rowdistance = rowmake - rowidentify

            if rowdistance == coldistance:
                totrange = indexmake - indexidentify
                rangepermove = totrange // rowdistance
           

                indexidentify = indexidentify + rangepermove
                for i in range(rowdistance-1):
                    if pos[indexidentify] == " " and indexidentify != indexmake:
                        indexidentify = indexidentify + rangepermove
                    elif pos[indexidentify] != " " and indexidentify != indexmake:
                        print("Cannot move there!")
                        wmove(gameboard, pos, cords)
           
                if indexidentify == indexmake:
                    if pos[indexmake] != " " and indexmake not in whitep:
                        print(f"{takenpiece} has been taken!")
                        pos[indexmake] = pos[ogindexidentify]
                        pos[ogindexidentify] = " "
                    elif pos[indexmake] == " ":
                        pos[indexmake] = pos[ogindexidentify]
                        pos[ogindexidentify] = " "
                   
            else:
                print("Cannot move there!")
                wmove(gameboard, pos, cords)
    
    if incheck(pos, "white"):
        print("Cant move there, you are still in check.")
        wmove(gameboard, pos, cords)

    if incheck(pos, "black"):
        print("\nblack in check.")
   
    print(gameboard(pos))
    bmove(gameboard, pos, cords)
   
   
def bmove(gameboard, pos, cords):
    blackp = ["p", "r", "n", "b", "k", "q"]
    
    identifymove = input("black to move. Enter the co ordinates of the piece you would like to move: ").lower()
    while identifymove not in cords:
        identifymove = input("black to move. Enter the co ordinates of the piece you would like to move: ").lower()
    indexidentify = cords.index(identifymove)
    piece = pos[indexidentify]
    makemove = input("What space would you like to move it to?: ").lower()
    while makemove not in cords:
        makemove = input("What space would you like to move it to?: ").lower()
    indexmake = cords.index(makemove)
    takenpiece = pos[indexmake]

    if pos[indexidentify] not in blackp:
        print("You did not select your own piece!")
        bmove(gameboard, pos, cords)
        
    

    if piece == "p":
        legal = legalmove(indexidentify, bpawnmoves)
        if indexidentify not in [8, 9, 10, 11, 12, 13, 14, 15]:
            if indexmake not in [indexidentify + 8, indexidentify + 7, indexidentify + 9] :
                print("Cannot move there!")
                bmove(gameboard, pos, cords)
           
            elif indexmake in [indexidentify + 8]:
                if pos[indexmake] == " ":
                    pos[indexmake] = pos[indexidentify]
                    pos[indexidentify] = " "
                else:
                    print("Cannot move there!")
                    bmove(gameboard, pos, cords)

            elif indexmake in [indexidentify + 9, indexidentify + 7]:
                if indexmake in legal:
                    if takenpiece != " " and takenpiece not in blackp:
                        print(f"{takenpiece} has been taken! ")
                        pos[indexmake] = pos[indexidentify]
                        pos[indexidentify] = " "
                    else:
                        print("Cannot move there!")
                        bmove(gameboard, pos, cords)
                else:
                    print("Cannot move there!")
                    bmove(gameboard, pos, cords)
       
        else:
            if indexmake in [indexidentify + 8]:
                if pos[indexmake] == " ":
                    pos[indexmake] = pos[indexidentify]
                    pos[indexidentify] = " "
                else:
                    print("Cannot move there!")
                    bmove(gameboard, pos, cords)

            elif indexmake in [indexidentify + 9, indexidentify + 7]:
                if indexmake in legal:
                    if takenpiece != " " and takenpiece not in blackp:
                        print(f"{takenpiece} has been taken! ")
                        pos[indexmake] = pos[indexidentify]
                        pos[indexidentify] = " "
                    else:
                        print("Cannot move there!")
                        bmove(gameboard, pos, cords)
                else:
                    print("Cannot move there!")
                    return bmove(gameboard, pos, cords)
           
            elif indexmake in [indexidentify + 8, indexidentify + 16]:
                if indexmake == indexidentify + 8:
                    if pos[indexmake] != " ":
                        print("Cannot move there!")
                        return bmove(gameboard, pos, cords)
                    else:
                        pos[indexmake] = pos[indexidentify]
                        pos[indexidentify] = " "
                elif indexmake == indexidentify + 16:
                    if pos[indexmake] != " " or pos[(indexmake - 8)] != " ":
                        print("Cannot move there!")
                        return bmove(gameboard, pos, cords)
                    else:
                        pos[indexmake] = pos[indexidentify]
                        pos[indexidentify] = " "
            else:
                print("Cannot move there!")
                bmove(gameboard, pos, cords)
           
    if piece == "n":

        legal = legalmove(indexidentify, knightmoves)

        if indexmake not in legal:
            print("Cannot move there!")
            bmove(gameboard, pos, cords)

        elif takenpiece in blackp:
            print("Cannot move there!")
            bmove(gameboard, pos, cords)
        else:
            if takenpiece != " ":
                print(f"{takenpiece} has been taken!")

            pos[indexmake] = pos[indexidentify]
            pos[indexidentify] = " "
           
    if piece == "b":
        ogindexidentify = indexidentify
        colidentify = indexidentify // 8
        colmake = indexmake // 8
        if colidentify > colmake:
            coldistance = colidentify - colmake
        elif colidentify < colmake:
            coldistance = colmake - colidentify
           
        rowidentify = indexidentify % 8
        rowmake = indexmake % 8
        if rowidentify > rowmake:
            rowdistance = rowidentify - rowmake
        elif rowidentify < rowmake:
            rowdistance = rowmake - rowidentify

        if rowdistance == coldistance:
            totrange = indexmake - indexidentify
            rangepermove = totrange // rowdistance
           
            indexidentify = indexidentify + rangepermove
            for i in range(rowdistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    bmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in blackp:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                   
        else:
            print("Cannot move there!")
            bmove(gameboard, pos, cords)
       
       
    if piece == "r":
        ogindexidentify = indexidentify
        colidentify = indexidentify // 8
        colmake = indexmake // 8
        rowidentify = indexidentify % 8
        rowmake = indexmake % 8
       
        if colidentify == colmake:
            if rowidentify > rowmake:
                rowdistance = rowidentify - rowmake
            elif rowmake > rowidentify:
                rowdistance = rowmake - rowidentify
           
            totrange = indexmake - indexidentify
            rangepermove = totrange // rowdistance
           
            indexidentify = indexidentify + rangepermove
            for i in range(rowdistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    bmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in blackp:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
       
       
        if rowidentify == rowmake:
            if colidentify > colmake:
                coldistance = colidentify - colmake
            elif colmake > colidentify:
                coldistance = colmake - colidentify
           
            totrange = indexmake - indexidentify
            rangepermove = totrange // coldistance
               
            indexidentify = indexidentify + rangepermove
            for i in range(coldistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    bmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in blackp:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "

    if piece == "k":
        legal = legalmove(indexidentify, kingmoves)
        if indexmake in legal:
            if pos[indexmake] != " " and indexmake not in blackp:
                print(f"{takenpiece} has been taken!")
                pos[indexmake] = pos[indexidentify]
                pos[indexidentify] = " "
            elif pos[indexmake] == " ":
                pos[indexmake] = pos[indexidentify]
                pos[indexidentify] = " "
        else:
            print("Cannot move there!")
            bmove(gameboard, pos, cords)

    if piece == "q":
        legal = legalmove(indexidentify, queenmoves)
        ogindexidentify = indexidentify
        colidentify = indexidentify // 8
        colmake = indexmake // 8
        rowidentify = indexidentify % 8
        rowmake = indexmake % 8

        if colidentify == colmake:
            if rowidentify > rowmake:
                rowdistance = rowidentify - rowmake
            elif rowmake > rowidentify:
                rowdistance = rowmake - rowidentify
           
            totrange = indexmake - indexidentify
            rangepermove = totrange // rowdistance    
           
            indexidentify = indexidentify + rangepermove
            for i in range(rowdistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    bmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in blackp:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
       
       
        elif rowidentify == rowmake:
            if colidentify > colmake:
                coldistance = colidentify - colmake
            elif colmake > colidentify:
                coldistance = colmake - colidentify
           
            totrange = indexmake - indexidentify
            rangepermove = totrange // coldistance
               
            indexidentify = indexidentify + rangepermove
            for i in range(coldistance-1):
                if pos[indexidentify] == " " and indexidentify != indexmake:
                    indexidentify = indexidentify + rangepermove
                elif pos[indexidentify] != " " and indexidentify != indexmake:
                    print("Cannot move there!")
                    bmove(gameboard, pos, cords)
           
            if indexidentify == indexmake:
                if pos[indexmake] != " " and indexmake not in blackp:
                    print(f"{takenpiece} has been taken!")
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "
                elif pos[indexmake] == " ":
                    pos[indexmake] = pos[ogindexidentify]
                    pos[ogindexidentify] = " "

        else:
            if colidentify > colmake:
                coldistance = colidentify - colmake
            elif colidentify < colmake:
                coldistance = colmake - colidentify
           
            rowidentify = indexidentify % 8
            rowmake = indexmake % 8
            if rowidentify > rowmake:
                rowdistance = rowidentify - rowmake
            elif rowidentify < rowmake:
                rowdistance = rowmake - rowidentify

            if rowdistance == coldistance:
                totrange = indexmake - indexidentify
                rangepermove = totrange // rowdistance
           

                indexidentify = indexidentify + rangepermove
                for i in range(rowdistance-1):
                    if pos[indexidentify] == " " and indexidentify != indexmake:
                        indexidentify = indexidentify + rangepermove
                    elif pos[indexidentify] != " " and indexidentify != indexmake:
                        print("Cannot move there!")
                        bmove(gameboard, pos, cords)
           
                if indexidentify == indexmake:
                    if pos[indexmake] != " " and indexmake not in blackp:
                        print(f"{takenpiece} has been taken!")
                        pos[indexmake] = pos[ogindexidentify]
                        pos[ogindexidentify] = " "
                    elif pos[indexmake] == " ":
                        pos[indexmake] = pos[ogindexidentify]
                        pos[ogindexidentify] = " "
                   
            else:
                print("Cannot move there!")
                bmove(gameboard, pos, cords)
    
    
    if incheck(pos, "black"):
        print("Cant move there, you are still in check.")
        bmove(gameboard, pos, cords)
        
    if incheck(pos, "white"):
        print("\nWhite in check.")
           

    print(gameboard(pos))    
    wmove(gameboard, pos, cords)


print(gameboard(pos))
wmove(gameboard, pos, cords)
