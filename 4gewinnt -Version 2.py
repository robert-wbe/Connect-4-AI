from tkinter import *
import time
#import winsound
tk = Tk()
canvas_width = 600
canvas_height = 700
w = Canvas(tk,width=canvas_width,height=canvas_height)
w.config(bg="#ffffff")
w.pack()
ccolumns = 7
rows = 6
player = 0
columns = []
comb = [[-1,1],[1,1],[1,0],[0,-1]]
resp = ["Congrats, you've won!","I won! Try again."]
for i in range(ccolumns):
    columns.append([])
for i in range (ccolumns+1):
    w.create_line(i*(canvas_width/ccolumns),0,i*(canvas_width/ccolumns),canvas_width, fill="#000000")
for i in range (rows+1):
    w.create_line(0,i*(canvas_width/rows),canvas_width,i*(canvas_width/rows), fill="#000000")
w.create_text(300, 615, text="The computer player is run by an engine developed by Robert Wiebe in 2019.", fill= "#000000")
symbols = ["/Volumes/SD-XD/Programme/Bilder/crossred.png","/Volumes/SD-XD/Programme/Bilder/circle.gif"]
def draw_symbol(column):
    global player
    row = len(columns[column])
    if row <= rows:
        img = PhotoImage(file=symbols[player])
        img =img.subsample(4,4)
        w.create_image(column*canvas_width/ccolumns+(canvas_width/ccolumns)/2,canvas_width-row*canvas_width/rows-(canvas_width/rows)/2,image = img)
        columns[column].append(player)
        w.update()
        if checkwinner(column,row) == 1:
            print("Spieler",player+1,"gewinnt!")
            w.create_text(canvas_width/2,canvas_height-50,font="Arial 40",fill="red",text=resp[player])
        elif player == 0:
            player = 1
            com_move()
        else:
            player = 0
        w.mainloop()
def getcolumn(posx):
    for i in range(ccolumns):
        if (i+1)*canvas_width/ccolumns > posx:
            return i
            break
def checkdir(c,r,cc,cr):
    count = 1
    cl = c + cc
    rw = r + cr
    while 0 <= cl <= ccolumns-1 and 0 <= rw <= len(columns[cl])-1:
        if columns[cl][rw] == columns[c][r]:
            count = count + 1
            cl = cl + cc
            rw = rw + cr
        else:
            break
    return count

def inv(i):
    if i == 0:
        return 1
    else:
        return 0

def valdir(c,r,cc,cr,pl,al,ac):
    count = ac
    i = 0
    il = al
    serie = 1
    wn = 0
    c1 = c + cc
    r1 = r + cr
    potential_row = 0
    gaps = 0
    while 0 <= c1 <= ccolumns-1 and rows > r1 >= 0:
        i = i + 1
        if r1 <= len(columns[c1]) - 1:
            if columns[c1][r1] == inv(pl):
                count = count - i*(0.1)
                break
            else:
                count = count + 1
                potential_row += 1
                if serie == 1:
                    #print("here")
                    il = il + 1
                    #print(il)
                    count = count*(2**(il-1))
                c1 = c1 + cc
                r1 = r1 + cr
        else:
            gaps += 1
            if serie == 1:
                count = count + 2**(il-1)
                serie = 0
            c1 = c1 + cc
            r1 = r1 + cr
    if serie == 1 and cr != -1 and il < 4:
        count = count/(2**il)
    #print("valdir",cc,cr,il,"count:",count)
    if cc == 0 and cr == 1:
        return [0,1]
    else:
        if il >= 4:
            count = 235 + pl*20
            wn = 1
        return [count,il,wn]

def checkwinner(c,r):
    hor = checkdir(c,r,1,0) + checkdir(c,r,-1,0)
    ver = checkdir(c,r,0,1) + checkdir(c,r,0,-1)
    ldig = checkdir(c,r,1,1) + checkdir(c,r,-1,-1)
    rdig = checkdir(c,r,1,-1) + checkdir(c,r,-1,1)
    if hor >= 5 or ver >= 5 or ldig >= 5 or rdig >= 5:
        return 1

def score(c,r):
    score = 0
    for co in comb:
        for p in range(2):
            score = score + valdir(c,r,co[0],co[1],p,valdir(c,r,-co[0],-co[1],p,1,0)[1],valdir(c,r,-co[0],-co[1],p,1,0)[0])[0]
    #print(c,r,score)
    return score

def com_move():
    time.sleep(1.5)
    vals = []
    for i in range(ccolumns):
        val = 0
        if len(columns[i]) < rows:
            val = score(i,len(columns[i]))
            if len(columns[i]) < rows-1 and val < 235:
                val = val - score(i,len(columns[i])+1)
        else:
            val = -50
        vals.append(val)
    draw_symbol(vals.index(max(vals)))


def move(event):
    global player
    draw_symbol(getcolumn(event.x))

w.bind("<Button-1>",move)
w.mainloop()