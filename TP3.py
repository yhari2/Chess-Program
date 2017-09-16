##################################
# Term Project  by Ashwin Anbu
####################################

from tkinter import * #barebones from 15-112 Website
from PIL import Image, ImageTk
import time
import copy
import io
####################################
# OOP for Chess Pieces
####################################

class ChessPiece(object):
    def __init__(self, pieceValue,color, location): 
        self.pieceValue=pieceValue #numerical piece value 
        self.color=color #piece color
        self.location=location #Tuple of position
    
    def isKinginTrouble(self,board,color):
        Kinglocation=None #Finds king of whoever's turn it is. 
        KingColor=None
        currentboard=board
        for col in range(len(board[1])):
            for row in range(len(board)):
                piece=board[col][row]
                if piece =="0": continue
                if isinstance(piece,King) and piece.color== color:
                    Kinglocation=(row,col) 
                    # print ("THE KING IS HERE",Kinglocation)
                    
        for col in range(len(board[1])): #finds pieces that can check. 
            for row in range(len(board)):
                piece=board[col][row]
                if piece =="0": continue
                if piece.color!= color:
                    piecelocation=(row,col)
                    if piece.isMoveLegal(piecelocation, Kinglocation,piece.color,piece,currentboard)==True: 
                        return True
        return False
        
    def isMoveLegal(self,oldlocation,location,turn,piece,board):  
        testboard=board

        if board[oldlocation[1]][oldlocation[0]]== "0": 
            return False
        if board[location[1]][location[0]]!="0":
            piece=board[location[1]][location[0]]
            # print ("piece is", piece, "color is", color, self.color)
            if piece.color==self.color: return False
        if self.color!=turn: return False
        if location[0]<0 or location[0]>7 or location[1]<0 or location[1]>7: return False
        if isinstance(self,Pawn):
            if self.color=="white":
                if oldlocation[1] == 6 :
                    if location[1]-oldlocation[1]==-2: 
                        if location[0]-oldlocation[0]!=0: return False
                    elif location[1]-oldlocation[1]==-1:
                         if location[0]-oldlocation[0]<-1 or location[0]-oldlocation[0]>1: return False
                         
                    else: return False
                         
                elif location[1]-oldlocation[1]!=-1: return False
                elif location[0]-oldlocation[0]<-1 or location[0]-oldlocation[0]>1: return False
                else: print ("continue")
            if self.color=="black":
                if oldlocation[1] == 1 :
                    if location[1]==3:
                        if location[0]-oldlocation[0]!=0: return False
                    elif location[1]==2:
                        if location[0]-oldlocation[0]>1 or location[0]-oldlocation[0]<-1: return False
                        else: print ("continue")
                    else: return False
                elif location[1]-oldlocation[1]!=1:return False
                elif location[0]-oldlocation[0]>1 or location[0]-oldlocation[0]<-1: return False
                else: print ("continue")

        if isinstance(self,Knight):
            if oldlocation[1]-location[1]>2 or oldlocation[1]-location[1]<-2: return False
            if oldlocation[0]-location[0]>2 or oldlocation[0]-location[0]<-2: return False
            if oldlocation[1]-location[1]==2 or oldlocation[1]-location[1]==-2:
                if oldlocation[0]-location[0]==1 or oldlocation[0]-location[0]==-1: print ("continue")
                else: return False
            elif oldlocation[0]-location[0]==2 or oldlocation[0]-location[0]==-2:
                if oldlocation[1]-location[1]==1 or oldlocation[1]-location[1]==-1: print ("continue")
                else: return False
            else: return False
            
        if isinstance(self,Bishop):
            if oldlocation[1]-location[1]==oldlocation[0]-location[0] or oldlocation[1]-location[1]==-1*(oldlocation[0]-location[0]):print (" ")
            else:return False
 
        if isinstance(self,Rook):
            if oldlocation[1]!=location[1] and oldlocation[0]!=location[0]: return False

        if isinstance(self,Queen):
            if oldlocation[1]-location[1]==oldlocation[0]-location[0] or oldlocation[1]-location[1]==-1*(oldlocation[0]-location[0]):print ("yes")
            elif oldlocation[1]!=location[1] and oldlocation[0]!=location[0]: return False
        if isinstance(self,King):
            if oldlocation[1]-location[1]>1 or oldlocation[1]-location[1]<-1: return False
            if oldlocation[0]-location[0]>1 or oldlocation[0]-location[0]<-1: return False
        oldpiece=testboard[oldlocation[1]][oldlocation[0]]
        return True
        #need to account for if King is in check 
        
    def setImage(self, file=None): 
    #http://pillow.readthedocs.io/en/3.4.x/reference/Image.html
        pillowImage=Image.open(file)
        pillowImage=flattenAlpha(pillowImage)
        size= 80,80
        pillowImage = pillowImage.resize(size)
        image = ImageTk.PhotoImage(pillowImage)
        self.piece=image
    
    def drawPiece(self, canvas, data,row,col):
        file, rank = col,row
        
        x = file*data.cellSize + data.cellSize/2 + data.xcentering
        y = rank*data.cellSize + data.cellSize/2 +data.ycentering
        
        canvas.create_image(x,y,image=self.piece)
    def __repr__(self):
        return ("ChessPiece@%s" %(str(self.location))) 

