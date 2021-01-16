# YTRobinHood
Youtube porting script

# Quick and dirty edition 
Just make sure you have all the depencies installed including chrome driver which can 
be found here: https://chromedriver.chromium.org/downloads
Chrome driver is dependand on your version of chrome you can check which version of chrome
you are currently running by typing ' chrome://version ' in your chrome browser

Make sure you keep your downloads folder and links.txt in the root folder of the python file

Change the filepaths to your location for the downloads folder and you're up and running
you can awnser the login credential questions when starting or change your user and password 
to your (currently) bitchute account

you can give the scraper a youtube channel url for example ' https://www.youtube.com/c/cbsboston/videos ' 
This would take you to the video page of the channel if you dont suply a link or an incorrect link the
scraper will just start from the youtube trending page 
(!Currently there has been no work done on a lazy load for video pages so you might not get every video at this time!)

i'll fix this shortly on top of the two exceptions that plague me 
youtube descriptions can have emojis which gives an exception
and sometimes the wait fails and doesnt find the desired element for some reason 

# What i hope to add
dynamic paths on top of the user input
hopefully get this out as a standdalone tool so the less programming inclined anons can also start working with this.
