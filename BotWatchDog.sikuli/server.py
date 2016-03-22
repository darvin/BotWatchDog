from sikuli import *


from bottle import route, run, template, view
from bottle import static_file, TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(getBundlePath(), "views"))

_watchDog = None

@route('/')
@view('index')
def index():
    _watchDog.wake()
    return dict(
        screenshots_number = len(_watchDog.screenshots_taken),
        screenshots_number_max = _watchDog.MAX_SCREENSHOTS,
        screenshot = _watchDog.screenshots_taken[-1],
        crashes_amount = _watchDog.crashes_amount
        )

@route('/static/<filename:re:.*>')
def server_static(filename):
    return static_file(filename, root=os.path.join(getBundlePath(), "static"))


@route('/screenshot/<filename>')
def screenshot(filename):
    _watchDog.wake()
    return static_file(filename,_watchDog.SCRENSHOTS_DIR, mimetype='image/png')

@route('/screenshot/latest.png')
def screenshot_latest():
    return screenshot(_watchDog.screenshots_taken[-1])

@route('/screenshot/<filename>/previous/<index>')
def screenshot_previous(filename, index):
    try:
        i = _watchDog.screenshots_taken.index(filename)
    except ValueError:
        i = 0
    i -= int(index)
    if i < 0:
        i = len(_watchDog.screenshots_taken)-1
    return screenshot(_watchDog.screenshots_taken[i])


from tail import tail
@route('/tail')
def req_tail():
    _watchDog.wake()
    f = open(_watchDog.LOG_FILE)
    if (f):
        result = tail(f)
        f.close()
        return result
    else:
        return ""


def run_server(watchDog):
    global _watchDog
    _watchDog = watchDog
    run(host='0.0.0.0', port=3070)