class Pawn(ChessPiece):
    allPawns = []
    def __init__(self, color, location,):
        pieceValue=1
        super().__init__(pieceValue,color,location)
        if (self.color=="white"):
            self.setImage("Pawn.PNG")
            
        elif (self.color=="black"):
            self.setImage("BlackPawn.PNG")
        Pawn.allPawns += [self]
    def __repr__(self):
        if self.color=="white":
            return ("P@%s" %(str(self.location))) 
        else: return ("p@%s" %(str(self.location))) 
            
class Bishop(ChessPiece):
    allBishops=[]
    def __init__(self, color, location):
        pieceValue=3
        super().__init__(pieceValue,color,location)
        if (self.color=="white"):
            self.setImage("Bishop.PNG") 
        elif (self.color=="black"):
            self.setImage("BlackBishop.PNG") 
        Bishop.allBishops += [self]
    def __repr__(self):
        if self.color=="white":
            return ("B@%s" %(str(self.location))) 
        else: return ("b@%s" %(str(self.location))) 
            

        
class Knight(ChessPiece):
    allKnights=[]
    def __init__(self, color, location):
        pieceValue=3
        super().__init__(pieceValue,color,location)
        if (self.color=="white"):
            self.setImage("Knight.PNG") 
        elif (self.color=="black"):
            self.setImage("BlackKnight.PNG") 
        Knight.allKnights += [self]
    def __repr__(self):
        if self.color=="white":
            return ("N@%s" %(str(self.location))) 
        else: return ("n@%s" %(str(self.location))) 
            
class Rook (ChessPiece):
    allRooks=[]
    def __init__(self, color, location):
        pieceValue=5
        super().__init__(pieceValue,color,location)
        if (self.color=="white"):
            self.setImage("Rook.PNG") 
        elif (self.color=="black"):
            self.setImage("BlackRook.PNG")
        Rook.allRooks +=[self]
    def __repr__(self):
        if self.color=="white":
            return ("R@%s" %(str(self.location))) 
        else: return ("r@%s" %(str(self.location))) 
                
class Queen(ChessPiece):
    allQueens=[]
    def __init__(self, color, location):
        pieceValue=9
        super().__init__(pieceValue,color,location)
        if (self.color=="white"):
            self.setImage("Queen.PNG") 
        elif (self.color=="black"):
            self.setImage("BlackQueen.PNG") 
        Queen.allQueens += [self]
    def __repr__(self):
        if self.color=="white":
            return ("Q@%s" %(str(self.location))) 
        else: return ("q@%s" %(str(self.location))) 
            
        
        
class King(ChessPiece):
    allKings=[]
    def __init__(self, color, location):
        pieceValue=104 #1 more point than highest total piece value of other pieces
        super().__init__(pieceValue,color,location)
        if (self.color=="white"):
            self.setImage("King.PNG") 
        elif (self.color=="black"):
            self.setImage("BlackKing.PNG") 
        King.allKings += [self]
    def __repr__(self):
        if self.color=="white":
            return ("K@%s" %(str(self.location))) 
        else: return ("k@%s" %(str(self.location))) 
            
        
        
####################################
# Basic functions
####################################

