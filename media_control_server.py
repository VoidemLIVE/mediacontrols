# Flask server to take media control commands through HTTP POST requests
from flask import Flask, request, jsonify
import subprocess
import os
import sys
import socket
import logging
from logging.handlers import RotatingFileHandler
import ipaddress

AHK_SCRIPT_PATH = r"D:\development\AHK\media_controls\media_controls.ahk"
AUTOHOTKEY_EXE = r"C:\Program Files\AutoHotkey\v2\AutoHotkey.exe"

HOST = "0.0.0.0"
PORT = 5000
VALID_TYPES = ["Previous", "Current", "Pause", "Next"]

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "media_control_server.log")

logger = logging.getLogger("MediaControlServer")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

app = Flask(__name__)

def is_private_ip(ip_str):
    """Check if the IP address is in a private network range"""
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private or
            ip.is_loopback or
            ip == ipaddress.ip_address('127.0.0.1')
        )
    except ValueError:
        return False

@app.before_request
def limit_to_local_network():
    """Restrict access to local network devices only"""
    client_ip = request.remote_addr
    
    if not is_private_ip(client_ip):
        logger.warning(f"Rejected request from non-local IP: {client_ip}")
        return jsonify({"error": "Access denied. Only local network devices allowed."}), 403

@app.route('/media/control', methods=['POST'])
def control_media():
    if not request.is_json:
        logger.warning("Request does not contain JSON")
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    if 'type' not in data:
        logger.warning("Missing 'type' parameter in request")
        return jsonify({"error": "Missing 'type' parameter"}), 400
    
    control_type = data['type']
    
    if control_type not in VALID_TYPES:
        logger.warning(f"Invalid control type requested: {control_type}")
        return jsonify({"error": f"Invalid control type. Must be one of: {', '.join(VALID_TYPES)}"}), 400
    
    # Running the AHK script
    try:
        if not os.path.exists(AUTOHOTKEY_EXE):
            logger.error(f"AutoHotkey executable not found at: {AUTOHOTKEY_EXE}")
            return jsonify({"error": "AutoHotkey executable not found. Please update AUTOHOTKEY_EXE path in the script."}), 500
            
        logger.info(f"Executing AHK script with parameter: {control_type}")
        result = subprocess.run([AUTOHOTKEY_EXE, AHK_SCRIPT_PATH, control_type], 
                               capture_output=True, 
                               text=True, 
                               check=False)
        
        if result.returncode != 0:
            logger.error(f"AHK script execution failed: {result.stderr}")
            return jsonify({"error": f"Failed to execute media control: {result.stderr}"}), 500
        
        logger.info(f"Successfully executed media control: {control_type}")
        return jsonify({"status": "success", "message": f"Media {control_type} command sent"})
    
    except Exception as e:
        logger.exception(f"Error executing AHK script: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/status', methods=['GET'])
def status():
    """Simple status endpoint to check if server is running"""
    return jsonify({
        "status": "online",
        "autohotkey_path": AUTOHOTKEY_EXE,
        "script_path": AHK_SCRIPT_PATH
    })

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_local_ip()
    logger.info(f"Starting Media Control Server on {local_ip}:{PORT}")
    logger.info(f"AHK Script Path: {AHK_SCRIPT_PATH}")
    logger.info(f"AutoHotkey Executable: {AUTOHOTKEY_EXE}")
    
    if not os.path.exists(AUTOHOTKEY_EXE):
        logger.error(f"AutoHotkey executable not found at: {AUTOHOTKEY_EXE}")
        logger.error("Please update the AUTOHOTKEY_EXE path in the script.")
        print(f"ERROR: AutoHotkey executable not found at: {AUTOHOTKEY_EXE}")
        print("Please update the AUTOHOTKEY_EXE path in the script and try again.")
        sys.exit(1)
        
    if not os.path.exists(AHK_SCRIPT_PATH):
        logger.error(f"AHK script not found at: {AHK_SCRIPT_PATH}")
        print(f"ERROR: AHK script not found at: {AHK_SCRIPT_PATH}")
        print("Please update the AHK_SCRIPT_PATH in the script and try again.")
        sys.exit(1)
    
    print(f"=== Media Control Server ===")
    print(f"Local server URL: http://{local_ip}:{PORT}")
    print(f"To control media, send POST requests to: http://{local_ip}:{PORT}/media/control")
    print(f"Request body format: {{ \"type\": \"[Previous|Current|Pause|Next]\" }}")
    print(f"Server logs located at: {log_file}")
    
    app.run(host=HOST, port=PORT)