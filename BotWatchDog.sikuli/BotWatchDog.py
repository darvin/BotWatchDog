APP_NAME = "Photos"
SCRENSHOTS_DIR = "/tmp/"

import shutil
import os
import time 
from threading import Timer

screenshots_taken = []
def screenshot_name():
    return os.path.join(SCRENSHOTS_DIR, "latest-screenshot.png")

def take_screenshot():
    region = App(APP_NAME).window()
    img = capture(region)
    scr = screenshot_name()
    shutil.move(img, scr)
    screenshots_taken.append(scr)
    print(".")
    Timer(5, take_screenshot, ()).start()

Timer(1, take_screenshot, ()).start()




import time
import BaseHTTPServer
import re

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 3007 # Maybe set this to 9000.

RE_SCRENSHOT_URL = r'^\/screenshots\/.*\.png$'

def process_screenshot_request(s):
    f = open(screenshots_taken[-1], "rb") 
    s.send_response(200)
    s.send_header('Content-type',    'image/png')
    s.end_headers()
    s.wfile.write(f.read())
    f.close()


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        if (re.match(RE_SCRENSHOT_URL,s.path)):
            process_screenshot_request(s)
        else:
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write("<html><head><title>Bot Watch</title></head>")
            s.wfile.write("<body><p>This is a test.</p>")
            # If someone went to "http://something.somewhere.net/foo/bar/",
            # then s.path equals "/foo/bar/".
            s.wfile.write("<p>You accessed path: %s </p>" % (s.path))
            s.wfile.write('<img scr="%s">' % "/screenshots/latest.png")
            s.wfile.write("</body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