def init(data): #Original init taken from Week 6 HW and then adapted
    data.width=1230 
    data.height=690
    data.movingwidth=data.width//2
    data.hCol=None
    data.hRow=None
    data.hCol2=None
    data.hRow2=None
    data.whitePiecesCaptured=[]
    data.blackPiecesCaptured=[]
    data.whitePointsLost=0
    data.blackPointsLost=0
    data.placeholderwhitePointsLost=0
    data.placeholderblackPointsLost=0
    data.placeholderwhitePiecesCaptured=[]
    data.placeholderblackPiecesCaptured=[]
    data.hSquares=[]
    rows,cols=8,8 #Dimensions of a Chess Board
    data.timer1= 600000 #miliseconds for 10 minutes
    data.timer2= 600000 #miliseconds for  minutes
    data.rows=rows
    data.cols=cols
    data.CurR=data.rows//2
    data.CurC=data.cols//2 
    data.cellSize=75    
    boardcolor=["#779559","#eeeed3"]
    data.boardcolor=boardcolor
    data.CurC=data.cols//2
    data.CurR=data.rows//2
    data.dimensions= 600
    data.x=data.CurC*data.dimensions-data.width//2
    data.y=data.CurR*data.dimensions-data.height//2
    data.gameOver=False
    data.undoboard=[]
    data.mode=0
    data.xcentering= 260
    data.ycentering=40
    data.textsize = 45
    data.textsize2 = 20
    data.textsize3 = 30
    data.turn= "white"
    data.engine=False
    data.winner = None
    data.currentPiece=None    
    data.one=1
    data.two=2
    data.three=3
    data.four=4
    data.five=5
    data.six=6
    data.seven=7
    data.eight=8
    data.pawn = Pawn("black",(0,1))
    data.pawn2 = Pawn("black",(1,1))
    data.pawn3 = Pawn("black",(2,1))
    data.pawn4 = Pawn("black",(3,1))
    data.pawn5 = Pawn("black",(4,1))
    data.pawn6 = Pawn("black",(5,1))
    data.pawn7 = Pawn("black",(6,1))
    data.pawn8 = Pawn("black",(7,1))
    data.pawn9 = Pawn("white",(0,6))
    data.pawn10 = Pawn("white",(1,6))
    data.pawn11 = Pawn("white",(2,6))
    data.pawn12 = Pawn("white",(3,6))
    data.pawn13 = Pawn("white",(4,6))
    data.pawn14 = Pawn("white",(5,6))
    data.pawn15 = Pawn("white",(6,6))
    data.pawn16 = Pawn("white",(7,6))
    data.king = King("black", (4,0))
    data.king1 = King("white", (4,7))
    data.queen1 = Queen("white", (3,7))
    data.queen = Queen("black", (3,0))
    data.knight = Knight("white", (1,7))
    data.knight2 = Knight("black", (1,0))
    data.knight3 = Knight("black", (6,0))
    data.knight4 = Knight("white", (6,7))
    data.bishop = Bishop("white", (2,7))
    data.bishop2 = Bishop("white", (5,7)) 
    data.bishop3 = Bishop("black", (5,0))
    data.bishop4 = Bishop("black", (2,0))
    data.rook = Rook("white", (0,7))
    data.rook2 = Rook("white", (7,7))
    data.rook3 = Rook("black", (7,0))
    data.rook4 = Rook("black", (0,0))
    data.image=setImage(file='Background.PNG')
    data.whitepawn=setImage(file='Pawn.PNG')
    data.blackpawn=setImage(file='BlackPawn.PNG')
    data.whiteknight=setImage(file='Knight.PNG')
    data.blackknight=setImage(file='BlackKnight.PNG')
    data.whitebishop=setImage(file='Bishop.PNG')
    data.blackbishop=setImage(file='BlackBishop.PNG')
    data.whiterook=setImage(file='Rook.PNG')
    data.blackrook=setImage(file='BlackRook.PNG')
    data.whitequeen=setImage(file='Queen.PNG')
    data.blackqueen=setImage(file='BlackQueen.PNG')
    data.whiteking=setImage(file='King.PNG')
    data.blackking=setImage(file='BlackKing.PNG')
    data.movecounter=0
    data.CheckMate=False
    data.board = [[data.rook4,data.knight2,data.bishop3,data.queen,data.king,data.bishop4,data.knight3,data.rook3],
    [data.pawn,data.pawn2,data.pawn3,data.pawn4,data.pawn5,data.pawn6,data.pawn7,data.pawn8],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    [data.pawn9,data.pawn10,data.pawn11,data.pawn12,data.pawn13,data.pawn14,data.pawn15,data.pawn16],
    [data.rook,data.knight,data.bishop,data.queen1,data.king1,data.bishop2,data.knight4,data.rook2]]
    data.setupBoard = [["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"]]
    data.moveList=[[[data.rook4,data.knight2,data.bishop3,data.queen,data.king,data.bishop4,data.knight3,data.rook3],
    [data.pawn,data.pawn2,data.pawn3,data.pawn4,data.pawn5,data.pawn6,data.pawn7,data.pawn8],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    [data.pawn9,data.pawn10,data.pawn11,data.pawn12,data.pawn13,data.pawn14,data.pawn15,data.pawn16],
    [data.rook,data.knight,data.bishop,data.queen1,data.king1,data.bishop2,data.knight4,data.rook2]]]
    data.startingboard=[[[data.rook4,data.knight2,data.bishop3,data.queen,data.king,data.bishop4,data.knight3,data.rook3],
    [data.pawn,data.pawn2,data.pawn3,data.pawn4,data.pawn5,data.pawn6,data.pawn7,data.pawn8],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0"],
    [data.pawn9,data.pawn10,data.pawn11,data.pawn12,data.pawn13,data.pawn14,data.pawn15,data.pawn16],
    [data.rook,data.knight,data.bishop,data.queen1,data.king1,data.bishop2,data.knight4,data.rook2]]]

