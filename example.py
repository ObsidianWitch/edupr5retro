import tkinter
import os, inspect
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageTk
from PIL import ImageDraw
import retro

######################################################################
#
# Mise en place de la partie technique | ne pas toucher

def ColorKey(image, color):
    img = image.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if (item[0] == color[0]) and (item[1] == color[1]) and (item[2] == color[2]):
            newData.append((0,0,0,0))
        else:
            newData.append(item)
    return img



scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))
scriptDIR  = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "assets")
myfont = ImageFont.truetype(font = os.path.join(assets, "DejaVuSansMono.ttf"), size = 30)


KEYPressed = set()
OnBoucle = True
window = tkinter.Tk()
WIDTH, HEIGHT = 640, 480
buffer = Image.new('RGBA', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(buffer)

def keyup(e):
    KEYPressed.remove(e.keysym)

def keydown(e):
    KEYPressed.add(e.keysym)
    #print(e.keysym)

def Fermeture():
    OnBoucle = False

def MouseClick(event):
    window.focus_set()
    print("clicked at", event.x, event.y)

def ReadMouseXY():
    x = window.winfo_pointerx()
    y = window.winfo_pointery()
    ax = window.winfo_pointerx() - window.winfo_rootx()
    ay = window.winfo_pointery() - window.winfo_rooty()
    if (ax < 0): ax = 0
    if (ax >= WIDTH ): ax = WIDTH - 1
    if (ay < 0): ay = 0
    if (ay >= HEIGHT): ay = HEIGHT - 1
    return (ax, ay)


canvas = tkinter.Canvas(window, width = WIDTH, height = HEIGHT, bg = "#000000")
window.title('Mon Super Jeu')
window.bind("<KeyPress>", keydown)
window.bind("<KeyRelease>", keyup)
window.protocol("WM_DELETE_WINDOW", Fermeture)
window.bind("<Button-1>", MouseClick)
window.config(cursor = 'none')
img = tkinter.PhotoImage(width = WIDTH, height = HEIGHT)
ECRAN = canvas.create_image((WIDTH / 2, HEIGHT / 2), image = img, state = "normal")
canvas.pack()

clock = retro.Clock(framerate = 60)

######################################################################
#
# Création des ressoures du jeu

bandit = PIL.Image.open(os.path.join(assets, "bandit_rue.png"))
bandit = ColorKey(bandit,(255,255,255))  # donne la couleur de fond transparente

decor = PIL.Image.open(os.path.join(assets, "map.png"))


fff = 0


while(OnBoucle):
    (MouseX,MouseY) = ReadMouseXY()

    #################################################################
    #
    # logique

    # https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm

    if ('Escape' in KEYPressed): OnBoucle = False
    if ('Left' in KEYPressed): fff -= 5
    if ('Right' in KEYPressed): fff += 5

    #################################################################
    #
    # affichage

    #print(fff,MouseX,MouseY)
    zone_jaune = decor.crop((fff,0,fff+WIDTH,HEIGHT)) # selectionne la zone a afficher dans le décors (x1,y1,x2,y2)
    buffer.paste(zone_jaune)
    buffer.alpha_composite(bandit,(100,HEIGHT-bandit.height)) #affichage avec transparence

    bandit_small = bandit.resize((bandit.width // 2, bandit.height // 2 ))  # // pour avoir des valeurs entieres
    buffer.alpha_composite(bandit_small,(200,HEIGHT-bandit_small.height))

    bandit_small = bandit_small.rotate(180)
    buffer.alpha_composite(bandit_small,(300,HEIGHT-bandit_small.height))


    C = buffer.getpixel((MouseX,MouseY)) # valeur (R,V,B) ou (R,V,B,A) A = transparence
    # print ( 'couleur : ',C[0], C[1],C[2])


    draw.ellipse(((MouseX-5, MouseY-5), (MouseX+5, MouseY+5)), fill="blue")
    draw.text((30, 5),"Utilisez les flèches <- ->", font= myfont, fill=(255,0,0))

    ##################################################################
    #
    #  gestion des FPS et de l'affiche écran | ne pas toucher

    # transfert de la zone de dessin vers l'ecran
    photo = PIL.ImageTk.PhotoImage(buffer)
    canvas.itemconfig(ECRAN, image = photo)

    print(1 / clock.tick())

    #affichage
    canvas.update()

window.destroy()
