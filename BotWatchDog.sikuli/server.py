from sikuli import *


from bottle import route, run, template, view
from bottle import static_file, TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(getBundlePath(), "views"))

_watchDog = None

@route('/')
@view('index')
def index():
    return dict(
        screenshots_number = len(_watchDog.screenshots_taken),
        screenshots_number_max = _watchDog.MAX_SCREENSHOTS,
        screenshot_url = "/screenshot/%s"%_watchDog.screenshots_taken[-1],
        crashes_amount = _watchDog.crashes_amount
        )

@route('/static/<filename:re:.*>')
def server_static(filename):
    return static_file(filename, root=os.path.join(getBundlePath(), "static"))


@route('/screenshot/<filename>')
def screenshot(filename):
    return static_file(filename,_watchDog.SCRENSHOTS_DIR, mimetype='image/png')

@route('/screenshot/latest.png')
def screenshot_latest():
    return screenshot(_watchDog.screenshots_taken[-1])

from tail import tail
@route('/tail')
def req_tail():
    f = open(_watchDog.LOG_FILE)
    result = tail(f)
    f.close()
    return result


def run_server(watchDog):
    global _watchDog
    _watchDog = watchDog
    run(host='localhost', port=3070)