def pieceIdentifier(file,rank,data):
    given=(file,rank)
    for piece in Pawn.allPawns:
        if given == piece.location:  
            return piece
    for piece in Knight.allKnights:
        if given == piece.location:  
            return piece
    for piece in Bishop.allBishops:
        if given == piece.location:  
            return piece
    for piece in Rook.allRooks:
        if given == piece.location:  
            return piece
    for piece in Queen.allQueens:
        if given == piece.location:  
            return piece
    for piece in King.allKings:
        if given == piece.location:  
            return piece

def mousePressed(event, data):
    if data.mode==1:
        x,y=coordinateconverter(event.x,event.y,data)
        if data.currentPiece==None:
            if len(data.hSquares)!=0:
                data.hSquares=[]
            data.oldx,data.oldy=x,y
            data.currentPiece=pieceIdentifier(x,y,data) 
            data.hSquares.append((data.oldx,data.oldy))                    
        else:
            oldlocation=(data.oldx,data.oldy)
            data.board[data.oldx][data.oldx]#Highlight piece being selected
            location=(x,y)
            data.hSquares.append(location)
            print("DATA. CURRENTPIECE", data.currentPiece, type(data.currentPiece))
            if (data.currentPiece.isMoveLegal(oldlocation,                                  
                            location,data.turn,data.currentPiece,data.board))==True:
                oldpiece=data.board[oldlocation[1]][oldlocation[0]]
                currentPiece = data.board[location[1]][location[0]]
                data.board[location[1]][location[0]]="0"
                data.board[location[1]][location[0]]=oldpiece
                data.board[oldlocation[1]][oldlocation[0]]="0"
                data.currentPiece=oldpiece
                print("DATA. CURRENTPIECE", data.currentPiece,type(data.currentPiece))
                if data.currentPiece.isKinginTrouble(data.board,data.turn)==True: 
                    data.board[oldlocation[1]][oldlocation[0]]=oldpiece
                    data.board[location[1]][location[0]]=currentPiece
                    data.currentPiece.location=(data.oldx,data.oldy)
                    data.currentPiece=None

                else: 
                    if data.placeholderwhitePiecesCaptured!=[] or data.placeholderblackPiecesCaptured!=[]:
                        data.placeholderwhitePiecesCaptured=[]
                        data.placeholderblackPiecesCaptured=[]
                        data.placeholderblackPointsLost=0
                        data.placeholderwhitePointsLost=0
                    if data.undoboard!=[]: data.undoboard=[]
                    if currentPiece!="0": 
                        if currentPiece.color =="white":
                            data.whitePiecesCaptured.append(currentPiece)
                            data.whitePointsLost+=currentPiece.pieceValue
                        else:
                            data.blackPiecesCaptured.append(currentPiece)
                            data.blackPointsLost+=currentPiece.pieceValue
                    print("DATA. CURRENTPIECE", data.currentPiece,type(data.currentPiece))

                    boardcopy= make2dList(8,8)
                    for i in range(len(data.board)):
                        for j in range(len(data.board)):
                            boardcopy[i][j]=data.board[i][j]
        
                    if data.turn=="white": data.turn="black"
                    else: data.turn="white"
                data.currentPiece.location=(x,y)
                data.currentPiece=None 
                data.moveList.append(boardcopy)
            data.currentPiece=None
       
        print (event.x,event.y)
        print ("coordinate converter x and y:", coordinateconverter(event.x,event.y,data))
        print ("WATCH ALL OF THIS RIGHT NOW")
        print('white placeholder',data.placeholderwhitePiecesCaptured)
        print ('black placeholder',data.placeholderblackPiecesCaptured)
        print ('white captured list',data.whitePiecesCaptured)
        print ('black captured list',data.blackPiecesCaptured)
        print('white points',data.whitePointsLost)
        print ('black points',data.blackPointsLost)
        print ('white placer points', data.placeholderwhitePointsLost)
        print ('black placeholder points',data.placeholderblackPointsLost)
        
        
