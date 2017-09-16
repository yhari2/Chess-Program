# Yasasvi Hari
# Section A 
# yhari
# 15112 Term Project
#########################################################
import pygame
import string
import copy
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255,215,0)
RED = (255,0,0)
GRAY= (192,192,192)
BLUE= (30,144,255)
GREEN= (0,230,0) 
DARKBLUE=(28,57,187)
YELLOW= (253,253,150)

class Piece(object):
    numRanks=8 # this will become useful later

    def __init__(self,name,color,board):
        self.name=name
        self.color=color
        self.hasMoved=False
        self.square=(0,0)
        self.board=board
        self.legalMoves=self.getLegalMoves()

    def __repr__(self):return self.color+self.name

    def __hash__(self):return hash(self.getHashables())

    def getHashables(self):
        return (self.name,self.color)

    def __eq__(self,other):pass

    def isLegalMove(self,newRank,newFile): 
        # ranks end at 7
        return (-1<newRank<Piece.numRanks and -1<newFile<Piece.numRanks)
    
    def setSquare(self,newSquare):self.square=newSquare

    def getLegalMoves(self):pass # to be overriden by each piece
    # returns set of legal moves

    def checkCollision(self,rank,file):
        # returns true if there is a collision with another piece
        if isinstance(self.board[rank][file],Piece):return True 
        else: return False

class Rook(Piece):
    motion=[(-1,0),(+1,0),(0,-1),(0,+1)] # all rooks have the same motion
    # forward, backward, left,right

    def __hash__(self):return hash(self.getHashables())


    def __eq__(self,other):return (isinstance(other,Rook) 
                                   and self.square==other.square)

    def getLegalMoves(self): # returns set of legal moves
        (startRank,startFile)=self.square
        result=set()
        for vector in Rook.motion:
            (dRank,dFile) = vector
            for mag in range(1,Piece.numRanks):
                newRank,newFile=startRank+mag*dRank,startFile+mag*dFile
                if not Piece.isLegalMove(self,newRank,newFile): break
                else:
                    if(isinstance(self.board[newRank][newFile],Piece) 
                       and self.board[newRank][newFile].color==self.color):
                        break
                    elif(isinstance(self.board[newRank][newFile],Piece) 
                       and self.board[newRank][newFile].color!=self.color):
                        result.add((newFile,newRank))
                        break
                    elif not isinstance(self.board[newRank][newFile],Piece):
                        result.add((newFile,newRank))
        return result

class Knight(Piece):
    motion=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(2,-1),(2,1),(1,2)]

    def __eq__(self,other):return (isinstance(other,Knight) 
                                   and self.square==other.square)
        
    def __hash__(self):return hash(self.getHashables())

    def getLegalMoves(self): # returns set of legal moves
        (startRank,startFile)=self.square
        result=[]
        for move in Knight.motion:
            (dRank,dFile)=move
            newRank,newFile=startRank+dRank,startFile+dFile
            if(self.isLegalMove(newRank,newFile)):
                if Piece.checkCollision(self,newRank,newFile)==True:
                    collidingPiece=self.board[newRank][newFile]
                    if collidingPiece.color==self.color:continue
                    else:
                        result.append((newFile,newRank))
                        continue
                else:result.append((newFile,newRank))
        return result

class Bishop(Piece):
    motion=[(-1,-1),        (-1,+1),
            (+1,-1),        (+1,+1)]

    def __eq__(self,other):return (isinstance(other,Bishop) 
                                   and self.square==other.square)

    def __hash__(self):return hash(self.getHashables())

    def getLegalMoves(self): # returns set of legal moves
        (startRank,startFile)=self.square
        result=[]
        for vector in Bishop.motion:
            (dFile,dRank)=vector
            for i in range(1,Piece.numRanks):
                newRank=startRank+i*dRank
                newFile=startFile+i*dFile
                if self.isLegalMove(newRank,newFile):
                    if self.checkCollision(newRank,newFile):
                        if self.board[newRank][newFile].color==self.color:
                            break
                        else: # accounts for captures
                            result.append((newFile,newRank))
                            break
                    result.append((newFile,newRank))
        return set(result)

class Queen(Piece):
    motion=[(-1,-1),(-1,+1),(+1,-1),(+1,+1),(-1,0),(+1,0),(0,-1),(0,+1)]

    def __eq__(self,other):return (isinstance(other,Queen) 
                                   and self.square==other.square)

    def __hash__(self):return hash(self.getHashables())

    def getLegalMoves(self): # returns set of legal moves
        (startRank,startFile)=self.square
        result=[]
        for vector in Queen.motion:
            (dRank,dFile)=vector
            for mag in range(1,Piece.numRanks):
                newRank,newFile=startRank+mag*dRank,startFile+mag*dFile
                if not Piece.isLegalMove(self,newRank,newFile): break
                elif(Piece.isLegalMove(self,newRank,newFile) and
                    Piece.checkCollision(self,newRank,newFile)!=True):
                    result.append((newFile,newRank))
                elif(Piece.isLegalMove(self,newRank,newFile) and 
                    Piece.checkCollision(self,newRank,newFile)):
                    # case on the colliding piece
                    if self.board[newRank][newFile].color==self.color:break
                    else:
                        result.append((newFile,newRank))
                        break # break out of the inner loop
        return set(result)

