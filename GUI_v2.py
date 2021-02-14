from tkinter import *

#click function
def click():
    entered_text=textentry.get() #will get text from entry box
    output.delete(0.0, END)
    try:
        definition = dict[entered_text]
    except:
        definition = "Sorry, search result does not exist"
    output.insert(END, definition)


    
window = Tk()
window.title("Psypher")
##Label(window, text = "Search anything", bg= "black", fg = "white",
##font = "none 12 bold").grid(row=1, column=0, sticky = W)
#psypher
#photo = PhotoImage(file='AM.jpg')
Label(window, bg='black').grid(row=0, column=0, sticky=W)
#text entry box
textentry = Entry(window, width = 110, bg = "white")
textentry.grid(row=2, column=0, sticky  = E)
#button
Button(window, text='Search',width = 15, command=click).grid(row=3, column=0,sticky=N)


output = Text(window, width = 100,height = 50,wrap = WORD,background="white")
output.grid(row=5,column= 0, columnspan=2, sticky=W)

#dictionary
dict = {
'word' : 'asdjaskd'
    }

window.mainloop()
