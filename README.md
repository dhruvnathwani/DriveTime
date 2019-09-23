# DriveTime
Get traffic information, trends, and time to leave for a destination!

Reasoning and Purpose:
I noticed that whenever I left my house for work, if I left 1 minute later, my commute became 10 minutes longer. I realized firsthand that traffic growth was exponential, and wanted to see if I could find a solution to optimize my morning commute, maximize the amount of sleep I get, and minimize the amount of time spent in traffic. So I wrote this program!

Methodology and Procedure:
This program first collects your beginning address and destination address, then asks you what time you want to arrive

It then utilizes the google maps API (Distance matrix API and geolocation API to get coordinates from user provided addresses) to calculate drive time for a future date and time, and returns when you would need to leave in order to arrive on time.

From there, the user is prompted and asked if they would like to see more traffic data and to select a traffic window

This window is a selection of how many minutes back a user wants to look at traffic data. For example, if the window is 10 minutes and the program has told the user that to arrive at 8 AM, they need to leave by 7:50 AM, the program will then query the google API for drive time with traffic for each minute before 7:50, 10 minutes back (ie. 7:40.7:41,7:42... etc). 

It will then plot the drive time for each departure time, with the goal of the program to be showing the user the optimal time to leave to avoid sitting in traffic the longest.
