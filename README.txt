Title: Study Timer
Description: This is a simple GUI based timer that helps you study by keeping you on task and helping you get a mental rest every so often
Author: I.S.

NOTE: This application is only Windows compatible since it uses Powershell scripts.

This mini-project was made for the AppleHacks hackathon. The reason I chose a timer specifically is because sometimes I forget to take breaks while studying or working, or sometimes I take too long of breaks, this helps with that.

I actually learned quite a lot from this project, this is my first time making a GUI application with Python, despite being a 3rd year CS student... actually now that I think about it this is the first time I've made a GUI application since I got into my uni... Welp at least I have some experience now! Also I got to play around with some Powershell scripts, which taught me that actually ending a process is a massive pain in the ass, at least from what I did. Due to the way I implemented this you have to get the exact process name of what you are trying to blacklist, so uhh if you don't know how to find that then it's gg. In the future I want to figure out a way to easily allow users to select opened applications and for the program to automatically pull the process name from it. Also one thing I'm really unsatisfied with is I couldn't figure out is how to make popups actually popup over fullscreen application, so I had to change my approach to spamming the user with audio instead of popups malware style lol. Although, I'm kinda hyped that I figured out how to kill the processes correctly with Powershell scripts, I find that super cool. Customtkinter was "fun" to work with. Tbh I never really figured out how to make a coherant GUI with it, just kinda slapped things together and called it a day. However, like I said before, first time making a GUI application so it was an experience and I had a lot of fun coding it. 

Side note: If I ever revisit this program first thing I'm doing is breaking this down into modules. Like this is an unreadable mess, but since I was just learning a lot of the tools I was using I did not really have a solid picture of what I was going to make so it made it kinda difficult to effectively partition it on the spot.

Features:
    - Configuratable timer
        - Can be paused/unpaused and stopped
        - Accepts values between 1-60 (in minutes)
        - Break time must be strictly less than study time
        - If in study time timer can be hidden
    - Configuratable blacklist
        - Requires exact process names to be known
        - Process must be open when adding to blacklist
    - Blacklist usage prevention
        - During study time if a blacklisted application is open it will pause the timer and play a notification message every 5 seconds until the application is closed
        - Extremist mode
            - Extremist mode runs Powershell scripts to kill the blacklisted process
            - At the end of break time you have 10 seconds before all blacklisted processes are killed
