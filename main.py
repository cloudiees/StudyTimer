import customtkinter
import psutil
import subprocess
from playsound import playsound
import ctypes
import pygetwindow as gw
import blconfig

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Initializing the base window and sections of the window
app = customtkinter.CTk()
app.geometry("400x450")
app.title("Study Timer")
app.grid_columnconfigure(0, weight=1)

frameA = customtkinter.CTkFrame(app)
frameA.grid(row=0, pady=20)
frameA.grid_columnconfigure(0, weight=1)

frameB = customtkinter.CTkFrame(app, width=300, height=200)
frameB.grid(row=1, pady=20)
frameB.grid_columnconfigure(0, weight=1)

# Validation function to ensure numeric input for the timer configuration
def validateNum(input):
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False

# Function that switches the timer from study mode to break mode
def loopTimer():
    ppButton.configure(state="normal")
    if timerState.cget("text") == "Study Time":
        timerState.configure(text="Break Time")
        countdown(int(breakTimerEntry.get())*60)
    else:
        timerState.configure(text="Study Time")
        countdown(int(studyTimerEntry.get())*60)

# Looping function that checks for blacklisted applications
def checkBlacklist():
    for i in psutil.process_iter():
        if i.name() in blacklist:
            sendHelp.configure(text="True")
            break
        else:
            sendHelp.configure(text="False")
    app.after(1000, checkBlacklist)

# Audio spammer used to annoy the user if they are using a blacklisted app when they shouldnt
def spamEm():
    if sendHelp.cget("text") == "True" and timerState.cget("text") == "Study Time" and ppButton.cget("text") != "Unpause Timer":
        playsound("blaudio.mp3")
        app.focus()
        app.after(5000, spamEm)
    elif timer.cget("text") == "Break Time Over!":
        timerState.configure(text="Study Time")
        countdown(int(studyTimerEntry.get())*60)
    elif timerState.cget("text") == "Study Time":
        countdown(int(timer.cget("text")))
    else:
        return
    
# Popup that displays to notify user that the time is over
def finishPopup():
    playsound("timerfin.mp3")
    global popup
    ppButton.configure(state="disabled")
    if timerState.cget("text") == "Study Time":
        timer.configure(text="Study Time Over!")
        timer.grid(row=1, columnspan=2)
    else:
        timer.configure(text="Break Time Over!")
        timer.grid(row=1, columnspan=2)
    timer.update()
    popup = customtkinter.CTkToplevel(app)
    popup.protocol("WM_DELETE_WINDOW", closePopup)
    popup.geometry("200x100") 
    popup.title("Timer Ended")
    popupLabel = customtkinter.CTkLabel(popup, text="Timer Over!")
    popupLabel.pack(pady=10)
    popupButton = customtkinter.CTkButton(popup, text="Confirm", command=closePopup)
    popupButton.pack()
    popup.focus()
    if extremistCb.get() and timerState.cget("text") == "Break Time":
        playsound("extremewarning.mp3")
        app.after(10000, closePopup)

# Function that handles closing of the finish timer popup
def closePopup():
    if popup.winfo_exists():
        popup.destroy()
    timer.grid_remove()
    loopTimer()

def processKiller():
    application = ""
    for i in psutil.process_iter():
        if i.name() in blacklist:
            application = i.name()[:len(i.name())-4]
            break
    if application != "":
        cmd = "Stop-Process -Name " + application
        subprocess.run(["powershell", "-Command", cmd], capture_output=False)
        sendHelp.configure(text="False") 
    if timer.cget("text") == "Break Time Over!":
        timerState.configure(text="Study Time")
        countdown(int(studyTimerEntry.get())*60)
    elif timerState.cget("text") == "Study Time":
        countdown(int(timer.cget("text")))

# The countdown
def countdown(cd):
    # Checking if a blacklisted app is running during study time
    if cancelled.cget("text") == "T":
        return
    if sendHelp.cget("text") == "True" and timerState.cget("text") == "Study Time":
        if not extremistCb.get():
            spamEm()
        else:
            processKiller()
    # Checking if the timer is finished
    elif cd <= 0:
        timerDisp.configure(text="00:00")
        finishPopup()
    # Decrementing the timer display and the internal counter
    elif ppButton.cget("text") != "Unpause Timer":
        timer.configure(text=cd)
        m = cd // 60
        s = cd - (m * 60)
        if (not showTimerCb.get() and timerState.cget("text") == "Study Time") or timerState.cget("text") == "Break Time":
            timerDisp.configure(text='{0:02d}'.format(m) + ":" + '{0:02d}'.format(s))
            timerDisp.update()
        cd -= 1
        app.after(1000, countdown, cd)

