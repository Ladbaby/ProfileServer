# 📄 Profile Server

A simple profile server supporting modified response header (non production) 

## Motivation

I need to serve a file with some additioinal http response header field needed to be evaluated from command line utilities. 

Since Nginx seems to be not capable of it, I wrote this simple server instead.

## Features

- Send a file when accessed via the specified route path
- The above file will be sent with a modified header, including additional fields:

    - `subscription-userinfo`

        e.g., 

        ```
        subscription-userinfo: upload=455727941; download=6174315083; total=1073741824000; expire=1671815872
        ```

    - `profile-update-interval`

        e.g.,

        ```
        profile-update-interval: 12
        ```
    
    - `content-disposition`

        e.g.,

        ```
        attachment; filename*=UTF-8''profile_name
        ```

        > the profile name supports UTF-8, which means it can even contain emoji

    - `profile-web-page-url`

## Installation

Clone this repo and install the required libraries:

```shell
pip install flask
```

Make sure you have `vnstat` installed to get the traffic data, for instance Debian:

```shell
sudo apt install vnstat
```

## Usage

See the command line options:

```shell
$ python3 main.py --help
usage: main.py [-h] --file-path FILE_PATH [--file-name FILE_NAME] [--route-path ROUTE_PATH] [--address ADDRESS] [--port PORT]
               [--total-bandwidth TOTAL_BANDWIDTH] [--expire EXPIRE] [--update-interval UPDATE_INTERVAL] [--web-url WEB_URL]

Python file server with dynamic headers

optional arguments:
  -h, --help            show this help message and exit
  --file-path FILE_PATH
                        Path to the file to serve
  --file-name FILE_NAME
                        Custom display name of the profile (support UTF-8)
  --route-path ROUTE_PATH
                        URL route path
  --address ADDRESS     Address the server will listen on
  --port PORT           Port number for the server
  --total-bandwidth TOTAL_BANDWIDTH
                        Bandwidth limit per month in byte
  --expire EXPIRE       Expire time of the profile in seconds from 00:00:00 UTC, January 1, 1970
  --update-interval UPDATE_INTERVAL
                        Profile update interval in hours
  --web-url WEB_URL     the URL to be opened via Open web page option in context menu
```

minimal example:

```shell
python3 main.py --file-path /path/to/file
```
    
