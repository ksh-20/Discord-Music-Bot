## Requirements:
1. Python Latest Version
2. Any IDE of Choice
3. Discord Account
4. ffmpeg (used for playing songs in discord)

## Installing Dependencies:
1. Install pyNaCl
```bash
pip install pyNaCl
```
2. Discord Library
```bash
pip install discord.py
```

3. For downloading yt videos
```bash
pip install youtube-dl
```

4. Discord Components
```bash
pip install discord-components
```

5. Urllib for parsing links
```bash
pip install urllib3
```

We can use the following command to view the list of installed packages in python:
```bash
pip list
``` 

## ffmpeg Installation
1. Go to https://github.com/BtbN/FFmpeg-Builds/releases and download the zip file of ffmpeg-master-latest-win64-gpl-shared.zip for windows.
2. Extract the zip file, copy the bin folder and go to c://program files and create a new folder called ffmpeg and paste it inside. 
3. Copy the path of the bin folder and go to environment variables and add new path and paste the folder path.
4. Click ok and exit.

## Use of cog files
The cog files contains the list of commands which are used to run the bot. 

## Discord Bot Setup
1. Go to https://discord.com/developers/applications and click create new application.
2. After creating an application and after customisation, turn on message content intent. Save the changes. 
3. Go to https://discordjs.guide/preparations/adding-your-bot-to-servers.html#bot-invite-links and copy the default bot link and paste it in new tab. Replace clientID and permissions.
4. ClientId can be found in OAuth2 tab and permission integer can be found in the bot tab and select Administrator as permission and the integer will be generated. 
5. After replacing clientId and permssion integer, click enter and allow the bot to join the server. 
Note: Bots can join the servers which are either owned by you or in those servers where you have privileges to add bots.

## Code 
1. Install the code as zip file and extract the folder. Open the extracted folder in the ide of choice.
2. Go to the Install dependencies section and install the necessary packages.
3. Create a text file token.txt and store the discord bot token.