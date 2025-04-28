' This script starts a Python media control server using VBScript. It creates a hidden command window.
Option Explicit

Dim pythonScriptPath
pythonScriptPath = "media_control_server.py" ' Path to the python script here

Dim pythonExe
pythonExe = "python"  '


Dim WshShell
Set WshShell = CreateObject("WScript.Shell")

WshShell.CurrentDirectory = "D:\development\AHK\media_controls"

WshShell.Run pythonExe & " """ & pythonScriptPath & """", 0, False

Set WshShell = Nothing