# Starts the countdown
def startTimer():
    # Validating that the entered values
    if studyTimerEntry.get() == "" or breakTimerEntry.get() == "":
        timerInputFeedback.configure(text="Please fill out both fields", text_color="yellow")
    elif int(studyTimerEntry.get()) <= int(breakTimerEntry.get()):
        timerInputFeedback.configure(text="Please have a study time\nlonger than your break time", text_color="red")
    elif int(studyTimerEntry.get()) > 60 or int(breakTimerEntry.get()) > 60:
        timerInputFeedback.configure(text="Please keep your study/break\nperiod an hour or under", text_color="red")
    elif int(studyTimerEntry.get()) < 1 or int(breakTimerEntry.get()) < 1:
        timerInputFeedback.configure(text="Please study/take a break for longer than 0 minutes", text_color="red")
    else:
        # Starting the countdown and hiding some widgets, as well as initalizing some variables
        extremistCb.configure(state="disabled")
        configureApps.configure(state="disabled")
        checkBlacklist()
        cancelled.configure(text="F")
        destroyTimer()
        timer.configure(text=int(studyTimerEntry.get())*60)
        ppButton.configure(text="Pause Timer")
        timerState.configure(text="Study Time")
        timerState.grid(row=0, columnspan=2, pady=20)
        ppButton.grid(row=1, column=0, padx=10, pady=(0,40))
        stopButton.grid(row=1, column=1, padx=10, pady=(0,40))
        countdown(int(studyTimerEntry.get())*60)

# Displays all the timer configuration widgets
def initTimer():
    studyTimerEntry.grid(row=1, column=0, padx=10)
    breakTimerEntry.grid(row=1, column=1, padx=10)
    studyTimerEntryLabel.grid(row=0, column=0, padx=10)
    breakTimerEntryLabel.grid(row=0, column=1, padx=10)
    timerButton.grid(row=2, columnspan=2, pady=(20,0))
    timerInputFeedback.grid(row=3, columnspan=2, padx=30, pady=10)

# Hides all the timer configuration widgets
def destroyTimer():
    studyTimerEntry.grid_remove()
    breakTimerEntry.grid_remove()
    studyTimerEntryLabel.grid_remove()
    breakTimerEntryLabel.grid_remove()
    timerButton.grid_remove()
    timerInputFeedback.grid_remove()
    timerInputFeedback.configure(text="")

# Pauses/Unpauses the countdown
def pause():
    if ppButton.cget("text") == "Pause Timer":
        ppButton.configure(text="Unpause Timer")
        ppButton.update()
    else:
        ppButton.configure(text="Pause Timer")
        ppButton.update()
        countdown(int(timer.cget("text")))

# Cancels the countdown and reinitializes all the timer configuration widgets
def cancelCd():
    configureApps.configure(state="normal")
    extremistCb.configure(state="normal")
    cancelled.configure(text="T")
    app.after(10)
    timerState.configure(text="")
    timer.configure(text="")
    stopButton.grid_remove()
    ppButton.grid_remove()
    timerState.grid_remove()
    timerDisp.configure(text="")
    initTimer() 

# Hides Timer
def hideTimer():
    if timerState.cget("text") == "Study Time":
        timerDisp.configure(text="")
        timerDisp.update()

# Initializing all the widgets
reg =  app.register(validateNum)
sendHelp = customtkinter.CTkLabel(app, text="")
studyTimerEntryLabel = customtkinter.CTkLabel(frameA, text="Study Timer")
breakTimerEntryLabel = customtkinter.CTkLabel(frameA, text="Break Timer")
timerButton = customtkinter.CTkButton(frameA, text="Start Timer", command=startTimer)
studyTimerEntry = customtkinter.CTkEntry(frameA, placeholder_text="", validate="key", validatecommand=(reg,'%P'), width=60)
breakTimerEntry = customtkinter.CTkEntry(frameA, placeholder_text="", validate="key", validatecommand=(reg,'%P'), width=60)
timerInputFeedback = customtkinter.CTkLabel(frameA, text="")
timerState = customtkinter.CTkLabel(frameA, text="Study Time", font=("Helvetica", 30))
ppButton = customtkinter.CTkButton(frameA, text="Pause Timer", command=pause)
stopButton = customtkinter.CTkButton(frameA, text="Stop Timer", command=cancelCd)
timer = customtkinter.CTkLabel(frameB, text="")
timerDisp = customtkinter.CTkLabel(frameB, text="", font=("Helvetica", 70))
timerDisp.grid(columnspan=2, row=0,pady=(20,0))
cancelled = customtkinter.CTkLabel(app, text="F")
showTimerCb = customtkinter.CTkCheckBox(frameB, text="Hide timer", command=hideTimer)
extremistCb = customtkinter.CTkCheckBox(frameB, text="Extremist Mode")
showTimerCb.grid(row=2, column=0, padx=40,pady=10)
extremistCb.grid(row=2, column=1, padx=40)
configureApps = customtkinter.CTkButton(app, text="Configure Blacklisted Applications", command=lambda: blconfig.openConfigurator(configureApps, blacklist, app))
configureApps.grid(row=3)
blacklist = set()

# Running the ongoing checks and initializing the timer inputs
initTimer()
app.mainloop()