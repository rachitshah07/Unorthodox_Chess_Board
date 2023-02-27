#!/usr/bin/env python
import sys, os
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter.messagebox import *
SCALING_FACTOR = 50
OFFSET_FACTOR = 0.5
# Actual value
BOARD_SIZE = None
## Dictionary to store the widget information
widgetInfoDict = {}
# widgetInfoDict {  "root" : <root widget object (main window")>,
#                   "pw"    : <reference to paned window inside the top (horizontal)>,
#                   "lf1"   : <reference to label_frame1 inside the horizontal paned window>
#                   "lf2"   : <reference to label_frame2 inside the horizontal paned window>
#                   "text"  : <reference to text widget inside the label_frame1>,
#                   "canvas"  : <reference to canvas widget inside the label_frame1>,
#               }

## Dictionary to store piece info
pieceInfoDict = {}
black={
        "Origin":[0,0]
    }
# pieceInfoDict {  "<piece_1>" : [<x_cord> , <y_cord>],
#                   "<piece_2>" : [<x_cord> , <y_cord>]
#               }


## Function to create the toplevel window, text and canvas widget
#
def createEditor(fileContents):
    # main tkinter window
    widgetInfoDict["root"] = Tk()
    widgetInfoDict["root"].geometry(str(widgetInfoDict["root"].winfo_screenwidth()) + 'x' + str(
        int(widgetInfoDict["root"].winfo_screenheight() * 0.9)))

    # panedwindow object
    widgetInfoDict["pw"] = PanedWindow(widgetInfoDict["root"], orient='horizontal')

    widgetInfoDict["lf1"] = LabelFrame(widgetInfoDict["root"], text='Editor', width=500)
    widgetInfoDict["lf1"].pack(expand='yes', fill=BOTH)

    widgetInfoDict["lf2"] = LabelFrame(widgetInfoDict["root"], text='Canvas', width=500)
    widgetInfoDict["lf2"].pack(expand='yes', fill=BOTH)


    widgetInfoDict["text"] = Text(widgetInfoDict["lf1"])
    widgetInfoDict["text"].pack(fill=BOTH, expand=True)
    
    widgetInfoDict["canvas"] = Canvas(widgetInfoDict["lf2"],scrollregion=(0, 0, 2000, 2000))
    widgetInfoDict["canvas"].pack(side=LEFT, fill=BOTH, expand=True)


    def get_image(filename,x,y):
        img = Image.open(filename).resize((60-x, 60-y), Image.LANCZOS)
        return ImageTk.PhotoImage(img)


    #Zoom-In Zoom-Out
    def do_zoom(event):
        x = widgetInfoDict["canvas"].canvasx(event.x)
        y = widgetInfoDict["canvas"].canvasy(event.y)
        factor = 1.001 ** event.delta
        # widgetInfoDict["canvas"].scale(ALL, x, y, factor, factor)
        is_shift = event.state & (1 << 0) != 0
        is_ctrl = event.state & (1 << 2) != 0
        widgetInfoDict["canvas"].scale(ALL, x, y, factor if not is_shift else 1.0, factor if not is_ctrl else 1.0)

        # widgetInfoDict["canvas"].create_image(x * SCALING_FACTOR, y * SCALING_FACTOR, image=img, tags=shape)
        # # widgetInfoDict.tag_bind(img,"<Button-3>")
        # img_ref.append(img)

    widgetInfoDict["canvas"].bind("<MouseWheel>",do_zoom)
    widgetInfoDict["canvas"].bind('<ButtonPress-1>', lambda event: widgetInfoDict["canvas"].scan_mark(event.x, event.y))
    widgetInfoDict["canvas"].bind("<B1-Motion>", lambda event: widgetInfoDict["canvas"].scan_dragto(event.x, event.y, gain=1))
    

    #SCROLLBAR
    yscroll = ttk.Scrollbar(widgetInfoDict["root"], orient=VERTICAL, command=widgetInfoDict["canvas"].yview)
    yscroll.pack(side=RIGHT, fill=Y)
    widgetInfoDict["canvas"].config(yscrollcommand=yscroll.set)
    xscroll = ttk.Scrollbar(widgetInfoDict["root"], orient=HORIZONTAL, command=widgetInfoDict["canvas"].xview)
    xscroll.pack(side=BOTTOM, fill=X)
    widgetInfoDict["canvas"].config(xscrollcommand=xscroll.set)
    widgetInfoDict["canvas"].pack()

   
    widgetInfoDict["canvas"].pack()
    widgetInfoDict["canvas"].pack(fill=BOTH, expand=True)

 
    widgetInfoDict["pw"].add(widgetInfoDict["lf1"])
    widgetInfoDict["pw"].add(widgetInfoDict["lf2"])
    widgetInfoDict["pw"].pack(fill=BOTH, expand=True)
    widgetInfoDict["pw"].configure(sashrelief=RAISED)

    renderBoard(BOARD_SIZE,data)
    # widgetInfoDict["text"].insert(END, fileContents)
    # placeSequence()
    btn = Button(widgetInfoDict["lf1"], text='Evaluate', bd='5', command=placeSequence)
    btn.pack(side='bottom')
    widgetInfoDict["text"].insert(END, fileContents)
    widgetInfoDict["root"].mainloop()


