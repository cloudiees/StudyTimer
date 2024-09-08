import ctypes
import pygetwindow as gw
import customtkinter
import psutil

# Validates if said process actually exists/is valid
def validateProcess(input):
    if input == "":
        feedback.configure(text="Please Select Something", text_color="yellow")
    else:
        x = (gw.getWindowsWithTitle(input)[0])._hWnd
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(x, ctypes.byref(pid))
        process = (psutil.Process(pid.value)).name()
        if process in blacklist:
            feedback.configure(text="Process already in blacklist.", text_color="red")
        else:
            blacklist.add(process)
            feedback.configure(text="Process successfully added.", text_color="green")
            updateBl()

# Updates the blacklist label
def updateBl():
    label = ""
    for i in blacklist:
        label += "- " + i + "\n"
    blLabel.configure(text=label)

# Kills configurator
def killConfig(test):
    configureApps.configure(state="normal")
    test.destroy()

# Adds items to blacklist
def openConfigurator(cA, bl, app):
    global blacklist
    global feedback
    global blLabel
    global configureApps
    configureApps = cA
    blacklist = bl
    # Initializing all the widgets
    configureApps.configure(state="disabled")
    
    configurator = customtkinter.CTkToplevel(app)
    configurator.title("Blacklist Config")
    configurator.geometry("300x300")
    configurator.protocol("WM_DELETE_WINDOW", lambda: killConfig(configurator))
    configurator.grid_columnconfigure(0, weight=1)
    
    configLabel = customtkinter.CTkLabel(configurator, text="Enter the blacklisted application's process name\nNote that the process must be open")
    configLabel.grid(columnspan=2, row=0, pady=20)

    options = gw.getAllTitles()
    options = [w for w in options if w]
    configEntryChoice = customtkinter.StringVar(value="")
    configEntry = customtkinter.CTkOptionMenu(configurator, values=options, variable=configEntryChoice, command=validateProcess)
    configEntry.grid(columnspan=2, row=1)
    
    currBlacklist = customtkinter.CTkScrollableFrame(configurator, label_anchor="nw", label_text="Current Blacklisted Proccesses:", width=300)
    currBlacklist.grid_columnconfigure(0, weight=1)
    currBlacklist.grid(columnspan=5, row=4)
    
    blLabel = customtkinter.CTkLabel(currBlacklist, text="", justify="left")
    updateBl()
    blLabel.grid(row=0, columnspan=5)
    
    feedback = customtkinter.CTkLabel(configurator, text="")
    feedback.grid(columnspan=2, row=3)
    
    configurator.focus()