class King(Piece):
    motion=[(-1,-1),(-1,0),(-1,+1),
            (0,-1),         (0,+1),
            (+1,-1),(+1,0),(+1,+1)]

    def isLegalMove(self,newRank,newFile): 
        # ranks end at 7
        return (-1<newRank<Piece.numRanks and -1<newFile<Piece.numRanks 
                and self.avoidCheck(newRank,newFile))

    def __eq__(self,other):return (isinstance(other,King) 
                                   and self.square==other.square)

    def __hash__(self):return hash(self.getHashables())
    
    def getLegalMoves(self): #returns set of legal moves
        (startRank,startFile)=self.square
        result=[]
        for vector in King.motion:
            (dRank,dFile)=vector
            newRank,newFile=startRank+dRank,startFile+dFile
            if self.isLegalMove(newRank,newFile): 
                if(self.board[newRank][newFile]==None): 
                    result.append((newFile,newRank))
                elif (isinstance(self.board[newRank][newFile],Piece) 
                     and self.board[newRank][newFile].color!=self.color):
                    result.append((newFile,newRank))
        return set(result)

    def avoidCheck(self,newRank,newFile): # keeps the king out of check
        for rank in range(len(self.board)):
            for file in range(len(self.board[0])):
                if (isinstance(self.board[rank][file],Piece) and 
                    self.board[rank][file]!=self.color):
                    # we've found another piece, now check for checks
                    if (newRank,newFile) in self.board[rank][file].legalMoves:
                        return False
        return True

class Pawn(Piece):

    def __eq__(self,other):return (isinstance(other,Pawn) 
                                   and self.square==other.square)

    def __hash__(self):return hash(self.getHashables())
        
    def getLegalMoves(self): # returns set of legal moves
        vectors=[(0,-1),(0,-2)]
        (currRank,currFile) = self.square
        if self.color=="Black":vectors=[(0,+1),(0,+2)]
        if self.hasMoved:vectors.pop(1)
        result=[]
        for move in vectors:
            (dRank,dFile)=move
            newRank=currRank+dRank
            newFile=currFile+dFile
            if(Piece.isLegalMove(self,newRank,newFile)):
                if(not Piece.checkCollision(self,newRank,newFile)):
                    result.append((newFile,newRank))
                elif Piece.checkCollision(self,newRank,newFile):
                    break
        result.extend(self.getCaptures())
        return set(result)

    def getCaptures(self): # pawns capture diagonally
        result=[]
        captureVects=[(-1,-1),(-1,+1)]
        if self.color == 'Black': captureVects=[(1,-1),(1,1)]
        (currRank,currFile)=self.square
        for (dfile,drank) in captureVects:
            newRank,newFile=currRank+drank,currFile+dfile
            if (Piece.isLegalMove(self,newRank,newFile)==False): continue
            if (isinstance(self.board[newRank][newFile],Piece) and 
                self.board[newRank][newFile].color!=self.color):
                # since you can't take your own pieces
                result.append((newFile,newRank))
        return result

#####################  PLAYER  ###########################################

class Player(object):
    numPawns=8
    pieceNames=["Rook","Knight","Bishop","King","Queen","Pawn"]
    
    def __init__(self,color,board,screen):
        self.amInCheck=False
        self.isMyTurn=True
        self.amMated=False 
        self.color=color
        self.board=board
        self.pieces=[]
        self.getPieces()
        self.setBoard()
        # note that this comes after the board being set
        self.allLegalMoves=self.getAllLegalMoves()

    def getPieces(self): # gets pieces 
        for piece in Player.pieceNames:
            if piece=="Pawn": # last to be made
                for i in range(Player.numPawns):
                    self.pieces.append(Pawn(piece+str(i),
                                            self.color,self.board))
            elif piece=="King":self.pieces.append(King(piece,self.color,
                                                       self.board))
            elif piece=="Queen": self.pieces.append(Queen(piece,self.color,
                                                          self.board))
            elif piece in set(["Rook","Knight","Bishop"]):
                for i in range(2):
                    if piece=="Rook":
                        self.pieces.append(Rook(piece,self.color,self.board))
                    elif piece=="Knight": 
                        self.pieces.append(Knight(piece,self.color,self.board))
                    elif piece=="Bishop": 
                        self.pieces.append(Bishop(piece,self.color,self.board))

    def setBoard(self): # sets pawns, K, Q
        otherPieces,pawns=self.pieces[0:8],self.pieces[8:]
        secondRank,backRank=6,7
        if self.color=="Black": secondRank,backRank=1,0
        for i in range(len(pawns)):
            self.board[i][secondRank]=pawns[i]
            pawns[i].setSquare((i,secondRank))
        self.board[3][backRank]=otherPieces.pop() # Queen
        self.board[3][backRank].setSquare((3,backRank))
        self.board[4][backRank]=otherPieces.pop() # King
        self.board[3][backRank].setSquare((4,backRank))
        while(otherPieces!=[]): 
            # This will deal with all of the doubles
            L=otherPieces[0:2]
            otherPieces=otherPieces[2:]
            self.setSidePieces(L,backRank)

    def setSidePieces(self,L,backRank): # sets the Rook, Knight, Bishop
        if isinstance(L[0],Rook): 
            self.board[0][backRank]=L[0]
            self.board[7][backRank]=L[1]
            L[0].setSquare((0,backRank))
            L[1].setSquare((7,backRank))
        elif isinstance(L[0],Knight): 
            self.board[1][backRank]=L[0]
            self.board[6][backRank]=L[1]
            L[0].setSquare((1,backRank))
            L[1].setSquare((6,backRank))
        elif isinstance(L[0],Bishop): 
            self.board[2][backRank]=L[0]
            self.board[5][backRank]=L[1]
            L[0].setSquare((2,backRank))
            L[1].setSquare((5,backRank))

    def getAllLegalMoves(self): # returns dict of all of the possible moves
        legalMoves=dict()
        for i in range(len(self.pieces)):
            currPiece=self.pieces[i]
            legalMoves[currPiece]=currPiece.getLegalMoves()
        legalMoves=dict(legalMoves)
        return legalMoves