## Function to read the data from sequence cmds (placeSequence.txt) file and write to the text editor
#
#   @param placementSwqCmdsFile : Reference to the area.txt file path
#
def readData(placmntSeqCmdsFile):
    with open(placmntSeqCmdsFile, 'r') as cmdFileObj:
        fileContents = cmdFileObj.read()
        # widgetInfoDict["text"].insert(END, fileContent)
        return fileContents


img_ref = []


def renderPiece(x, y, shape):
    if (x >= BOARD_SIZE or y >= BOARD_SIZE or x<0 or y<0):
        print(shape,    "with", "coordinates: (",x,",",y,") is placed OUT OF THE CHESS BOARD!")
        print(showerror("showerror", (shape,"with coordinates: (",x,",",y,") is placed OUT OF THE CHESS BOARD!")))
    else:
        x, y = x + 0.5, y + 0.5
        shapeImage = shape.split('_')
        img = ImageTk.PhotoImage(Image.open(f"ChessPieces{os.sep}{shapeImage[0]}.png"))
        widgetInfoDict["canvas"].create_image(x * SCALING_FACTOR, y * SCALING_FACTOR, image=img, tags=shape)
        img_ref.append(img)

## Function to draw the board on the canvas
#
#   @param boardSize : integer number.
#
def renderBoard(boardSize,data):
    renderRectangle([0, 0, boardSize, boardSize], "board")
    for n in range(boardSize):
        renderLine([n, 0, n, boardSize])
        renderLine([0, n, boardSize, n])
    list_obj=data.splitlines()
    t=[]
    for i in range(1,len(list_obj)):
        temp=list_obj[i].split()
        if(len(temp)>0):
            t.append(temp);

    # print(t)
    # print(len(t))
    for i in t:
        # print(i)
        # print(black[i[1]][0])
        # snake_ladder[i[0]]
        black[i[0]]=[int(black[i[1]][0])+int(i[2]),int(black[i[1]][1])+int(i[3])]
    # print(black)

    for i in black:
        if(i!="Origin"):
            renderPiece(black[i][0],black[i][1],i)
    return



