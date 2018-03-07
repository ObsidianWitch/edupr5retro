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

window = retro.Window(
    title = "Mon Super Jeu",
    size  = (640, 480)
)
window.config(cursor = 'none')
clock = retro.Clock(framerate = 20)

draw = ImageDraw.Draw(window.buffer)

KEYPressed = set()
OnBoucle = True

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
    if (ax >= window.width ): ax = window.width - 1
    if (ay < 0): ay = 0
    if (ay >= window.height): ay = window.height - 1
    return (ax, ay)

window.bind("<KeyPress>", keydown)
window.bind("<KeyRelease>", keyup)
window.protocol("WM_DELETE_WINDOW", Fermeture)
window.bind("<Button-1>", MouseClick)

######################################################################
#
# Création des ressoures du jeu

bandit = PIL.Image.open(os.path.join(assets, "bandit_rue.png"))
bandit1 = ColorKey(bandit,(255,255,255))  # donne la couleur de fond transparente
bandit2 = bandit.resize((bandit1.width // 2, bandit1.height // 2 ))  # // pour avoir des valeurs entieres
bandit3 = bandit2.rotate(180)

decor = PIL.Image.open(os.path.join(assets, "map.png"))


fff = 0

while(OnBoucle):
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
    zone_jaune = decor.crop((fff,0,fff+window.width,window.height)) # selectionne la zone a afficher dans le décors (x1,y1,x2,y2)
    window.buffer.paste(zone_jaune)
    window.buffer.alpha_composite(bandit1, (100, window.height - bandit1.height)) #affichage avec transparence
    window.buffer.alpha_composite(bandit2, (200, window.height - bandit2.height))
    window.buffer.alpha_composite(bandit3, (300, window.height - bandit3.height))

    (MouseX,MouseY) = ReadMouseXY()
    # C = buffer.getpixel((MouseX,MouseY)) # valeur (R,V,B) ou (R,V,B,A) A = transparence
    # print ( 'couleur : ',C[0], C[1],C[2])

    draw.ellipse(((MouseX-5, MouseY-5), (MouseX+5, MouseY+5)), fill="blue")
    draw.text((30, 5),"Utilisez les flèches <- ->", font= myfont, fill=(255,0,0))

    ##################################################################
    #
    #  gestion des FPS et de l'affiche écran | ne pas toucher

    window.draw()

    print(1 / clock.tick())

window.destroy()
