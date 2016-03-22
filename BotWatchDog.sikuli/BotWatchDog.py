APP_NAME = "Photos"
SCRENSHOTS_DIR = "/tmp/"
LOG_FILE = "/var/log/system.log"
MAX_SCREENSHOTS = 20
import shutil
import os
import time 
from threading import Timer

screenshots_taken = []
def screenshot_name():
    return "%s.png" % time.strftime("%Y%m%d-%H%M%S")


def clean_old_screenshots():
    global screenshots_taken
    indx = len(screenshots_taken)-MAX_SCREENSHOTS
    for screnshot in screenshots_taken[:indx]:
        print "-scr: %s" % screnshot
    screenshots_taken = screenshots_taken[indx:]

def take_screenshot():
    global screenshots_taken
    region = App(APP_NAME).window()
    img = capture(region)
    scr = screenshot_name()
    shutil.move(img, os.path.join(SCRENSHOTS_DIR, scr))
    print "+scr: %s" % scr
    screenshots_taken.append(scr)
    if len(screenshots_taken)>MAX_SCREENSHOTS:
        clean_old_screenshots()
    Timer(1, take_screenshot, ()).start()

Timer(1, take_screenshot, ()).start()


import org.sikuli.util.JythonHelper
JythonHelper.get().addSysPath(getBundlePath())


print getBundlePath()


from bottle import route, run, template, view
from bottle import static_file, TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(getBundlePath(), "views"))

@route('/')
@view('index')
def index():
    return dict(
        screenshots_number = len(screenshots_taken),
        screenshots_number_max = MAX_SCREENSHOTS,
        screenshot_url = "/screenshot/%s"%screenshots_taken[-1]
        )

@route('/static/<filename:re:.*>')
def server_static(filename):
    return static_file(filename, root=os.path.join(getBundlePath(), "static"))


@route('/screenshot/<filename>')
def screenshot(filename):
    return static_file(filename,SCRENSHOTS_DIR, mimetype='image/png')

@route('/screenshot/latest.png')
def screenshot_latest():
    return screenshot(screenshots_taken[-1])

run(host='localhost', port=3070)