def readFile(path): #15-112 Website
    with open(path, "rt") as f:
        return f.read()
        
def saveChessgame(path,games):
    with open(path, "wt") as f:
        f.write(games)

def make2dList(rows, cols): #15-112 website
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a
    
def keyPressed(event, data):
    if data.mode==0:
        if event.keysym in "Pp": data.mode=1
        elif event.keysym in "Aa": data.mode=2
        elif event.keysym in "Dd": data.mode=3
    if event.keysym in "Hh": init(data)
    if data.mode==1:
        if event.keysym =='n':
            init(data)
            data.mode=1
            print("THIS IS WORKING",data.mode)
        if event.keysym =='g':
            print ("WATCH ALL OF THIS RIGHT NOW")
            print('white placeholder',data.placeholderwhitePiecesCaptured)
            print ('black placeholder',data.placeholderblackPiecesCaptured)
            print ('white captured list',data.whitePiecesCaptured)
            print ('black captured list',data.blackPiecesCaptured)
            print('white points',data.whitePointsLost)
            print ('black points',data.blackPointsLost)
            print ('white placer points', data.placeholderwhitePointsLost)
            print ('black placeholder points',data.placeholderblackPointsLost)
        if event.keysym == "Left":            
            print(len(data.moveList))
            if len(data.moveList)>1:
                print(data.undoboard)
                print(data.moveList)
                data.undoboard.append(data.moveList.pop())
                data.movecounter-=1
                data.board=data.moveList[-1]
                if data.turn=="white":
                    data.turn="black"
                else: data.turn="white"
                for piece in data.whitePiecesCaptured:
                    if piece in data.board: 
                        data.whitePiecesCaptured.remove(piece)
                        data.placeholderwhitePiecesCaptured.append(piece)
                        data.WhitePointsLostholder-=piece.pieceValue
                        data.placerholderWhitePointsLostholder+=piece.pieceValue
                        print (piece)
                        print(piece in data.board)
                for piece in data.blackPiecesCaptured:
                    if piece in data.board: 
                        data.blackPiecesCaptured.remove(piece)
                        data.placeholderblackPiecesCaptured.append(piece)
                        data.BlackPointsLostholder-=piece.pieceValue
                        data.placerholderBlackPointsLostholder+=piece.pieceValue
                
                if data.movecounter==0:
                    data.board=data.startingboard
                print2dList(data.undoboard)
                boardcopy= make2dList(8,8)
                for i in range(len(data.board)):
                   for j in range(len(data.board)):
                       boardcopy[i][j]=data.moveList[-1][i][j]
                print("move list", data.moveList[-1])
            if len(data.moveList)==0: datamoveList=data.board
        if event.keysym == "Right":
            if len(data.undoboard)>0:
                data.moveList.append(data.undoboard.pop())
                data.movecounter+=1
                if data.turn=="white":
                    data.turn="black"
                else: data.turn="white"
                boardcopy= make2dList(8,8)
                for i in range(len(data.board)):
                    for j in range(len(data.board)):
                        boardcopy[i][j]=data.moveList[-1][i][j]
                data.board=boardcopy
                for piece in data.placeholderwhitePiecesCaptured:
                    if piece not in data.board: 
                        data.placeholdewhitePiecesCaptured.remove(piece)
                        data.whitePiecesCaptured.append(piece)
                        data.placeholderWhitePointsLost-=piece.pieceValue
                        data.WhitePointsLostholder+=piece.pieceValue
                for piece in data.placeholderblackPiecesCaptured:
                    if piece not in data.board: 
                        data.placeholderblackPiecesCaptured.remove(piece)
                        data.blackPiecesCaptured.append(piece)
                        data.placeholderBlackPointsLostholder-=piece.pieceValue
                        data.BlackPointsLostholder+=piece.pieceValue
        if event.keysym =="k":
            return data.currentPiece.isKinginTrouble(data.board,color=data.turn)    
        if event.keysym =="z":
            print(print2dList(data.board))
        if event.keysym =="p":
            if data.turn =="white":
                data.timer1=data.timer1+data.timerDelay #pauses game
                if event.keysym =="p":
                    data.timer1-=1000 #continues timer
            if data.turn =="black":
                data.timer2=data.timer2 #pauses game
                if event.keysym =="p":
                    data.timer2-=1000 #continues timer
        if event.keysym== "m" or event.keysym== "Tab":
            if data.turn=="black": data.winner="White"
            else: data.winner="Black"
            data.mode=5
        if event.keysym =="e":
            if data.engine==False: data.engine=True
            else: data.engine=False
        if event.keysym == "m":
            if data.turn=="black": data.winner="white"
            else: data.winner="black"
            data.mode=5
    if data.mode ==2:
        if event.keysym =="w":
            data.turn ="white"
        if event.keysym =="b":
            data.turn ="black"
    if data.mode==5:
        if event.keysym =="n":
            data.mode=1