######################## GRAPHICS ############################################

def init(data,screen):
    data.screen=screen
    data.ranks=data.files=8
    data.board=getBoard(data)
    data.width=data.height=650 # of the board
    data.winWidth=data.winHeight=800
    data.margin=50
    data.pieceNames=pieceNames=["Rook","Knight","Bishop","King","Queen","Pawn"]
    data.images=loadPieces(data,screen)
    data.white=Player("White",data.board,screen)
    data.black=Player("Black",data.board,screen)
    data.mode="startScreen"
    data.clickedPiece=[] #this will be modified as the player clicks on a piece
    data.font=pygame.font.SysFont("Arial", 30)
    data.clickedPiece=None # will change to be clicked piece
    data.clickedPieceSquare=None
    data.hilightedSquares=set()
    data.pieceMoves=set()
    data.turn=0
    data.score=[] # notation
    data.helpCenter=None # These 3 are used for the startscreen
    data.customizeCenter=None
    data.boardCenter=None
    data.backCenter=None
    data.currMove=0
    data.capturedPieces=[]
    data.aiOn=False
    if data.aiOn==True:
        if data.turn%2==0:amMaximizing(data,data.board)
        else:amMinimizing(data,data.board)
    data.bestMove=None

def play(data,rank,file):
    if data.clickedPiece==None:return # double check
    if (data.board[rank][file]==data.clickedPiece):
        data.clickedPiece=None
        data.possMoves.clear()
        data.hilightedSquares.clear()
        data.clickedPieceSquare=None
        return # so as to avoid pieces disappearing if you click it twice
    if((data.turn%2==0 and data.clickedPiece.color=="White") 
        or (data.turn%2==1 and data.clickedPiece.color=="Black")):
        piece=data.clickedPiece
        (currRank,currFile)=piece.square
        data.clickedPiece=None
        data.hilightedSquares.clear()
        if (file,rank) not in data.possMoves:# illegal moves
            data.clickedPiece=None
            data.clickedPieceSquare=None
            data.hilightedSquares.clear()
            return
        else:# legal move 
            if(isinstance(data.board[rank][file],Piece)):
                if data.turn%2==0: 
                    # White's move, piece is in legal moves
                    oppPiece=data.board[rank][file] # opponent's piece
                    data.black.pieces.remove(oppPiece)
                    data.capturedPieces.append(oppPiece)
                    # this is to ensure that this piece is not accounted 
                    #for by the AI
                else:
                    # Black's move, legal move
                    oppPiece=data.board[rank][file] # opponent's piece
                    data.white.pieces.remove(oppPiece)
                    data.capturedPieces.append(oppPiece)
            data.board[rank][file]=piece
            piece.square=(file,rank)
            data.score.append((piece,(currFile,currRank),(file,rank)))
            data.board[currRank][currFile]=None
            piece.hasMoved=True
            data.turn+=1
            data.clickedPieceSquare=None
            data.clickedPiece=None
            if data.aiOn:
                if data.turn%2==0:amMaximizing(data,data.board)
                else:amMinimizing(data,data.board)
    else:# picked a piece of the opposite color
        data.clickedPieceSquare=None
        data.clickedPiece=None
        return

def printPieces(data):
    for person in [data.white,data.black]:
        for piece in person.pieces:
            print(piece.name,piece.square)
         
def getBoard(data):
    result=[]
    toAdd=[]
    for eachRank in range(data.ranks):
        for eachFile in range(data.files):
            toAdd.append(None) # empty string= emptySquare
        result.append(toAdd)
        toAdd=[]
    return result

def keyPressed(data, key):pass

