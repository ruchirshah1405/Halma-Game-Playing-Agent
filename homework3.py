f = open("input.txt","r")
gamestatus = f.readline().rstrip("\n")
player = f.readline().rstrip("\n")
time_limit = f.readline().rstrip("\n")
white = {}
white['B'] = [(15,15),(14,15),(15,14),(13,15),(14,14),(15,13),(12,15),(13,14),(14,13),(15,12),(11,15),(12,14),(13,13),(14,12),(15,11),(11,14),(12,13),(13,12),(14,11)]
white['G'] = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]

black ={}
black['B'] = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
black['G'] = [(11, 14), (11, 15), (12, 13), (12, 14), (12, 15), (13, 12), (13, 13), (13, 14), (13, 15), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15)]
row = []
maxtrix = []
move_consider = []
for l in f.readlines():
    l = l.strip()
    for c in l:
        if c == "\n":
            break
        row.append(c)
    maxtrix.append(row)
    row =[]
f.close()


def baseCamp(board,color):
    processfirst = []
    final_check= []
    if color == 'W':
        lookupdict = white
        for i, j in white['B']:
            if board[i][j] == 'W':
                processfirst.append((i, j))
    else:
        lookupdict = black
        for i, j in black['B']:
            if board[i][j] == 'B':
                processfirst.append((i, j))

    if len(processfirst) > 0:
        if color == 'B':
            ngh = [(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (0, -1), (-1, 0), (-1, -1)]
        else:
            ngh = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        mini = 9999
        for r, c in processfirst:
            available = []
            for nr, nc in ngh:
                if len(board) > r + nr >= 0 and len(board[r]) > c + nc >= 0:
                    if color == 'W' and r+nr <= r and nc+c <= c and board[r + nr][c + nc] == '.':
                        available.append((r + nr, c + nc))
                    elif color == 'B' and r+nr >= r and c+nc >= c and board[r + nr][c + nc] == '.':
                        available.append((r + nr, c + nc))
            visited = {}
            queue = [(r, c)]
            while queue:
                startx, starty = queue.pop()
                visited[(startx, starty)] = 1
                for i, j in ngh:
                    midStart = startx + i
                    midEnd = starty + j
                    if 0 <= midStart <= 15 and 0 <= midEnd <= 15 and board[midStart][midEnd] != '.':
                        newStart = midStart + i
                        newEnd = midEnd + j
                        if 0 <= newStart <= 15 and 0 <= newEnd <= 15 and (newStart, newEnd) not in visited and \
                                board[newStart][newEnd] == '.':
                            if color == 'W' and newStart<= startx and newEnd<=starty:
                                available.append((newStart, newEnd))
                            elif color =='B' and newStart>=startx and newEnd>=starty:
                                available.append((newStart, newEnd))
                            queue.append((newStart, newEnd))

            if len(available) > 0:
                final_moves = []
                for end in available:
                    final_moves.append(((r, c), end))
                if color == 'B':
                    h1 = (15, 15)
                else:
                    h1 = (0, 0)
                for x, y in final_moves:
                    euclidan = ((h1[0] - y[0]) ** 2 + (h1[1] - y[1]) ** 2) ** 0.5
                    if euclidan < mini:
                        mini = euclidan
                        final_check.append((x, y))
    if len(final_check)>0:
        if color == 'B':
            h1 = (15, 15)
        else:
            h1 = (0, 0)
        mini = 99999
        for x, y in final_check:
            euclidan = ((h1[0] - y[0]) ** 2 + (h1[1] - y[1]) ** 2) ** 0.5
            if euclidan < mini:
                mini = euclidan
                destination = (x,y)
        return destination
    else:
        return []

def finalMove(move,color):
    if color == 'B':
        h1 = (15, 15)
    else:
        h1 = (0,0)
    mini = 99999
    for x, y in move:

        euclidan = ((h1[0] - y[0]) ** 2 + (h1[1] - y[1]) ** 2) ** 0.5
        if euclidan < mini:
            mini = euclidan
            destination = (x, y)
    return destination

def fromrecPossibleMoves(board,color):
    global white
    global black
    iteratelist = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == color:
                iteratelist.append((i, j))
    lookupdict1 = {}
    if color == 'W':
        lookupdict1 = white
        ngh = [(-1,-1), (-1,0), (0,-1), (-1,1), (1,-1), (0,1), (1,0), (1,1)]
        # ngh = [(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (0, -1), (1, 0), (-1, -1)]
    else:
        lookupdict1 = black
        ngh = [(1,1),(1,0),(0,1),(1,-1),(-1,1),(0,-1),(1,0),(-1,-1)]
    possible = []
    for r, c in iteratelist:
        flag = 0
        if (r, c) in lookupdict1['G']:
            flag = 1
        for nr, nc in ngh:
            if len(board) > r + nr >= 0 and len(board[r]) > c + nc >= 0:
                if flag == 1:
                    if (r + nr, nc + c) not in lookupdict1['G']:
                        continue
                if board[r + nr][c + nc] == '.':
                    possible.append(((r,c),(r+nr,c+nc)))
        visited = {}
        queue = [(r, c)]
        while queue:
            startx, starty = queue.pop()
            visited[(startx, starty)] = 1
            for i, j in ngh:
                midStart = startx + i
                midEnd = starty + j
                if 0 <= midStart <= 15 and 0 <= midEnd <= 15 and board[midStart][midEnd] != '.':
                    newStart = midStart + i
                    newEnd = midEnd + j
                    if flag == 1:
                        if (newStart, newEnd) not in lookupdict1['G']:
                            continue
                    if 0 <= newStart <= 15 and 0 <= newEnd <= 15 and (newStart, newEnd) not in visited and \
                            board[newStart][newEnd] == '.':
                        possible.append(((r,c),(newStart,newEnd)))
                        queue.append((newStart, newEnd))
    return possible
def evaluate(board,color):
    checklist = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == color:
                checklist.append((i, j))
    if color == "W":
        lookupdict = white
    else:
        lookupdict = black
    totalvacantpost = 0
    xsum = 0
    ysum = 0
    for x, y in lookupdict['G']:
        if board[x][y] != color:
            xsum += x
            ysum += y
            totalvacantpost += 1
    if totalvacantpost != 0 :
        h1 = (xsum/totalvacantpost,ysum/totalvacantpost)
        heuristicvalue = 0
        for x1, y1 in checklist:
            if(x1,y1) not in lookupdict['G']:
                euclidan = ((h1[0] - x1)**2 + (h1[1] - y1)**2)**0.5
                heuristicvalue += euclidan
        if heuristicvalue != 0:
            heuristicvalue = (1/heuristicvalue)
        else:
            heuristicvalue = 99999
    else:
        heuristicvalue = 99999
    return heuristicvalue

def minimax(depth, board, color, alpha, beta,globalcolor):
    global move_consider
    if depth == 2:
        score = evaluate(board,color)
        return score
    if color == globalcolor:
        best = -99999
        possible_moves = fromrecPossibleMoves(board,color)
        lookupdict1 = {}
        if color == "W":
            lookupdict1 = white
        else:
            lookupdict1 = black
        maxdistance = 0
        returnmoves = []
        if depth == 0:
            for start, land in possible_moves:
                if start not in lookupdict1['G'] and land in lookupdict1['G']:
                    if (abs(start[0]-land[0])+abs(start[1]-land[1]))>maxdistance:
                        maxdistance = abs(start[0]-land[0])+abs(start[1]-land[1])
                        returnmoves = [(start,land)]
            if len(returnmoves)>0:
                move_consider = returnmoves
                return best
        g_best = -99999
        for i in possible_moves:
            start = i[0]
            end = i[1]
            board[end[0]][end[1]] = board[start[0]][start[1]]
            board[start[0]][start[1]] = "."
            if globalcolor == 'W':
                val = minimax(depth + 1, board, 'B', alpha, beta,globalcolor)
            else:
                val = minimax(depth + 1, board, 'W', alpha, beta,globalcolor)
            board[start[0]][start[1]] = board[end[0]][end[1]]
            board[end[0]][end[1]] = "."
            best = max(best, val)
            alpha = max(alpha, best)
            if g_best < best and depth == 0:
                g_best = best
                move_consider = [i]
            if beta <= alpha:
                break
        return best
    else:
        best = 99999
        possible_moves = fromrecPossibleMoves(board, color)
        for i in possible_moves:
            start = i[0]
            end = i[1]
            board[end[0]][end[1]] = board[start[0]][start[1]]
            board[start[0]][start[1]] = "."
            val = minimax(depth + 1, board, globalcolor, alpha, beta,globalcolor)
            board[start[0]][start[1]] = board[end[0]][end[1]]
            board[end[0]][end[1]] = "."
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def findPath(board,moves):
    parent = {}
    visited = {}
    queue = [(moves[0][0],moves[0][1])]
    parent[(moves[0][0],moves[0][1])] = None
    visited[(moves[0][0],moves[0][1])] = 1
    path = []
    flag = 0
    ngh = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while queue:
        startx, starty = queue.pop()
        for i, j in ngh:
            midStart = startx + i
            midEnd = starty + j
            if 0 <= midStart <= 15 and 0 <= midEnd <= 15 and board[midStart][midEnd] != '.':
                newStart = midStart + i
                newEnd = midEnd + j
                if 0 <= newStart <= 15 and 0 <= newEnd <= 15 and (newStart, newEnd) not in visited and \
                        board[newStart][newEnd] == '.':
                    queue.append((newStart, newEnd))
                    visited[(newStart, newEnd)] = 1
                    parent[(newStart, newEnd)] = startx,starty
                    if (newStart,newEnd) == (moves[1][0],moves[1][1]):
                        flag = 1
                        break
    if flag == 1:
        nodes = parent[(moves[1][0],moves[1][1])]
        path.append((moves[1][0],moves[1][1]))
        while(nodes):
            path.append(nodes)
            nodes=parent[nodes]
        path.reverse()
    final_path = []
    for i in range(len(path)-1):
        final_path.append((path[i],path[i+1]))
    return final_path

file_write = ""
if gamestatus == 'SINGLE':
    move_first = baseCamp(maxtrix,player[0])
    if len(move_first) > 0:
        if 0<=abs(move_first[0][0]-move_first[1][0])<=1 and  0<=abs(move_first[0][1]-move_first[1][1])<=1:
            move_first = ((move_first[0][1], move_first[0][0]), (move_first[1][1], move_first[1][0]))
            file_write += "E "+str(move_first[0])[1:-1].replace(" ",'')+" "+str(move_first[1])[1:-1].replace(" ",'')
        else:
            path = findPath(maxtrix,move_first)
            for p in path:
                file_write+="J "+str(p[0][1])+","+str(p[0][0])+" "+str(p[1][1])+","+str(p[1][0])+"\n"

    else:
        all_moves = fromrecPossibleMoves(maxtrix,player[0])
        final_move = finalMove(all_moves,player[0])
        if 0<=abs(final_move[0][0]-final_move[1][0])<=1 and  0<=abs(final_move[0][1]-final_move[1][1])<=1:
            final_move = ((final_move[0][1], final_move[0][0]), (final_move[1][1], final_move[1][0]))
            file_write += "E "+str(final_move[0])[1:-1].replace(" ",'')+" "+str(final_move[1])[1:-1].replace(" ",'')
        else:
            path = findPath(maxtrix,final_move)
            for p in path:
                file_write += "J "+str(p[0][1])+","+str(p[0][0])+" "+str(p[1][1])+","+str(p[1][0])+"\n"

else:
    move_first = baseCamp(maxtrix, player[0])
    if len(move_first) > 0:
        if 0 <= abs(move_first[0][0] - move_first[1][0]) <= 1 and 0 <= abs(move_first[0][1] - move_first[1][1]) <= 1:
            move_first = ((move_first[0][1], move_first[0][0]), (move_first[1][1], move_first[1][0]))
            file_write += "E " + str(move_first[0])[1:-1].replace(" ", '') + " " + str(move_first[1])[1:-1].replace(" ", '')
        else:
            path = findPath(maxtrix, move_first)
            for p in path:
                file_write += "J " + str(p[0][1]) + "," + str(p[0][0]) + " " + str(p[1][1]) + "," + str(p[1][0]) + "\n"

    else:
        move = minimax(0, maxtrix, player[0], -99999, 99999, player[0])
        final_move = move_consider
        # print(final_move)
        if 0 <= abs(final_move[0][0][0] - final_move[0][1][0]) <= 1 and 0 <= abs(
                final_move[0][0][1] - final_move[0][1][1]) <= 1:
            final_move = ((final_move[0][0][1], final_move[0][0][0]), (final_move[0][1][1], final_move[0][1][0]))
            file_write += "E " + str(final_move[0])[1:-1].replace(" ", '') + " " + str(final_move[1])[1:-1].replace(" ",
                                                                                                                    '')
        else:
            path = findPath(maxtrix, final_move[0])
            for p in path:
                file_write += "J " + str(p[0][1]) + "," + str(p[0][0]) + " " + str(p[1][1]) + "," + str(p[1][0]) + "\n"
file_write = file_write.rstrip('\n')
f = open("output.txt",'w')
f.write(file_write)
f.close()

