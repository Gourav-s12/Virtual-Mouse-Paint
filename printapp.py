from tkinter import *
import autopy
import sys

#variables
current_x, current_y = 0,0
color = 'black'
scalewidth= 1.255
scaleheight= 1.271
widthSc, heightSc = autopy.screen.size()
widthSc= scalewidth * widthSc

#functions
def addLine(pX, pY , cX, cY ):

    canvas.create_line((pX * scalewidth, pY * scaleheight, cX *scalewidth, cY * scaleheight),fill = color ,width=5)  #"white")
    
def show_color(new_color):
    
    global color
    color = new_color

def new_canvas():
    
    canvas.delete('all')
    #print(color)
    display_pallete()

def quitd():
    
     window.withdraw()

#tkinter window  
window = Tk()

window.title('Paint')
window.state('zoomed')

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

canvas= Canvas(window,background='white') 
canvas.master.overrideredirect(True)
canvas.grid(row=0,column=0,sticky='nsew')

#2 buttons
btn= Button(canvas, text="New Canvas", bg="#353535" ,fg="#fefefe" , command=new_canvas)
btn.place(x=widthSc-150, y=555)

btn2= Button(canvas, text="Quit Draw", bg="#353535" ,fg="#fefefe" , command=quitd)
btn2.place(x=widthSc-150, y=610)

#colors
def display_pallete():
    id = canvas.create_rectangle((widthSc-65,70, widthSc - 30,105),fill='black')
    canvas.tag_bind(id, '<Button-1>', lambda x: show_color('black'))

    id = canvas.create_rectangle((widthSc-65,120, widthSc - 30,155),fill='gray')
    canvas.tag_bind(id, '<Button-1>', lambda x: show_color('gray'))

    id = canvas.create_rectangle((widthSc-65,170, widthSc - 30,205),fill='#fefefe')
    canvas.tag_bind(id, '<Button-1>', lambda x: show_color('#fefefe'))

    id = canvas.create_rectangle((widthSc-65,220, widthSc - 30,255),fill='red')
    canvas.tag_bind(id, '<Button-1>', lambda x: show_color('red'))

    id = canvas.create_rectangle((widthSc-65,270, widthSc - 30,305),fill='orange')
    canvas.tag_bind(id, '<Button-1>', lambda x: show_color('orange'))

    id = canvas.create_rectangle((widthSc-65,320, widthSc - 30,355),fill='yellow')
    canvas.tag_bind(id, '<Button-1>', lambda x: show_color('yellow'))

    id = canvas.create_rectangle((widthSc-65,370, widthSc - 30,405),fill='green')
    canvas.tag_bind(id, '<Button-1>', lambda x: show_color('green'))

    id = canvas.create_rectangle((widthSc-65,420, widthSc - 30,455),fill='blue')
    canvas.tag_bind(id, '<Button-1>', lambda x: show_color('blue'))

    id = canvas.create_rectangle((widthSc-65,470, widthSc - 30,505),fill='purple')
    canvas.tag_bind(id, '<Button-1>', lambda x: show_color('purple'))

    
display_pallete()

#top of screen transparent
canvas.master.wm_attributes("-topmost", True)
#canvas.master.wm_attributes("-disabled", True)
canvas.master.wm_attributes("-transparentcolor", "white")

#window.withdraw()
#window.deiconify()
#window.state('zoomed')
#window.mainloop()