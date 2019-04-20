# ThriftyField
ThriftyField is an open source alternative to the closed source FRC Field Management System(FMS). <br>
The goal of ThriftyField is to provide an easy way to manage the states of many robots at once just like the real fields to, but only with a small amount of inexpensive equipment. ThriftyField can also keep track of scores entered on tablets via the web application and can generate a near real-time audience view just like an official event.

## Main Features
These are all the main features of ThriftyField
 - Web-based field control
 - Manual scoring with tablets via the web application
 - Near real-time audience display
 - Chroma key display for using in a twitch stream
 - Completely open API that can be used for building apps and other tools to interact with the field
 - The ability to emulate an official offseason event network using the latest Driverstation protocol
 - Only requires a laptop and any router to set up

## Setup
To set up ThriftyField, you will need the following:
 - A laptop with python3 installed
 - A wireless router with at least 7 ethernet ports, or a wireless router and a network switch
 - At least 2 tablets or phones for score input
 - (Optional) Other computer(s) connected to screens or projectors for displaying the audiance display

### The Network
Due to the way that the Driverstation protocol was designed, the field network must be set to the `10.0.100.x` ip space, with `10.0.100.5` reserved for the laptop running the ThriftyField software. After the router has been configured to accomodate this, either plug all 6 alliance station ethernet cables into the router, or a network switch.

### Scoring Devices
On the scoring devices, navigate to [10.0.100.5:8080](http://10.0.100.5:8080) in firefox or chrome and tap on the **Scoring** tab at the top, then select the alliance that the divice will be inputting data for.

### Audience Diaplay
On any computer hooked up to a projector or display, navigate to [10.0.100.5:8080](http://10.0.100.5:8080) in firefox or chrome, click on the **displays** tab, then select **Main**. Next, move this window to the secondary screen and press `f11` to go into fullscreen mode. Your mouse will be hidden when interacting with this window.

### Field Control
On the field control computer, navigate to [10.0.100.5:8080](http://10.0.100.5:8080) in firefox or chrome then click on the **Field Control** tab at the top.

## Usage
The following section outlines how to set up the field and score games

### Field
The field control panel is split into two sections: Alliance station control, and Game control. 

To add teams to the current match, simply type their team number into the corresponding text box to their assigned alliance station in the top section, then click anywhere outside of the text box to save. If you would like to start a game without a specific team or alliance station, simply click the green box beside the team number to bypass the alliance station. This box will turn red to show that the station has been disabled. Click it again to re-enable it.

To start or abort a match, just click the corresponding buttons in the bottom section. ThriftyField will automatically handle the control data and networking for the robots and will follow the usual game timing and segments, along with switching between auto and teleop.

### Scoring 
By default the scoring panels are set in addition mode. Pressing any number on screen will add it to the current score. For example, pressing 5 twice will add 10 to the score.

To subtract from the score, press the **-** button to switch into subtraction mode. Make sure to press **+** when you want to start adding to the score again.

## Credits
This project would not have been possible without the [FRCture Project](https://frcture.readthedocs.io/en/latest/). Their wiki made the whole process of network programming and interacting with the Driverstation protocol much easier. 

Also, thanks to [cheesy-arena](https://github.com/Team254/cheesy-arena) by the Cheesy Poofs for the inspiration behind ThriftyField. Much of the ThriftyField codebase is ported to python from cheesy-arena or infulences by cheesy-arena's design and layout.