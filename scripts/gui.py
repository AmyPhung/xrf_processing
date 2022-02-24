import tkinter as tk
import tkFileDialog as fd

class XRFWindow():
    def __init__(self):
        self.mca_filename = ""
        self.calib_filename = ""
        self.cfg_filename = ""

        # Create the root window
        self.window = tk.Tk()
        # self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Set window title
        self.window.title('XRF Data Connection')

        # Set window background color
        # self.window.config(background = "white")

        # Create a File Explorer label
        self.mca_file_label = tk.Label(self.window,
                                    text = "Choose mca file...        ", wraplength=500)#, justify=tk.LEFT)#,
                                    #width = 50, height = 4)

        self.calib_file_label = tk.Label(self.window,
                                    text = "Choose calib file...        ", wraplength=500)#, justify=tk.LEFT)#,
                                    #width = 50, height = 4)

        self.cfg_file_label = tk.Label(self.window,
                                    text = "Choose cfg file...        ", wraplength=500)#, justify=tk.LEFT)#,
                                    #width = 50, height = 4)

        self.mca_file_button = tk.Button(self.window,
                                text = "Browse mca files",
                                command = self.mcaFilesButtonCB,
                                width=15)

        self.calib_file_button = tk.Button(self.window,
                             text = "Browse calib files",
                             command = self.calibFilesButtonCB,
                             width=15)

        self.cfg_file_button = tk.Button(self.window,
                             text = "Browse cfg files",
                             command = self.cfgFilesButtonCB,
                             width=15)

        self.send_button = tk.Button(self.window,
                             text = "Send data to server",
                             command = self.sendButtonCB)

        self.mca_file_label.grid(column = 1, row = 1)
        self.calib_file_label.grid(column = 1, row = 2)
        self.cfg_file_label.grid(column = 1, row = 3)

        self.mca_file_button.grid(column = 2, row = 1)
        self.calib_file_button.grid(column = 2, row = 2)
        self.cfg_file_button.grid(column = 2, row = 3)
        self.send_button.grid(column = 1, row = 4)

        # Set window size
        self.window.geometry("600x300")

        # Flag for main loop
        self.send_data = False

    def mcaFilesButtonCB(self):
        self.mca_filename = fd.askopenfilename(initialdir = "", title = "Select a File",
            filetypes = (("Multi Channel Analyzers", "*.mca*"),
                         ("all files", "*.*")))

        self.mca_file_label.configure(text=self.mca_filename)

    def calibFilesButtonCB(self):
        self.calib_filename = fd.askopenfilename(initialdir = "", title = "Select a File",
            filetypes = (("Calibration Files", "*.calib*"),
                         ("all files", "*.*")))

        self.calib_file_label.configure(text=self.calib_filename)

    def cfgFilesButtonCB(self):
        self.cfg_filename = fd.askopenfilename(initialdir = "", title = "Select a File",
            filetypes = (("Configuration Files", "*.cfg*"),
                         ("all files", "*.*")))

        self.cfg_file_label.configure(text=self.cfg_filename)

    def sendButtonCB(self):
        if self.mca_filename == "":
            print("[ERROR]: mca filename cannot be blank!")
            return
        elif self.calib_filename == "":
            print("[ERROR]: calib filename cannot be blank!")
            return
        elif self.cfg_filename == "":
            print("[ERROR]: cfg filename cannot be blank!")
            return
        self.send_data = True

    def update(self):
        self.window.update()