def ScoreKeeper(canvas,data):
    Score=-(data.whitePointsLost-data.blackPointsLost)
    return Score
    #Positive means White is winning, Negative means black is winning
    
def timerFired(data):
    if data.turn=="white":
        data.timer1-=data.timerDelay
    if data.turn=="black":
        data.timer2-=data.timerDelay
    if data.timer1==0:
        data.winner= "Black"
        data.mode=5
    elif data.timer2==0:
        data.winner = "White"
        data.mode=5

def coordinateconverter(x,y,data):
    newx=(x-data.xcentering)//data.cellSize
    newy=(y-data.ycentering)//data.cellSize
    return newx,newy

def drawPieces(canvas,data):
    for row in range(len(data.board)):
        for col in range(len(data.board[0])):
            piece=data.board[row][col]
            if piece!="0":
                piece.drawPiece(canvas,data,row,col)
    
def drawBackground(canvas,data): 
    x1 = 0
    x2 = data.width
    y1 = 0
    y2 = data.height
    canvas.create_rectangle(x1, y1,x2, y2,fill="#312e2b")
    
def drawstart(canvas,data):
    msg1 = "Click P to Play Game"
    msg2 = "Setup Position [A]"
    msg3 = "Game Database [D]"
    msg4 = "The Chess Mentor"
    homesize = "Avenir %d bold", data.textsize
    homesize2 = "Avenir %d bold", data.textsize2
    (canvas.create_text(data.width//2 +20, data.height//2-40,font=homesize,
    text=msg4,fill= "black"))  
    (canvas.create_text(data.width//2 +30, data.height//2,font=homesize2,
    text=msg1,fill= "white"))
    (canvas.create_text(data.width//2 +30, data.height//2+20,font=homesize2,
    text=msg2,fill= "white"))
    (canvas.create_text(data.width//2 +30, data.height//2+40,font=homesize2,
    text=msg3,fill= "white")) 
            
def drawboard(canvas,data): 
    for row in range(data.rows): 
        if(row%2):
            Counter = 0
        else: 
            Counter=1
        for col in range(data.cols):
            specialfill = Counter%2 #Condition that allow colors to alternate
            canvas.create_rectangle(row*data.cellSize+data.xcentering,
            col*data.cellSize+data.ycentering,(row+1)
            *data.cellSize+data.xcentering,(col+1)*data.cellSize+data.ycentering,
            width=0,fill=data.boardcolor[specialfill]) #Creates board, adds color
            if (row,col) in data.hSquares:
                canvas.create_rectangle(row*data.cellSize+data.xcentering, col*data.cellSize+data.ycentering,(row+1) *data.cellSize+data.xcentering,(col+1)*data.cellSize+data.ycentering,fill="yellow")
                
            Counter+=1
    size = "Calibri %d bold", data.textsize2
    size2 = "Calibri %d bold", data.textsize
    msg= "       a            b           c           d           e            f            g           h "
    msg2= "CHECK!"
    msg3=ScoreKeeper(canvas,data)
    canvas.create_text(col*data.cellSize+20, row*data.cellSize+data.ycentering+90,font=size, text= msg, fill="white")
    canvas.create_text(col*data.cellSize-280, row*data.cellSize+data.ycentering+40,font=size, text=data.one, fill="white")
    canvas.create_text(col*data.cellSize-280, row*data.cellSize+data.ycentering-40,font=size, text=data.two, fill="white")
    canvas.create_text(col*data.cellSize-280, row*data.cellSize+data.ycentering-115,font=size, text=data.three, fill="white")
    canvas.create_text(col*data.cellSize-280, row*data.cellSize+data.ycentering-185,font=size, text=data.four, fill="white")
    canvas.create_text(col*data.cellSize-280, row*data.cellSize+data.ycentering-260,font=size, text=data.five, fill="white")
    canvas.create_text(col*data.cellSize-280, row*data.cellSize+data.ycentering-340,font=size, text=data.six, fill="white")
    canvas.create_text(col*data.cellSize-280, row*data.cellSize+data.ycentering-415,font=size, text=data.seven, fill="white")
    canvas.create_text(col*data.cellSize-280, row*data.cellSize+data.ycentering-490,font=size, text=data.eight, fill="white")
    
    if data.currentPiece!=None: 
        if data.currentPiece.isKinginTrouble(data.board,data.turn)==True: canvas.create_text(col*data.cellSize-400, row*data.cellSize+data.ycentering-490,font=size2, text=msg2, fill="red")
    if data.engine==True:
        canvas.create_text(col*data.cellSize-400, row*data.cellSize+data.ycentering-290,font=size2, text=msg3, fill="white")

