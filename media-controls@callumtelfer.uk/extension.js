'use strict';

import St from 'gi://St';
import GLib from 'gi://GLib';
import Clutter from 'gi://Clutter';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import * as ExtensionUtils from 'resource:///org/gnome/shell/misc/extensionUtils.js';
import Gio from 'gi://Gio';

export default class Extension {
    constructor() {
        this._previousButton = null;
        this._playPauseButton = null;
        this._nextButton = null;
    }

    enable() {
        this._previousButton = new PanelMenu.Button(0.0, "Media Controls: Previous", false);
        let previousIcon = new St.Icon({
            icon_name: 'media-skip-backward-symbolic',
            style_class: 'system-status-icon'
        });
        this._previousButton.add_child(previousIcon);
        this._previousButton.connect('button-press-event', () => {
            this._sendMediaCommand('Previous');
            return Clutter.EVENT_STOP;
        });

        this._playPauseButton = new PanelMenu.Button(0.0, "Media Controls: Play/Pause", false);
        let playPauseIcon = new St.Icon({
            icon_name: 'media-playback-start-symbolic',
            style_class: 'system-status-icon'
        });
        this._playPauseButton.add_child(playPauseIcon);
        this._playPauseButton.connect('button-press-event', () => {
            this._sendMediaCommand('Pause');
            return Clutter.EVENT_STOP;
        });

        this._nextButton = new PanelMenu.Button(0.0, "Media Controls: Next", false);
        let nextIcon = new St.Icon({
            icon_name: 'media-skip-forward-symbolic',
            style_class: 'system-status-icon'
        });
        this._nextButton.add_child(nextIcon);
        this._nextButton.connect('button-press-event', () => {
            this._sendMediaCommand('Next');
            return Clutter.EVENT_STOP;
        });

        Main.panel.addToStatusArea('media-controls-prev', this._previousButton, 0, 'right');
        Main.panel.addToStatusArea('media-controls-play', this._playPauseButton, 1, 'right');
        Main.panel.addToStatusArea('media-controls-next', this._nextButton, 2, 'right');
    }

    disable() {
        if (this._previousButton) {
            this._previousButton.destroy();
            this._previousButton = null;
        }
        if (this._playPauseButton) {
            this._playPauseButton.destroy();
            this._playPauseButton = null;
        }
        if (this._nextButton) {
            this._nextButton.destroy();
            this._nextButton = null;
        }
    }

    _sendMediaCommand(commandType) {
        try {
            let proc = Gio.Subprocess.new(
                ['curl', '-X', 'POST', 'http://IPHERE:5000/media/control', // IP has been redacted due to this being a dev script, not production level
                '-H', 'Content-Type: application/json', 
                '-d', `{"type":"${commandType}"}`],
                Gio.SubprocessFlags.NONE
            );
            
            console.log(`Media control command sent: ${commandType}`);
        } catch (e) {
            console.error(`Failed to execute media control command: ${e.message}`);
        }
    }
}