def mousePressed(data, x, y):
    if data.mode=="startScreen":
        r=85
        (xb,yb)=data.boardCenter[0],data.boardCenter[1]
        (xh,yh)=data.helpCenter[0],data.helpCenter[1]
        if((xb-r<=x<=xb+r) and (yb-r<=y<=yb+r)):data.mode='board'
        elif((xh-r<=x<=xh+r) and (yh-r<=y<=yh+r)):data.mode='help'
    elif data.mode=="help":handleHelp(data,x,y)
    elif data.mode=="board":handleBoard(data,x,y)

def handleHelp(data,x,y):
    #(data.margin,data.winHeight-2*data.margin,
    #data.winWidth-14*data.margin,data.margin)
    cX=(data.margin+data.winWidth-14*data.margin)
    cY=(data.margin+data.winHeight-2*data.margin)
    xWidth,yHeight=(data.winWidth-14*data.margin),data.margin
    #(data.winWidth-3*data.margin,data.winHeight-2*data.margin,
    #data.winWidth-14*data.margin,data.margin)
    cNextX=data.winWidth-3*data.margin+data.winWidth-14*data.margin
    cNextY=data.winWidth-data.margin
    cNextWidth,cNextHeight=data.winWidth-14*data.margin,data.margin
    if((cX-xWidth<x<cX+xWidth) and (cY-yHeight<y<cY+yHeight)):
        data.mode="startScreen"
    elif((cNextX-cNextWidth<=x<=cNextX+cNextWidth) and 
        (cNextY-cNextHeight<=y<=cNextY+cNextHeight)):data.mode='king'

def handleBoard(data,x,y):
    #(0,0,1.5*data.margin,data.margin-10)
    #(data.winWidth-2*data.margin,0,data.winWidth,data.margin-10)
    if((0<x<1.5*data.margin) and (0<y<data.margin-10)):data.mode='help'
    elif((0<x<=2*data.winWidth-2*data.margin) and (0<y<=data.margin-10)):
        data.aiOn=not data.aiOn
    (nextRank,nextFile)=getSquare(x,y,data)
    if (nextRank,nextFile)==(-1,-1):
        data.clickedPiece=None
        data.clickedPieceSquare=None
        data.hilightedSquares=set()
        return
    if isinstance(data.clickedPiece,Piece):
        play(data,nextRank,nextFile)
        data.hilightedSquares.clear()
    else:
        # then there is no clicked piece
        if isinstance(data.board[nextRank][nextFile],Piece):
            data.clickedPiece=data.board[nextRank][nextFile]
            data.possMoves=data.clickedPiece.getLegalMoves()
            data.clickedPieceSquare=data.clickedPiece.square
            for move in data.possMoves:
                data.hilightedSquares.add(move)

def clickOnBoard(data,x,y):
    # ensure that it's not on the margin 
    return ((data.margin<x<data.width-data.margin) and 
            (data.margin<y<data.height-data.margin))

def getSquare(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not clickOnBoard(data,x, y)):return (-1, -1)
    boardWidth  = data.width - 2*data.margin
    boardHeight = data.height - 2*data.margin
    fileWidth  = boardWidth / data.files
    rankHeight = boardHeight / data.ranks
    file = (y - data.margin) // fileWidth
    rank = (x - data.margin) // rankHeight
    return (int(rank),int(file))

# clickOnBoard and getSquare were adapted from the 112 Course notes

def mouseMoved(data, buttons, x, y):
    pass