def setImage(file=None):  
    #http://pillow.readthedocs.io/en/3.4.x/reference/Image.html
    pillowImage=Image.open(file)
    size= 1000,600
    pillowImage.resize(size)
    image = ImageTk.PhotoImage(pillowImage)
    return image

def stringconverter(x,y,data):
    if x==0:file=a
    elif x==1:file=b
    elif x==2:file=c
    elif x==3:file=d
    elif x==4:file=e
    elif x==5:file=f
    elif x==6:file=g
    elif x==7:file=h
    
    if y==0:row=8
    elif y==1:row=7
    elif y==2:file=6
    elif y==3:file=5
    elif y==4:file=4
    elif y==5:file=3
    elif y==6:file=2
    elif y==7:file=1
    return str(rank)+str(file)

def piecelist(canvas,data):
    print("here")
    canvas.create_image(10,10,image=data.whitepawn)

def drawPieceShower(canvas,data):
    canvas.create_rectangle(data.cols*data.cellSize+320, 
    data.rows*data.cellSize+40,(data.cols+1)*data.cellSize +520,(data.rows+1)*data.cellSize-625,width=0,fill="#eeeed3")

def drawImageScreen(canvas,data):
    canvas.create_image(data.width//2,data.height//2, image=data.image)
    
def drawtext(canvas,data):
    size = "Calibri %d bold", data.textsize2
    # Piece=first index
    # x=third index
    # y=fourth index 
    # str(data.currentPiece):
    canvas.create_text(125,350,font=size, text="Selected Piece:"+str(data.currentPiece),fill="white")

def coordinateinterpreter(canvas,data):
    rowvalue=data.currentPiece[0] 
    columnvalue=data.currentPiece[1]
    row=rowconverter(canvas, rowvalue,data)
    col=columnconverter(canvas,columnvalue,data)
    
def rowconverter(canvas,row,data):
    if row==0: return 'a'
    if row==1: return 'b'
    if row==2: return 'c'
    if row==3: return 'd'
    if row==4: return 'e'
    if row==5: return 'f'
    if row==6: return 'g'
    if row==7: return 'h'

def columnconverter(canvas, col,data):
    if column==0: return '8'
    if column==1: return '7'
    if column==2: return '6'
    if column==3: return '5'
    if column==4: return '4'
    if column==5: return '3'
    if column==6: return '2'
    if column==7: return '1'
    
def drawPlayerturn(canvas,data):
    whitecaptured= "WHITE PIECES:"
    whitelist=str(data.whitePiecesCaptured)
    blackcaptured="BLACK PIECES:"
    blacklist= str(data.blackPiecesCaptured)
    canvas.create_rectangle(data.cols*data.cellSize+320, 
    data.rows*data.cellSize+40,(data.cols+1)*data.cellSize +520,(data.rows+1)*data.cellSize-625,width=0,fill="#eeeed3")
    homesize4 =  "Arial %d bold", data.textsize2
    homesize3 = "Arial %d bold", data.textsize3
    canvas.create_text(data.cols*data.cellSize+460, data.rows*data.cellSize+5,font=homesize3,text="REDO MOVE (->)",fill="black")
    canvas.create_line(data.cols*data.cellSize+320, data.rows*data.cellSize-30,(data.cols+1)*data.cellSize +520,(data.rows+1)*data.cellSize-105,width=2.5,fill="black")
    canvas.create_text(data.cols*data.cellSize+460, data.rows*data.cellSize-65,font=homesize3,text="UNDO MOVE (<-)",fill="black")
    canvas.create_line(data.cols*data.cellSize+320, data.rows*data.cellSize-100,(data.cols+1)*data.cellSize +520,(data.rows+1)*data.cellSize-175,width=2.5,fill="black")
    canvas.create_text(data.cols*data.cellSize+460, data.rows*data.cellSize-135,font=homesize3,text="NEW GAME (N)",fill="black")
    canvas.create_line(data.cols*data.cellSize+320, data.rows*data.cellSize-165,(data.cols+1)*data.cellSize +520,(data.rows+1)*data.cellSize-240,width=2.5,fill="black")
    canvas.create_text(data.cols*data.cellSize+460, data.rows*data.cellSize-205,font=homesize3,text="GAME ENGINE (E)",fill="black")
    canvas.create_line(data.cols*data.cellSize+320, data.rows*data.cellSize-232,(data.cols+1)*data.cellSize +520,(data.rows+1)*data.cellSize-305,width=2.5,fill="black")
    canvas.create_text(data.cols*data.cellSize+460, data.rows*data.cellSize-400,font=homesize3,text=whitecaptured,fill="black")
    canvas.create_text(data.cols*data.cellSize+460, data.rows*data.cellSize-370,font=homesize4,text=whitelist,fill="black")
    canvas.create_text(data.cols*data.cellSize+460, data.rows*data.cellSize-315,font=homesize3,text=blackcaptured,fill="black")
    canvas.create_text(data.cols*data.cellSize+460, data.rows*data.cellSize-290,font=homesize4,text=blacklist,fill="black")

def timer(canvas,data):  
    min=data.timer1//60000
    seconds=(data.timer1//1000)%60
    font= "Arial %d bold", data.textsize3
    if seconds<10:
        text1 = "White    "+str(min)+":0"+str(seconds)
    else: text1 = "White   "+str(min)+":"+str(seconds)
    canvas.create_text(data.cols*data.cellSize+450,data.rows*data.cellSize-525,font=font,text=text1)
    min2=data.timer2//60000
    sec2= (data.timer2//1000)%60
    if sec2<10:
        text2= "Black   "+str(min2)+":0"+str(sec2)
    else:
        text2= "Black   "+str(min2)+":"+str(sec2)
    canvas.create_text(data.cols*data.cellSize+450,data.rows*data.cellSize-475,font=font,text=text2)
    canvas.create_line(data.cols*data.cellSize+320, data.rows*data.cellSize-432,(data.cols+1)*data.cellSize +520,(data.rows+1)*data.cellSize-506,width=2.5,fill="black") 

def drawGameOver(canvas,data):
    msg = "Game Over"
    msg2 = "%s Wins" %(data.winner)
    msg3 = "Click H to return to the home screen"
    size = "Calibri %d bold", data.textsize
    size2 = "Calibri %d bold", data.textsize2
    (canvas.create_text(data.width//2, data.height//2, font=size, fill = "white", text= msg))
    (canvas.create_text(data.width//2, data.height//2+40, font = size2, fill ="white", text=msg2))
    (canvas.create_text(data.width//2, data.height//2+80, font = size2, fill = "white", text=msg3))


def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen
    
def print2dList(a): #15-112 Website 
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")
    
def redrawAll(canvas, data):
    if data.mode==0:
        drawBackground(canvas,data)
        drawImageScreen(canvas,data)
        drawstart(canvas,data)
        
    if data.mode==1:
        drawBackground(canvas,data)
        drawboard(canvas,data)
        drawPieces(canvas, data)
        drawtext(canvas,data)
        drawPlayerturn(canvas,data)
        timer(canvas,data)
                
    if data.mode==2:
        drawBackground(canvas,data)
        drawboard(canvas,data)
        drawPieceShower(canvas,data)
        drawtext(canvas,data)
        piecelist(canvas,data)
                
    if data.mode==4:
        drawBackground(canvas,data)
        drawboard(canvas,data)
        init(data)
        drawPieces(canvas, data)    
    
    if data.mode==5:
        drawBackground(canvas,data)
        drawGameOver(canvas,data)
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    data.root = root
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    init(data)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
                            
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

def flattenAlpha(img): #from http://stackoverflow.com/questions/41576637/are-rgba-pngs-unsupported-in-python-3-5-pillow
    alpha = img.split()[-1]  # Pull off the alpha layer
    ab = alpha.tobytes()  # Original 8-bit alpha

    checked = []  # Create a new array to store the cleaned up alpha layer bytes

    # Walk through all pixels and set them either to 0 for transparent or 255 for opaque fancy pants
    transparent = 50  # change to suit your tolerance for what is and is not transparent

    p = 0
    for pixel in range(0, len(ab)):
        if ab[pixel] < transparent:
            checked.append(0)  # Transparent
        else:
            checked.append(255)  # Opaque
        p += 1

    mask = Image.frombytes('L', img.size, bytes(checked))

    img.putalpha(mask)

    return img
run(1230,690)
