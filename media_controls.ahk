; This script controls the media playback keys using AutoHotkey v2 (https://www.autohotkey.com)
#Requires AutoHotkey v2.0

typee := "Pause"

if (A_Args.Length > 0) {
    typee := A_Args[1]
}

if (typee = "Previous") {
    SendInput "{Media_Prev}" 
} else if (typee = "Current") {
    SendInput "{Media_Play_Pause}"
} else if (typee = "Pause") {
    SendInput "{Media_Play_Pause}"
} else if (typee = "Next") {
    SendInput "{Media_Next}"
} else {
    MsgBox("Invalid type: " typee ". Valid values are 'Previous', 'Current', 'Pause', 'Next'.")
}

ExitApp