#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import Tkinter as tk
from pycomm.ab_comm.slc import Driver as SlcDriver
import logging
from PIL import ImageTk, Image

WindowsSize = "780x1050"
PLC_IP_Adress = '172.23.1.77'
Update_Program_Every_ms = 50



class DripControl:

    def __init__(self, master, connection, ipAddress):

        self.root = master
        self.connection = connection

        self.active_image = ImageTk.PhotoImage(file="active.gif")
        self.inactive_image = ImageTk.PhotoImage(file="inactive.gif")

        self.connection_status = ""
        self.start_hr_1 = 0
        self.start_min_1 = 0
        self.end_hr_1 = 0
        self.end_min_1 = 0
        self.start_hr_2 = 0
        self.start_min_2 = 0
        self.end_hr_2 = 0
        self.end_min_2 = 0
        self.start_hr_3 = 0
        self.start_min_3 = 0
        self.end_hr_3 = 0
        self.end_min_3 = 0
        self.start_hr_4 = 0
        self.start_min_4 = 0
        self.end_hr_4 = 0
        self.end_min_4 = 0
        self.auto_watering_status = self.inactive_image
        self.auto_drip_status = self.inactive_image

        if connection.open(ipAddress):
            self.connection_status = "Successful" #"เชื่อมต่อสำเร็จ"
            self.start_hr_1 = connection.read_tag('N7:2')
            self.start_min_1 = connection.read_tag('N7:3')
            self.end_hr_1 = connection.read_tag('N7:4')
            self.end_min_1 = connection.read_tag('N7:5')
            self.start_hr_2 = connection.read_tag('N7:6')
            self.start_min_2 = connection.read_tag('N7:7')
            self.end_hr_2 = connection.read_tag('N7:8')
            self.end_min_2 = connection.read_tag('N7:9')
            self.start_hr_3 = connection.read_tag('N7:10')
            self.start_min_3 = connection.read_tag('N7:11')
            self.end_hr_3 = connection.read_tag('N7:12')
            self.end_min_3 = connection.read_tag('N7:13')
            self.start_hr_4 = connection.read_tag('N7:14')
            self.start_min_4 = connection.read_tag('N7:15')
            self.end_hr_4 = connection.read_tag('N7:16')
            self.end_min_4 = connection.read_tag('N7:17')

            if(connection.read_tag('B3:3/1') == 1):
                self.auto_watering_status = self.active_image
            else:
                self.auto_watering_status = self.inactive_image

            if(connection.read_tag('B3:2/5') == 1):
                self.auto_drip_status = self.active_image
            else:
                self.auto_drip_status = self.inactive_image

        else:
            self.connection_status = "!!Can't connect!!" #"ไม่สามารถเชื่อมต่อได้"
        self.header_bg_color = "#252525"
        self.active_char_color = "#BDBDBD"
        self.control_bg_color = "#363636"
        self.total_bg_color = "#2A2A2A"
        self.border_color = "#7B7B7B"
        self.button_highlight_color = "#5A5A5A"
        self.something_change_colur = "#332424"

        

        master.title('โปรแกรมควบคุมน้ำหยด')
        master.config(bg=self.total_bg_color)

        self.frame_header = tk.Frame(master, bg=self.header_bg_color)
        self.frame_header.pack(fill="x", anchor = "n", expand=False)
        tk.Label(self.frame_header, text = "Connection status : " + self.connection_status, bg=self.header_bg_color, fg=self.active_char_color, height=4, anchor="center").pack()
    
        self.main_control = tk.Frame(master, bg=self.total_bg_color)
        self.main_control.pack(fill='both')
        self.schedule_control = tk.Frame(self.main_control, bg=self.total_bg_color)
        self.schedule_control.grid(row=0,column=0, padx = (20,60), pady=20)
        self.system_status = tk.Frame(self.main_control, bg=self.total_bg_color)
        self.system_status.grid(row=0,column=2)
        
        self.frame_irreigation_pump_status_indicator = tk.Frame(self.system_status, bg=self.total_bg_color)
        self.frame_irreigation_pump_status_indicator.pack(side='top')
        tk.Label(self.frame_irreigation_pump_status_indicator, text="Auto irrigation pump", bg=self.total_bg_color, fg=self.active_char_color).grid(row=0,column=0)
        self.WaterAutoStatusImage = tk.Label(self.frame_irreigation_pump_status_indicator,image=self.auto_watering_status, bg=self.total_bg_color)
        self.WaterAutoStatusImage.image = self.auto_watering_status
        self.WaterAutoStatusImage.grid(row=1, column=0)

        self.frame_drip_status_indicator = tk.Frame(self.system_status, bg=self.total_bg_color)
        self.frame_drip_status_indicator.pack(pady=50)
        tk.Label(self.frame_drip_status_indicator, text="Auto dripping", bg=self.total_bg_color, fg=self.active_char_color).grid(row=0,column=0)
        self.DripAutoStatusImage = tk.Label(self.frame_drip_status_indicator,image=self.auto_drip_status, bg=self.total_bg_color)
        self.DripAutoStatusImage.image = self.auto_drip_status
        self.DripAutoStatusImage.grid(row=1, column=0)
        


        self.frame_control_program1 = tk.Frame(self.schedule_control, bg=self.control_bg_color)
        self.frame_control_program1.pack(fill="both", padx=30, pady=30, ipadx=10, ipady=10, expand=False)
        self.subframe_control_program1 = tk.Frame(self.frame_control_program1, bg=self.control_bg_color)
        self.subframe_control_program1.pack(anchor="center")
        tk.Label(self.subframe_control_program1, text = "โปรแกรม 1", bg=self.control_bg_color, fg=self.active_char_color).grid(row=0, sticky="w", padx=10, pady=10)
        tk.Label(self.subframe_control_program1, text = "Start", bg=self.control_bg_color, fg=self.active_char_color).grid(row=1, column=0, columnspan = 4, padx=20, pady=(10,1), sticky="w")
        self.entry_start_hr_1 = tk.Entry(self.subframe_control_program1, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_start_hr_1.grid(row=2, column=0, padx=(10,0), pady=(0,10))
        self.entry_start_min_1 = tk.Entry(self.subframe_control_program1, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_start_min_1.grid(row=2, column=1, padx=0, pady=(0,10))
        tk.Label(self.subframe_control_program1, text = "น.", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=2, padx=2, pady=(0,10))
        tk.Label(self.subframe_control_program1, text = " >>>>> ", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=3, padx=2, pady=(0,10))
        tk.Label(self.subframe_control_program1, text = "End", bg=self.control_bg_color, fg=self.active_char_color).grid(row=1, column=4, columnspan = 4, padx=10, pady=(10,1), sticky="w")
        self.entry_end_hr_1 = tk.Entry(self.subframe_control_program1, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_end_hr_1.grid(row=2, column=5, padx=(10,0), pady=(0,10))
        self.entry_end_min_1 = tk.Entry(self.subframe_control_program1, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_end_min_1.grid(row=2, column=6, padx=(10,0), pady=(0,10))
        tk.Label(self.subframe_control_program1, text = "น.", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=7, padx=2, pady=(0,10))
        tk.Button(self.subframe_control_program1, text="Update", highlightcolor=self.button_highlight_color, highlightbackground=self.border_color, bg=self.total_bg_color, fg=self.active_char_color).grid(row=3,columnspan=8, padx=(0,90), pady=(10,20), sticky="e")
        tk.Button(self.subframe_control_program1, text="Cancel", highlightcolor=self.button_highlight_color, highlightbackground=self.border_color, bg=self.total_bg_color, fg=self.active_char_color).grid(row=3,columnspan=8, padx=(0,0), pady=(10,20), sticky="e")

   
        self.frame_control_program2 = tk.Frame(self.schedule_control, bg=self.control_bg_color)
        self.frame_control_program2.pack(fill="both", padx=30, pady=30, expand=False)
        self.subframe_control_program2 = tk.Frame(self.frame_control_program2, bg=self.control_bg_color)
        self.subframe_control_program2.pack(anchor="center")
        tk.Label(self.subframe_control_program2, text = "โปรแกรม 2", bg=self.control_bg_color, fg=self.active_char_color).grid(row=0, sticky="w", padx=10, pady=10)
        tk.Label(self.subframe_control_program2, text = "Start", bg=self.control_bg_color, fg=self.active_char_color).grid(row=1, column=0, columnspan = 4, padx=20, pady=(10,1), sticky="w")
        self.entry_start_hr_2 = tk.Entry(self.subframe_control_program2, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_start_hr_2.grid(row=2, column=0, padx=(10,0), pady=(0,10))
        self.entry_start_min_2 = tk.Entry(self.subframe_control_program2, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_start_min_2.grid(row=2, column=1, padx=0, pady=(0,10))
        tk.Label(self.subframe_control_program2, text = "น.", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=2, padx=2, pady=(0,10))
        tk.Label(self.subframe_control_program2, text = " >>>>> ", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=3, padx=2, pady=(0,10))
        tk.Label(self.subframe_control_program2, text = "End", bg=self.control_bg_color, fg=self.active_char_color).grid(row=1, column=4, columnspan = 4, padx=10, pady=(10,1), sticky="w")
        self.entry_end_hr_2 = tk.Entry(self.subframe_control_program2, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_end_hr_2.grid(row=2, column=5, padx=(10,0), pady=(0,10))
        self.entry_end_min_2 = tk.Entry(self.subframe_control_program2, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_end_min_2.grid(row=2, column=6, padx=(10,0), pady=(0,10))
        tk.Label(self.subframe_control_program2, text = "น.", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=7, padx=2, pady=(0,10))
        tk.Button(self.subframe_control_program2, text="Update", highlightcolor=self.button_highlight_color, highlightbackground=self.border_color, bg=self.total_bg_color, fg=self.active_char_color).grid(row=3,columnspan=8, padx=(0,90), pady=(10,20), sticky="e")
        tk.Button(self.subframe_control_program2, text="Cancel", highlightcolor=self.button_highlight_color, highlightbackground=self.border_color, bg=self.total_bg_color, fg=self.active_char_color).grid(row=3,columnspan=8, padx=(0,0), pady=(10,20), sticky="e")


        
        self.frame_control_program3 = tk.Frame(self.schedule_control, bg=self.control_bg_color)
        self.frame_control_program3.pack(fill="both", padx=30, pady=30, expand=False)
        self.subframe_control_program3 = tk.Frame(self.frame_control_program3, bg=self.control_bg_color)
        self.subframe_control_program3.pack(anchor="center")
        tk.Label(self.subframe_control_program3, text = "โปรแกรม 3", bg=self.control_bg_color, fg=self.active_char_color).grid(row=0, sticky="w", padx=10, pady=10)
        tk.Label(self.subframe_control_program3, text = "Start", bg=self.control_bg_color, fg=self.active_char_color).grid(row=1, column=0, columnspan = 4, padx=20, pady=(10,1), sticky="w")
        self.entry_start_hr_3 = tk.Entry(self.subframe_control_program3, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_start_hr_3.grid(row=2, column=0, padx=(10,0), pady=(0,10))
        self.entry_start_min_3 = tk.Entry(self.subframe_control_program3, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_start_min_3.grid(row=2, column=1, padx=0, pady=(0,10))
        tk.Label(self.subframe_control_program3, text = "น.", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=2, padx=2, pady=(0,10))
        tk.Label(self.subframe_control_program3, text = " >>>>> ", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=3, padx=2, pady=(0,10))
        tk.Label(self.subframe_control_program3, text = "End", bg=self.control_bg_color, fg=self.active_char_color).grid(row=1, column=4, columnspan = 4, padx=10, pady=(10,1), sticky="w")
        self.entry_end_hr_3 = tk.Entry(self.subframe_control_program3, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_end_hr_3.grid(row=2, column=5, padx=(10,0), pady=(0,10))
        self.entry_end_min_3 = tk.Entry(self.subframe_control_program3, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_end_min_3.grid(row=2, column=6, padx=(10,0), pady=(0,10))
        tk.Label(self.subframe_control_program3, text = "น.", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=7, padx=2, pady=(0,10))
        tk.Button(self.subframe_control_program3, text="Update", highlightcolor=self.button_highlight_color, highlightbackground=self.border_color, bg=self.total_bg_color, fg=self.active_char_color).grid(row=3,columnspan=8, padx=(0,90), pady=(10,20), sticky="e")
        tk.Button(self.subframe_control_program3, text="Cancel", highlightcolor=self.button_highlight_color, highlightbackground=self.border_color, bg=self.total_bg_color, fg=self.active_char_color).grid(row=3,columnspan=8, padx=(0,0), pady=(10,20), sticky="e")

        
        self.frame_control_program4 = tk.Frame(self.schedule_control, bg=self.control_bg_color)
        self.frame_control_program4.pack(fill="both", padx=30, pady=30, expand=False)
        self.subframe_control_program4 = tk.Frame(self.frame_control_program4, bg=self.control_bg_color)
        self.subframe_control_program4.pack(anchor="center")
        tk.Label(self.subframe_control_program4, text = "โปรแกรม 4", bg=self.control_bg_color, fg=self.active_char_color).grid(row=0, sticky="w", padx=10, pady=10)
        tk.Label(self.subframe_control_program4, text = "Start", bg=self.control_bg_color, fg=self.active_char_color).grid(row=1, column=0, columnspan = 4, padx=20, pady=(10,1), sticky="w")
        self.entry_start_hr_4 = tk.Entry(self.subframe_control_program4, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_start_hr_4.grid(row=2, column=0, padx=(10,0), pady=(0,10))
        self.entry_start_min_4 = tk.Entry(self.subframe_control_program4, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_start_min_4.grid(row=2, column=1, padx=0, pady=(0,10))
        tk.Label(self.subframe_control_program4, text = "น.", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=2, padx=2, pady=(0,10))
        tk.Label(self.subframe_control_program4, text = " >>>>> ", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=3, padx=2, pady=(0,10))
        tk.Label(self.subframe_control_program4, text = "End", bg=self.control_bg_color, fg=self.active_char_color).grid(row=1, column=4, columnspan = 4, padx=10, pady=(10,1), sticky="w")
        self.entry_end_hr_4 = tk.Entry(self.subframe_control_program4, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_end_hr_4.grid(row=2, column=5, padx=(10,0), pady=(0,10))
        self.entry_end_min_4 = tk.Entry(self.subframe_control_program4, width = 6, bg=self.total_bg_color, highlightbackground=self.control_bg_color, highlightcolor=self.header_bg_color, fg=self.active_char_color)
        self.entry_end_min_4.grid(row=2, column=6, padx=(10,0), pady=(0,10))
        tk.Label(self.subframe_control_program4, text = "น.", bg=self.control_bg_color, fg=self.active_char_color).grid(row=2, column=7, padx=2, pady=(0,10))
        tk.Button(self.subframe_control_program4, text="Update", highlightcolor=self.button_highlight_color, highlightbackground=self.border_color, bg=self.total_bg_color, fg=self.active_char_color).grid(row=3,columnspan=8, padx=(0,90), pady=(10,20), sticky="e")
        tk.Button(self.subframe_control_program4, text="Cancel", highlightcolor=self.button_highlight_color, highlightbackground=self.border_color, bg=self.total_bg_color, fg=self.active_char_color).grid(row=3,columnspan=8, padx=(0,0), pady=(10,20), sticky="e")
        
        self.get_data_all()

        
        
        
        # self.entry_start_min_1.insert(0,self.start_min_1)
        # self.entry_end_hr_1.insert(0,self.end_hr_1)
        # self.entry_end_min_1.insert(0,self.end_min_1)
        # self.entry_start_hr_2.insert(0,self.start_hr_2)
        # self.entry_start_min_2.insert(0,self.start_min_2)
        # self.entry_end_hr_2.insert(0,self.end_hr_2)
        # self.entry_end_min_2.insert(0,self.end_min_2)
        # self.entry_start_hr_3.insert(0,self.start_hr_3)
        # self.entry_start_min_3.insert(0,self.start_min_3)
        # self.entry_end_hr_3.insert(0,self.end_hr_3)
        # self.entry_end_min_3.insert(0,self.end_min_3)
        # self.entry_start_hr_4.insert(0,self.start_hr_4)
        # self.entry_start_min_4.insert(0,self.start_min_4)
        # self.entry_end_hr_4.insert(0,self.end_hr_4)
        # self.entry_end_min_4.insert(0,self.end_min_4)
    

    def get_data_all(self):
        self.get_data(self.entry_start_hr_1,self.start_hr_1)
        self.get_data(self.entry_start_min_1,self.start_min_1)
        self.get_data(self.entry_end_hr_1,self.end_hr_1)
        self.get_data(self.entry_end_min_1,self.end_min_1)
        self.get_data(self.entry_start_hr_2,self.start_hr_2)
        self.get_data(self.entry_start_min_2,self.start_min_2)
        self.get_data(self.entry_end_hr_2,self.end_hr_2)
        self.get_data(self.entry_end_min_2,self.end_min_2)
        self.get_data(self.entry_start_hr_3,self.start_hr_3)
        self.get_data(self.entry_start_min_3,self.start_min_3)
        self.get_data(self.entry_end_hr_3,self.end_hr_3)
        self.get_data(self.entry_end_min_3,self.end_min_3)
        self.get_data(self.entry_start_hr_4,self.start_hr_4)
        self.get_data(self.entry_start_min_4,self.start_min_4)
        self.get_data(self.entry_end_hr_4,self.end_hr_4)
        self.get_data(self.entry_end_min_4,self.end_min_4)


    def get_data(self, entry, value):
        entry.delete(0, 'end')
        entry.insert(0, value)



    # def update(self):




    # def cancel(self):

c = SlcDriver()
root = tk.Tk()
root.resizable(width=False, height=False)
root.geometry(WindowsSize)
controller = DripControl(root, c, PLC_IP_Adress)

def compare_CurrentEntryGUIData_with_plcData():
        if(str(controller.entry_start_hr_1.get()) == str(controller.connection.read_tag('N7:2'))):
            controller.entry_start_hr_1.configure(bg=controller.total_bg_color)
        else:
            controller.entry_start_hr_1.configure(bg=controller.something_change_colur)

        if(str(controller.entry_start_min_1.get()) == str(controller.connection.read_tag('N7:3'))):
            controller.entry_start_min_1.configure(bg=controller.total_bg_color)
        else:
            controller.entry_start_min_1.configure(bg=controller.something_change_colur)
        if(str(controller.entry_end_hr_1.get()) == str(controller.connection.read_tag('N7:4'))):
            controller.entry_end_hr_1.configure(bg=controller.total_bg_color)
        else:
            controller.entry_end_hr_1.configure(bg=controller.something_change_colur)

        if(str(controller.entry_end_min_1.get()) == str(controller.connection.read_tag('N7:5'))):
            controller.entry_end_min_1.configure(bg=controller.total_bg_color)
        else:
            controller.entry_end_min_1.configure(bg=controller.something_change_colur)

        if(str(controller.entry_start_hr_2.get()) == str(controller.connection.read_tag('N7:6'))):
            controller.entry_start_hr_2.configure(bg=controller.total_bg_color)
        else:
            controller.entry_start_hr_2.configure(bg=controller.something_change_colur)

        if(str(controller.entry_start_min_2.get()) == str(controller.connection.read_tag('N7:7'))):
            controller.entry_start_min_2.configure(bg=controller.total_bg_color)
        else:
            controller.entry_start_min_2.configure(bg=controller.something_change_colur)
        if(str(controller.entry_end_hr_2.get()) == str(controller.connection.read_tag('N7:8'))):
            controller.entry_end_hr_2.configure(bg=controller.total_bg_color)
        else:
            controller.entry_end_hr_2.configure(bg=controller.something_change_colur)

        if(str(controller.entry_end_min_2.get()) == str(controller.connection.read_tag('N7:9'))):
            controller.entry_end_min_2.configure(bg=controller.total_bg_color)
        else:
            controller.entry_end_min_2.configure(bg=controller.something_change_colur) 

        if(str(controller.entry_start_hr_3.get()) == str(controller.connection.read_tag('N7:10'))):
            controller.entry_start_hr_3.configure(bg=controller.total_bg_color)
        else:
            controller.entry_start_hr_3.configure(bg=controller.something_change_colur)

        if(str(controller.entry_start_min_3.get()) == str(controller.connection.read_tag('N7:11'))):
            controller.entry_start_min_3.configure(bg=controller.total_bg_color)
        else:
            controller.entry_start_min_3.configure(bg=controller.something_change_colur)
        if(str(controller.entry_end_hr_3.get()) == str(controller.connection.read_tag('N7:12'))):
            controller.entry_end_hr_3.configure(bg=controller.total_bg_color)
        else:
            controller.entry_end_hr_3.configure(bg=controller.something_change_colur)

        if(str(controller.entry_end_min_3.get()) == str(controller.connection.read_tag('N7:13'))):
            controller.entry_end_min_3.configure(bg=controller.total_bg_color)
        else:
            controller.entry_end_min_3.configure(bg=controller.something_change_colur)

        if(str(controller.entry_start_hr_4.get()) == str(controller.connection.read_tag('N7:14'))):
            controller.entry_start_hr_4.configure(bg=controller.total_bg_color)
        else:
            controller.entry_start_hr_4.configure(bg=controller.something_change_colur)

        if(str(controller.entry_start_min_4.get()) == str(controller.connection.read_tag('N7:15'))):
            controller.entry_start_min_4.configure(bg=controller.total_bg_color)
        else:
            controller.entry_start_min_4.configure(bg=controller.something_change_colur)
        if(str(controller.entry_end_hr_4.get()) == str(controller.connection.read_tag('N7:16'))):
            controller.entry_end_hr_4.configure(bg=controller.total_bg_color)
        else:
            controller.entry_end_hr_4.configure(bg=controller.something_change_colur)

        if(str(controller.entry_end_min_4.get()) == str(controller.connection.read_tag('N7:17'))):
            controller.entry_end_min_4.configure(bg=controller.total_bg_color)
        else:
            controller.entry_end_min_4.configure(bg=controller.something_change_colur)

        
        controller.root.after(Update_Program_Every_ms, compare_CurrentEntryGUIData_with_plcData)


def main():
    
    compare_CurrentEntryGUIData_with_plcData()
    root.mainloop()

if __name__== "__main__": main()