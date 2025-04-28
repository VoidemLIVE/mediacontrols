# MediaControls

A simple development project that I created to let me change my current playing media on my main pc, whilst using my Ubuntu development machine.

Inside `media-controls@callumtelfer.uk`, is the code for the Ubuntu shell extension that allows you to control the media player from the top bar.

`media_control_server.py`, `media_controls.ahk`, and `start_media_server.vbs` all should be on the Windows machine. `start_media_server.vbs` is the script that runs the Python server, so should have a shortcut placed in the startup folder.

On line 76 of `media-controls@callumtelfer.uk/extension.js`, you will need to change the IP address to the IP of your windows machine.

On line 11, 12 of `media_control_server.py`, you will need to change the paths for your corresponding files.