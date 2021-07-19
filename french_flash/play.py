from tkinter import *


win = Tk()


canvas= Canvas(width=200, height=200)
canvas.pack()

canvas.text1_id = canvas.create_text(
	50,
	50,
	text = 'im some text'
	)

print(canvas.itemcget(canvas.text1_id, 'text'))

win.mainloop()

