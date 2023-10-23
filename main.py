from flask import Flask, send_file
import subprocess
import json
import argparse
from urllib.parse import quote

app = Flask(__name__)

def get_args():
    parser = argparse.ArgumentParser(description='Python file server with dynamic headers')
    parser.add_argument('--file-path', type=str, required=True, help='Path to the file to serve')
    parser.add_argument('--file-name', type=str, help='Custom display name of the profile (support UTF-8)')
    parser.add_argument('--route-path', type=str, default='', help='URL route path')
    parser.add_argument('--address', type=str, default='127.0.0.1', help='Address the server will listen on')
    parser.add_argument('--port', type=int, default=18010, help='Port number for the server')
    parser.add_argument('--total-bandwidth', type=int, default=1099511627776, help='Bandwidth limit per month in byte')
    parser.add_argument('--expire', type=int, default=None, help='Expire time of the profile in seconds from 00:00:00 UTC, January 1, 1970')
    parser.add_argument('--update-interval', type=int, help='Profile update interval in hours')
    parser.add_argument('--web-url', type=str, help='the URL to be opened via Open web page option in context menu')
    return parser.parse_args()

args = get_args()

# Function to get dynamic data from vnstat
def get_vnstat_data():
    try:
        result = json.loads(subprocess.check_output(['vnstat', '--json']).decode('utf-8'))
        upload = result["interfaces"][0]["traffic"]["month"][0]["tx"]
        # note: Vultr only calculate outbound traffic, thus rx not used
        # download = result["interfaces"][0]["traffic"]["month"][0]["rx"]
        download = 0
        return upload, download
    except subprocess.CalledProcessError as e:
        return None, None

@app.route(f'/{args.route_path}')
def serve_file():
    global args
    
    # Get dynamic data from vnstat
    upload, download = get_vnstat_data()
    
    # Modify the response headers
    response = send_file(args.file_path)

    if (upload and download) is not None:
        response.headers['subscription-userinfo'] = f"upload={upload}; download={download}; total={args.total_bandwidth}; expire={args.expire or ''}"
        if args.file_name:
            response.headers['content-disposition'] = f"attachment; filename*=UTF-8''{quote(args.file_name)}"
        if args.update_interval:
            response.headers['profile-update-interval'] = f"{args.update_interval}"
        if args.web_url:
            response.headers['profile-web-page-url'] = args.web_url

    return response

if __name__ == '__main__':
    app.run(host=args.address, port=args.port)
