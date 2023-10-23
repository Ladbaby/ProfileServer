from flask import Flask, send_file
import subprocess
import json
import argparse
from urllib.parse import quote

app = Flask(__name__)

upload = 0
download = 0
total = 1099511627776


def get_args():
    parser = argparse.ArgumentParser(description='Python file server with dynamic headers')
    parser.add_argument('--file-path', type=str, required=True, help='Path to the file to serve')
    parser.add_argument('--file-name', type=str, help='Custom display name of the profile')
    parser.add_argument('--route-path', type=str, required=True, help='URL route path')
    parser.add_argument('--port', type=int, default=18010, help='Port number for the server (default: 18010)')
    return parser.parse_args()

args = get_args()

# Function to get dynamic data from vnstat
def get_vnstat_data():
    global upload
    global download
    try:
        result = json.loads(subprocess.check_output(['vnstat', '--json']).decode('utf-8'))
        upload = result["interfaces"][0]["traffic"]["month"][0]["tx"]
        # download = result["interfaces"][0]["traffic"]["month"][0]["rx"]
        return True
    except subprocess.CalledProcessError as e:
        return None

@app.route(f'/{args.route_path}')
def serve_file():
    global args
    global upload
    global download
    global total
    file_path = args.file_path
    file_name = args.file_name
    
    # Get dynamic data from vnstat
    get_vnstat_data()
    
    # Modify the response headers
    response = send_file(file_path)

    response.headers['Subscription-Userinfo'] = f"upload={upload}; download={download}; total={total}; expire="
    if file_name:
        response.headers['content-disposition'] = f"attachment; filename*=UTF-8''{quote(file_name)}"

    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=args.port)