## Function to draw the rectangle on the canvas using the coordinates
#
#   @param coord : tuple with lower left and upper right coordinates
#   @param name : Reference to the shape name
#
# Info : In tkinter, rectangle/square can be drawn by passing the lower left and upper right coordinates, ex: to draw a
# 5(l), 7(b) rectangle from origin, coordinates are (0,0) and (5,7)
#
def renderRectangle(coords, name=None):
    coords = [coord * SCALING_FACTOR for coord in coords]
    coordref = widgetInfoDict["canvas"].create_rectangle(coords[0], coords[1], coords[2], coords[3], tags=name)
    # ref 'coordref' can be used to print the coordinates of the rendered name, i.e.
    # print(widgetInfoDict["canvas"].coords(coordref))
    # Add the shape name to the rendered name
    if name:
        widgetInfoDict["canvas"].create_text((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2, text=name,
                                             tags=name)


## Function to draw a line on the canvas using the coordinates
#
#   @param coord : [x1, y1, x2, y2]
#   @param color : Color of the line
#   @param name :  Reference to the line name
#
def renderLine(coords, color="black", name=None):
    coords = [coord * SCALING_FACTOR for coord in coords]
    coordref = widgetInfoDict["canvas"].create_line(coords[0], coords[1], coords[2], coords[3], fill=color, tags=name)
    # ref 'coordref' can be used to print the coordinates of the rendered name, i.e.
    # print(widgetInfoDict["canvas"].coords(coordref))
    # Add the shape name to the rendered name
    if name:
        widgetInfoDict["canvas"].create_text((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2, text=name,
                                             tags=name)


## Function to delete shape
#
#   @param tag : Tag of the shape to be deleted
#
def deleteShape(tag):
    widgetInfoDict["canvas"].delete(tag)


## Function to delete multiple shapes
#
#   @param tags : List of tag of the shapes to be deleted
#
def deleteShapes(tags):
    widgetInfoDict["canvas"].delete(*tags)


## Function to read the coordinate information from the file
#
#   @param pieceInfoFile : Reference to the pieceInfoFile path
#
def readPieceInfoFromFile(pieceInfoFile):
    with open(pieceInfoFile, 'r') as pieceFileObj:
        for line in pieceFileObj:
            dataLst = line.split()
            if len(dataLst) != 3:
                print("Couldn't process the line " + line + " in " + str(
                    pieceInfoFile) + "due to missing of information. Format is '<piece_name> <x_cord> <y_cord>', "
                                     "hence skipping this line")
                continue
            pieceInfoDict[dataLst[0]] = [int(dataLst[1]), int(dataLst[2])]

# Our Algo
def valid(x,y):
    if(x>=0 and y>=0 and x<=BOARD_SIZE and y<=BOARD_SIZE):
        return True
    return False

def validate(x):
    if(x>=0 and x<=BOARD_SIZE ):
        return True
    return False

def pawn(pawnx,pawny,wkingx,wkingy):
    if((validate(pawnx+1) and validate(pawny+1)) or (validate(pawnx-1) and validate(pawny+1))):
        if((pawnx+1==wkingx and pawny+1==wkingy) or (pawnx-1==wkingx and pawny+1==wkingy)):
            return False
    return True
    
def kinght(bishopx,bishopy,wkingx,wkingy):
    if((validate(bishopx+1) and validate(bishopy-2)) or (validate(bishopx-1) and validate(bishopy-2)) or (validate(bishopx+1) and validate(bishopy+2)) or (validate(bishopx-1) and validate(bishopy+2)) or (validate(bishopx-2) and validate(bishopy+1)) or (validate(bishopx-2) and validate(bishopy-1)) or (validate(bishopx+2) and validate(bishopy+1)) or (validate(bishopx+2) and validate(bishopy-1))):
        if(((bishopx+1==wkingx) and (bishopy-2==wkingy)) or ((bishopx-1==wkingx) and (bishopy-2==wkingy)) or ((bishopx+1==wkingx) and (bishopy+2==wkingy)) or ((bishopx-1==wkingx) and (bishopy+2==wkingy)) or ((bishopx-2==wkingx) and (bishopy+1==wkingy)) or ((bishopx-2==wkingx) and (bishopy-1==wkingy)) or ((bishopx+2==wkingx) and (bishopy+1==wkingy)) or ((bishopx+2==wkingx) and (bishopy-1==wkingy))):
            return False
    return True
    
def king(kingx,kingy,wkingx,wkingy):
    if((validate(kingx+1) and validate(kingy-2)) or (validate(kingx-1) and validate(kingy-2)) or (validate(kingx+1) and validate(kingy+2)) or (validate(kingx-1) and validate(kingy+2)) or (validate(kingx-2) and validate(kingy+1)) or (validate(kingx-2) and validate(kingy-1)) or (validate(kingx+2) and validate(kingy+1)) or (validate(kingx+2) and validate(kingy-1))):
        if(((kingx+1==wkingx) and (kingy-2==wkingy)) or ((kingx-1==wkingx) and (kingy-2==wkingy)) or ((kingx+1==wkingx) and (kingy+2==wkingy)) or ((kingx-1==wkingx) and (kingy+2==wkingy)) or ((kingx-2==wkingx) and (kingy+1==wkingy)) or ((kingx-2==wkingx) and (kingy-1==wkingy)) or ((kingx+2==wkingx) and (kingy+1==wkingy)) or ((kingx+2==wkingx) and (kingy-1==wkingy))):
            return False
    return True

def rook(rookx,rooky,wkingx,wkingy):
    if(rookx==wkingx or rooky==wkingy):
        return False
    return True

def bishop(bishopx,bishopy,wkingx,wkingy):
        # S-w
        tx=bishopx
        ty=bishopy
        while(tx<BOARD_SIZE and ty<BOARD_SIZE):
            if(tx==wkingx and wkingy==ty):
                return False
            else:
                tx+=1
                ty+=1
        # S-e
        tx=bishopx
        ty=bishopy
        while(tx>=0 and ty<BOARD_SIZE):
            if(tx==wkingx and wkingy==ty):
                return False
            else:
                tx-=1
                ty+=1
        # N-W
        tx=bishopx
        ty=bishopy
        while(tx<BOARD_SIZE and ty>=0):
            if(tx==wkingx and wkingy==ty):
                return False
            else:
                 tx+=1
                 ty-=1
        # N-E
        tx=bishopx
        ty=bishopy
        while(tx>=0 and ty>=0):
            if(tx==wkingx and wkingy==ty):
                return False
            else:
                 tx-=1
                 ty-=1
        return True
def queen(queenx,queeny,wkingx,wkingy):
    if(rook(queenx,queeny,wkingx,wkingy) and bishop(queenx,queeny,wkingx,wkingy)):
        return True
    return False
def func(x,y):
    for i in black:
        s=i.split('_')[0]
        if(s=='Knight'):
            if(kinght(black[i][0],black[i][1],x,y)==False):
                return False
        elif(s=='Pawn'):
            if(pawn(black[i][0],black[i][1],x,y)==False):
                return False
        elif(s=='Queen'):
            if(queen(black[i][0],black[i][1],x,y)==False):
                return False
        elif(s=='Bishop'):
            if(bishop(black[i][0],black[i][1],x,y)==False):
                return False
        elif(s=='Rook'):
            if(rook(black[i][0],black[i][1],x,y)==False):
                return False
        elif(s=='King'):
            if(king(black[i][0],black[i][1],x,y)==False):
                return False
    return True

def white(x, y):
    # x,y=WHITE_X, WHITE_Y
    i=0
    # while(validate(x,y)):
    if(func(x,y)):
        return x,y,i
    while(i<BOARD_SIZE):
        up=y-i
        down=y+i
        right=x+i
        left = x-i
        for j in range(left,right+1):
            if(valid(j,up)):
                if(func(j,up)):
                    # WHITE_X, WHITE_Y= j,up
                    return j,up,i
                    
            if(valid(j,down)):
                if(func(j,down)):
                    # WHITE_X, WHITE_Y= j,down
                    return j,down,i
        for j in range(up+1,down):
            if(valid(left,j)):
                if(func(left,j)):
                    # WHITE_X, WHITE_Y = left,j
                    return left,j,i
            if(valid(right,j)):
                if(func(right,j)):
                    # WHITE_X, WHITE_Y =right,j
                    return right,j,i
        i+=1
    return 0,0,0
## Function which will be executed after the 'Evaluate' button click
#
def placeSequence():
    # clear the canvas
    text_file = open(sys.argv[1], "w")
    text_file.write(widgetInfoDict["text"].get(1.0, END))
    text_file.close()
    widgetInfoDict["canvas"].delete("all")
    # Re-render the board
    data = readData(sys.argv[1])
    renderBoard(BOARD_SIZE,data)
    ta,tb,d = white(wk[0],wk[1])
    tema,temb,td=wk[0],wk[1],wk[2]
    wk[0],wk[1],wk[2] = ta,tb,td
    renderPiece(ta, tb, 'WhiteKing')
    if(tema==ta and temb==tb):
        print("No change in position of white king as it's already safe. ")
        print(showinfo("showinfo", ("No change in position of white king as it's already safe. ")))

    else:
        print("New position",ta,tb, "distance=",d)
        print(showinfo("showinfo", ("New position",ta,tb, "distance travelled =",d)))

a,b = 0,0
wk=[0,0,0]
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Please pass the <Black Positions> file path, <White King Coordinates> and <Board Size> as arguments in "
            "the command line")
        sys.exit()

    BOARD_SIZE = int(sys.argv[4])
    WHITE_X, WHITE_Y = int(sys.argv[2]), int(sys.argv[3])
    # print(WHITE_X)
    a,b=WHITE_X,WHITE_Y
    wk[0],wk[1]=a,b
    data = readData(sys.argv[1])
    createEditor(data)