def drawWinCondition(data,color):
    data.screen.fill(BLUE)
    rect=(data.winWidth//2,data.winHeight//2,data.winWidth//2+data.margin,
          data.winHeight//2+data.margin)

    contentFont=pygame.font.SysFont("Arial",50)
    content= color +"wins!"
    contentSurf=contentFont.render(content,GOLD,True,pygame.SRCALPHA)
    data.screen.blit(contentSurf,rect)
    
def drawBoard(data):
    data.screen.fill(BLUE) 
    if data.white.pieces==[]:
        drawWinCondition(data,"Black")
        return
    elif data.black.pieces==[]:
        drawWinCondition(data,"White")
        return
    for rank in range(data.ranks):
        for file in range(data.files):
            (x,y,colWidth,rowHeight)=getSquareBounds(rank,file,data)
            if (rank+file)%2==0: 
                pygame.draw.rect(data.screen,WHITE,(x,y,colWidth,rowHeight))
            if (rank+file)%2==1: 
                pygame.draw.rect(data.screen,GRAY,(x,y,colWidth,rowHeight))
            if (rank,file) in data.hilightedSquares:
                pygame.draw.rect(data.screen,YELLOW,(x,y,colWidth,rowHeight))
            if (file,rank)==data.clickedPieceSquare:
                pygame.draw.rect(data.screen,GOLD,(x,y,colWidth,rowHeight))
    drawScoreSheet(data)
    drawNavBar(data)
    drawCapturedPieces(data)
    if data.aiOn:drawAI(data)

def drawCapturedPieces(data):
    spacing=20 # spacing from edge of board
    kingIndex=3 # the index of the white king image in the images list
    capturedRect=(data.width-data.margin+spacing,4*data.margin,3.5*data.margin,
                  data.winHeight-15*spacing+data.margin*1.5)
    pygame.draw.rect(data.screen,WHITE,capturedRect)

    headerFont=pygame.font.SysFont("Arial", 20)
    headerText=headerFont.render("Captured Pieces:",True,BLACK,pygame.SRCALPHA)
    data.screen.blit(headerText,capturedRect)

    xOffSet=55
    yOffSet=55
    y=6*data.margin-yOffSet
    for piece in data.capturedPieces:
        width=0.5*data.margin
        height=55
        if y+height>=4*data.margin+data.winHeight-15*spacing+data.margin*1.5:
            y=6*data.margin-yOffSet
            xOffSet+=55
        x=data.width-data.margin*2+xOffSet+10
        pieceRect=(x,y,width,height)
        if (isinstance(piece,Pawn) and piece.color=="White"):
            data.screen.blit(data.images[len(data.images)//2-1],pieceRect)
        elif (isinstance(piece,Pawn) and piece.color=="Black"):
            data.screen.blit(data.images[-1],pieceRect)
        elif (isinstance(piece,Rook) and piece.color=="White"):
            data.screen.blit(data.images[0],pieceRect)
        elif (isinstance(piece,Rook) and piece.color=="Black"):
            data.screen.blit(data.images[2*kingIndex],pieceRect)
        elif (isinstance(piece,Bishop) and piece.color=="White"):
            data.screen.blit(data.images[2],pieceRect)
        elif (isinstance(piece,Bishop) and piece.color=="Black"):
            data.screen.blit(data.images[2*kingIndex+2],pieceRect)
        elif (isinstance(piece,Knight) and piece.color=="White"):
            data.screen.blit(data.images[1],pieceRect)
        elif (isinstance(piece,Knight) and piece.color=="Black"):
            data.screen.blit(data.images[2*kingIndex+1],pieceRect)
        elif (isinstance(piece,Queen) and piece.color=="White"):
            data.screen.blit(data.images[kingIndex+1],pieceRect)
        elif (isinstance(piece,Queen) and piece.color=="Black"):
            data.screen.blit(data.images[kingIndex**2+1],pieceRect)
        y+=yOffSet

            
def drawNavBar(data):
    spacing=20
    navFont=pygame.font.SysFont("Arial",30)

    navBar=(0,0,data.winWidth,data.margin-0.5*spacing)
    pygame.draw.rect(data.screen,WHITE,navBar)

    helpRect=(0,0,1.5*data.margin,data.margin-spacing//2)
    helpText=navFont.render("Help", True,WHITE,pygame.SRCALPHA)
    pygame.draw.rect(data.screen,BLACK,helpRect)
    data.screen.blit(helpText,helpRect)

    spacing=100

    content=""
    if data.turn%2==0: content+="White"
    else: content+='Black'
    content+="'s Move"
    contentText=navFont.render(content,True,BLACK,pygame.SRCALPHA)
    contentRect=(data.width//2,0,data.margin+4*spacing,
                 data.margin-0.5*spacing)
    data.screen.blit(contentText,contentRect)

    aiText="AI Off"
    if data.aiOn==True:aiText="AI On"
    aiRect=(data.winWidth-2*data.margin,0,data.winWidth,data.margin-10)
    AIText=navFont.render(aiText,True,WHITE,pygame.SRCALPHA)
    pygame.draw.rect(data.screen,BLACK,aiRect)
    data.screen.blit(AIText,aiRect)

def drawAI(data):
    spacing=20
    if data.bestMove==None:return
    aiFont= pygame.font.SysFont("Arial",25)
    outerRect=(data.width-data.margin+spacing,data.margin,
               data.width-9.5*data.margin,2*data.margin)
    pygame.draw.rect(data.screen,WHITE,outerRect)

    aiText= aiFont.render("Coach thinks:",True, BLACK, pygame.SRCALPHA)
    data.screen.blit(aiText,(data.width-data.margin+spacing,data.margin,
                     data.winWidth-2*data.margin-data.width,data.margin))
    
    recommText=writeRecommendation(data)
    recommFont=pygame.font.SysFont("Arial", 15)
    recommSurf=recommFont.render(recommText, True, BLACK,pygame.SRCALPHA)
    recommRect=((data.width-data.margin+spacing),data.margin+50,data.winWidth,
                data.margin*10)
    data.screen.blit(recommSurf,recommRect)

def drawScoreSheet(data):
    spacing=40
    rect=(data.margin,data.width-data.margin,data.width-2*data.margin,
          data.winHeight-15*spacing-0.5*data.margin)
    pygame.draw.rect(data.screen,WHITE,rect)

    headerFont =pygame.font.SysFont("Arial",30)
    header = headerFont.render("Score:",True, BLACK, pygame.SRCALPHA)
    headerRect=(data.margin,data.width-data.margin,data.width,
                    data.height-data.margin)

    scoreFont=pygame.font.SysFont("Arial",20)


    data.screen.blit(header,headerRect)
    if data.score!=[]:
        text=""
        count=0
        for move in data.score:
            text+=" "+convertToChessNotation(move)+" "
        textRect=(data.margin,data.width-data.margin+spacing,data.width,
                    data.height-data.margin)
        moves=scoreFont.render(text,True,BLACK,pygame.SRCALPHA)
        data.screen.blit(moves,textRect)

def convertToChessNotation(move):
    result=""
    piece,startMove,endMove=move[0],move[1],move[2]
    if isinstance(piece,King):result+="K"
    elif isinstance(piece,Knight):result+="N"
    elif isinstance(piece,Bishop):result+="B"
    elif isinstance(piece,Rook):result+="R"
    elif isinstance(piece,Queen):result+="Q"
    result+=getNumbers(move)
    return result

def getNumbers(move):
    endMove=move[2]
    (rank,file)=endMove
    result=""
    if file==0:result+='a'
    elif file==1: result+='b'
    elif file==2: result+='c'
    elif file==3: result+='d'
    elif file==4: result+='e'
    elif file==5: result+='f'
    elif file==6: result+='g'
    else: result+='h'
    result+=str(8-rank)
    return result

def drawHelpScreen(data):
    data.screen.fill(BLUE)

    headerFont=pygame.font.SysFont("Arial",50)
    textFont=pygame.font.SysFont("Arial",25)
    backFont=pygame.font.SysFont("Arial",25)

    pygame.draw.rect(data.screen,WHITE,(data.margin,data.margin,
                    data.winHeight-2*data.margin,data.winWidth-2*data.margin))

    header=headerFont.render("Help",True,BLACK,pygame.SRCALPHA)
    backText=backFont.render("Back",True,BLACK,pygame.SRCALPHA)

    spacing=100

    headerRect=(data.width//2, data.margin+10, data.margin,data.margin)
    data.screen.blit(header,headerRect)

    backRect=(data.margin,data.winHeight-2*data.margin,
              data.winWidth-14*data.margin,data.margin)
    pygame.draw.rect(data.screen,GOLD,backRect)
    data.screen.blit(backText,backRect)
    drawBody(data)

def drawBody(data):
    spacing=100

    bodyFont=pygame.font.SysFont("Arial",15)

    body= """\nWelcome to BabyBlue! This is a 15-112 Term Project made by Yasasvi Hari. The artwork on the main\nmenu was done by my friend Shiva Peri.\n\n\nThis project came together with help from Prof. David Kosbie, Prof. David Andersen, and numerous \nfriends including, but not limited to, David Bick, Joe Segel, and Keith Kozlosky.The goal of this game is to \ncapture your opponent's pieces.\n\nThis app's has a few main functionalities. Apart from the chessboard and pieces, it also keeps track of the \ngame, located in the scoresheet feature. Additionally, when you click on each piece, the piece is highlighted \nin a dark gold color, and all of its possible moves, including captures, are highlighted in a lighter yellow color.\n\nThe game also keeps track of captured pieces, and displays them in the captured pieces menu. It is \nintended as a chess mentor for beginning chess players. It has a simple AI that suggests one move at \na time to the user. This AI likes to capture as many pieces as it can. You can toggle between playing with \nthe AI and playing without it by pressing the 'AI Off'/'AI On' button on the navbar on the \nboard. The "AI On" setting significantly slows gameplay, while the "AI Off" feature preserves the \ninstantaneous feel of the game. The navbar also displays whose move it currently is.\n\n\nTo go back to the main menu, please click the 'back' button.
    """

    for content in body.splitlines():
        contentSurf=bodyFont.render(content,True,BLACK,pygame.SRCALPHA)
        y=data.margin+spacing
        bodyRect=(data.margin,y,data.winWidth-2*data.margin,
            data.winHeight-2*data.margin)
        data.screen.blit(contentSurf,bodyRect)
        spacing+=15


def drawStartScreen(data):
    data.screen.fill(BLUE)
    bigFont=pygame.font.SysFont("Arial",72)
    buttonFont=pygame.font.SysFont("Arial",30)
    headerRect=(data.margin,data.margin,data.width-2*data.margin,
                data.height-data.margin)
    header=bigFont.render("Welcome to BabyBlue!",True, WHITE, pygame.SRCALPHA)
    data.screen.blit(header,headerRect)

    spacing=150 # space between each of the circles
    boardCircle=(data.margin,data.height-data.margin,2*data.margin,data.margin) 
    boardText=buttonFont.render("Board",True,BLACK,pygame.SRCALPHA)
    pygame.draw.circle(data.screen,GOLD,
            (2*data.margin,data.height-data.margin),85)
    pygame.draw.circle(data.screen,WHITE,
                      (2*data.margin,data.height-data.margin),75)

    data.boardCenter=boardText.get_rect(center=(2*data.margin,
                                        data.height-data.margin))

    data.screen.blit(boardText,data.boardCenter)
    helpText=buttonFont.render("Help", True,BLACK,pygame.SRCALPHA)
    
    pygame.draw.circle(data.screen,GOLD,(2*data.margin+4*spacing,
        8*data.height-data.margin),85)

    pygame.draw.circle(data.screen,GOLD,(2*data.margin+4*spacing,
                                    data.height-data.margin),85)
    pygame.draw.circle(data.screen,WHITE,(2*data.margin+4*spacing,
                                    data.height-data.margin),75)
    data.helpCenter=helpText.get_rect(center=(2*data.margin+4*spacing,
                                      data.height-data.margin))
    data.screen.blit(helpText,data.helpCenter)

    creditFont=pygame.font.SysFont("Arial",15)
    credit=creditFont.render("A 15-112 term project by Yasasvi Hari.",True, 
                            WHITE,pygame.SRCALPHA)
    data.screen.blit(credit,(data.width//2-data.margin, 
                             data.winWidth-data.margin))

    logo = pygame.image.load("Logo.jpg").convert()
    logo.set_colorkey((255,255,255))
    (cX,cY)= logo.get_size()
    logo = pygame.transform.scale(logo,(cX//3,cY//3))
    spacing=40
    logoRect = logo.get_rect(center = (data.winHeight//2,
                                data.winWidth//2-spacing))

    # this logo was created by my friend Shiva Peri    
    data.screen.blit(logo,logoRect)

def loadPieces(data,screen):
    result=[]
    # ["Rook","Knight","Bishop","King","Queen",Pawn"]
    for color in ["White","Black"]:
        for piece in data.pieceNames:
            fileName=color+piece+'.png'
            result.append(pygame.image.load(fileName))
    return result

def placePieces(data):
    # now, the pieces are saved in self.images
    # we will now take the pieces and place them on the board
    for rank in range(len(data.board)):
        for file in range(len(data.board[0])):
            if isinstance(data.board[rank][file],Piece):
                createPieces(data,rank,file)

def createPieces(data,rank,file):
    (x0,y0)=getCellBounds(data,rank,file)
    piece=data.board[rank][file]
    kingIndex=3 # the index of the white king image in the images list
    if (isinstance(piece,Pawn) and piece.color=="White"):
        data.screen.blit(data.images[len(data.images)//2-1],(x0,y0))
    elif (isinstance(piece,Pawn) and piece.color=="Black"):
        data.screen.blit(data.images[-1],(x0,y0))
    elif (isinstance(piece,Rook) and piece.color=="White"):
        data.screen.blit(data.images[0],(x0,y0))
    elif (isinstance(piece,Rook) and piece.color=="Black"):
        data.screen.blit(data.images[2*kingIndex],(x0,y0))
    elif (isinstance(piece,Bishop) and piece.color=="White"):
        data.screen.blit(data.images[2],(x0,y0))
    elif (isinstance(piece,Bishop) and piece.color=="Black"):
        data.screen.blit(data.images[2*kingIndex+2],(x0,y0))
    elif (isinstance(piece,Knight) and piece.color=="White"):
        data.screen.blit(data.images[1],(x0,y0))
    elif (isinstance(piece,Knight) and piece.color=="Black"):
        data.screen.blit(data.images[2*kingIndex+1],(x0,y0))
    elif (isinstance(piece,King) and piece.color=="White"):
        data.screen.blit(data.images[kingIndex],(x0,y0))
    elif (isinstance(piece,King) and piece.color=="Black"):
        data.screen.blit(data.images[kingIndex**2],(x0,y0))
    elif (isinstance(piece,Queen) and piece.color=="White"):
        data.screen.blit(data.images[kingIndex+1],(x0,y0))
    elif (isinstance(piece,Queen) and piece.color=="Black"):
        data.screen.blit(data.images[kingIndex**2+1],(x0,y0))
    piece.setSquare((rank,file))
            

def getCellBounds(data,rank,file):
    # adapted from 15-112 notes
    margin=50
    gridWidth  = data.width - 2*margin
    gridHeight = data.height - 2*margin
    columnWidth = gridWidth / len(data.board[0])
    rowHeight = gridHeight / len(data.board)
    x0 = margin + rank * columnWidth
    y0 = margin + file * rowHeight
    return (x0,y0)

def getSquareBounds(row,col,data):
    gridWidth=data.width-2*data.margin
    gridHeight=data.height-2*data.margin
    colWidth=gridWidth//data.files
    rowHeight=gridHeight//data.ranks
    x0=data.margin+(col)*colWidth
    y0=data.margin+(row)*rowHeight
    return (x0,y0,colWidth,rowHeight)

def amMinimizing(data,board,alpha=-10**6,beta=10**6,depth=3):
    ev=10**6 # arbitrarily large 
    currBoard=copy.deepcopy(board)
    if depth==0: return estimator(data,currBoard,"black")
    for eachPiece in data.black.pieces:
        if data.black.allLegalMoves.get(eachPiece)==set():continue
        for eachMove in eachPiece.getLegalMoves():
            if eachMove==None:continue
            currSquare=eachPiece.square
            newBoard=makeMove(currBoard,eachMove,currSquare,eachPiece)
            maxEval=amMaximizing(data,newBoard,alpha,beta,depth-1)
            #if depth%2==0:return bestMove
            if maxEval<ev:data.bestMove=(eachPiece,eachMove)
            ev=min(maxEval,ev)
            if ev<=beta: # if they are equal, we are indifferent
                # update bestMove and beta
                data.bestMove=(eachPiece,eachMove)
                beta=ev
            if beta<=alpha:
                break # cut off beta
                # move onto next move
    return ev

def amMaximizing(data,board,alpha=-10**6,beta=10**6,depth=3):
    ev=-10**6 # arbitrarily large 
    currBoard=copy.deepcopy(board)
    if depth==0: return estimator(data,currBoard,"white")
    for eachPiece in data.white.pieces:
        if data.white.allLegalMoves.get(eachPiece)==set():continue
        for eachMove in eachPiece.getLegalMoves():
            if eachMove==None:continue
            currSquare=eachPiece.square
            newBoard=makeMove(currBoard,eachMove,currSquare,eachPiece)
            #if depth%2==0:return bestMove
            minEval=amMinimizing(data,newBoard,alpha,beta,depth-1)
            if minEval>ev:data.bestMove=(eachPiece,eachMove)
            ev=max(minEval,ev)
            if ev>=alpha: # if they are equal, we are indifferent
                # update bestMove and beta
                data.bestMove=(eachPiece,eachMove)
                alpha=ev
            if beta<=alpha:
                break # cut off alpha
                # move onto next move
    return ev

def writeRecommendation(data):
    (piece,square)=data.bestMove
    (rank,file)=square
    result=""
    if isinstance(piece,King):result+="K"
    elif isinstance(piece,Knight):result+="N"
    elif isinstance(piece,Bishop):result+="B"
    elif isinstance(piece,Rook):result+="R"
    elif isinstance(piece,Queen):result+="Q"
    if file==0:result+='a'
    elif file==1: result+='b'
    elif file==2: result+='c'
    elif file==3: result+='d'
    elif file==4: result+='e'
    elif file==5: result+='f'
    elif file==6: result+='g'
    else: result+='h'
    result+=str(8-rank)
    return result

def makeMove(board,move,currSquare,piece):
    newFile,newRank=move # unpacking
    currRank,currFile=currSquare
    if (newFile,newRank) in piece.legalMoves:
        board[currRank][currFile]=None
        board[newRank][newFile]=piece
    return board

def estimator(data,board,color):
    # pieces are counted by tempi- 3 tempi/pawn
    whiteCount=1 # since White goes first
    blackCount=0
    for rank in range(len(board)):
        for file in range(len(board[0])):
            if isinstance(board[rank][file],Piece):
                if(isinstance(board[rank][file],Queen) 
                    and board[rank][file].color=="White"):whiteCount+=9*3
                elif(isinstance(board[rank][file],Queen) 
                    and board[rank][file].color=="Black"):blackCount-=9*3
                elif(isinstance(board[rank][file],Rook) 
                    and board[rank][file].color=="White"):whiteCount+=5*3
                elif(isinstance(board[rank][file],Rook) 
                    and board[rank][file].color=="Black"):blackCount-=5*3
                elif(isinstance(board[rank][file],Bishop) 
                    and board[rank][file].color=="White"):whiteCount+=3*3
                elif(isinstance(board[rank][file],Bishop)
                    and board[rank][file].color=='Black'):blackCount-=3*3
                elif(isinstance(board[rank][file],Knight) 
                    and board[rank][file].color=="White"):whiteCount+=3*3
                elif(isinstance(board[rank][file],Knight)
                    and board[rank][file].color=='Black'):blackCount-=3*3
                elif(isinstance(board[rank][file],Pawn) 
                    and board[rank][file].color=="White"):whiteCount+=3
                elif(isinstance(board[rank][file],Pawn)
                    and board[rank][file].color=='Black'):blackCount-=3
    whiteCount+=spaceCalc(data,board,"white")
    blackCount-=spaceCalc(data,board,"black")
    return whiteCount*blackCount

def spaceCalc(data,board,color):
    result=0
    if color=="white":
        for piece in data.white.allLegalMoves:
            result+=len(data.white.allLegalMoves[piece])
    else:
        for piece in data.black.allLegalMoves:
            result+=len(data.black.allLegalMoves[piece])
    return result

def redrawAll(data):
    if data.mode=="startScreen":drawStartScreen(data)
    elif data.mode=="help":drawHelpScreen(data)
    else:
        drawBoard(data)
        placePieces(data)
        

def main():
    pygame.init()
    clock = pygame.time.Clock()
    # create the display surface
    screen = pygame.display.set_mode((800, 800))

    playing = True

    class Struct(object): pass
    data = Struct()

    init(data,screen)
    while True:
        pygame.time.delay(5)
        for event in pygame.event.get():
            #printPieces(data)
            if event.type == pygame.QUIT:
                playing=False
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                keyPressed(data, event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousePressed(data, *event.pos)
            elif event.type == pygame.MOUSEMOTION:
                mouseMoved(data, event.buttons, *event.pos)
        screen.fill(WHITE)
        redrawAll(data)
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()

if __name__ == '__main__':main()

# All pieces came from the WikiMedia Commons
# https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

# Animations adapted from Lukas Pereza's code on github
# https://github.com/LBPeraza/Pygame-Asteroids/blob/master/Examples/EventsExample.py