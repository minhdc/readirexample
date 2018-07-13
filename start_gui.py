import tkinter
import setttings
import os

from do_classification import  do_classification

gui = tkinter.Tk()

src_dir_label = tkinter.Label(gui,text="SRC_DIR")
src_dir_label.grid(row=1,column=1)
src_dir_entry = tkinter.Entry(gui,bd=5,width=35,textvariable=tkinter.StringVar(gui,setttings.SRC_DIR))
src_dir_entry.grid(row=1,column=2)

dst_dir_label = tkinter.Label(gui,text="DST_DIR")
dst_dir_entry = tkinter.Entry(gui,bd=5,width=35,textvariable=tkinter.StringVar(gui,setttings.DST_DIR))
dst_dir_label.grid(row=2,column=1)
dst_dir_entry.grid(row=2,column=2)

list_of_target = tkinter.Label(gui,text="List_of_target")
list_of_target_entry = tkinter.Entry(gui,bd=5,width=35,textvariable=tkinter.StringVar(gui,setttings.LIST_OF_TARGET))
list_of_target.grid(row=3,column=1)
list_of_target_entry.grid(row=3,column=2)


excel_file_log = tkinter.Label(gui,text="excel_file_loc")
excel_file_log_entry = tkinter.Entry(gui,bd=5,width=35,textvariable=tkinter.StringVar(gui,setttings.EXCEL_FILE_LOC))
excel_file_log.grid(row=4,column=1)
excel_file_log_entry.grid(row=4,column=2)


execute_button = tkinter.Button(gui,text='Execute',command = do_classification)
execute_button.grid(row=5)

gui2 = tkinter.Tk()
terminal_frame = tkinter.Frame(gui2,height = 400, width = 400)
terminal_frame.pack(fill=tkinter.BOTH,expand=tkinter.YES)
wid = terminal_frame.winfo_id()
os.system('powershell -into %d -geometry 40x20 -sb &' % wid)

gui.mainloop()