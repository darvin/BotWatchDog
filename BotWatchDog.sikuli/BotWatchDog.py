import org.sikuli.util.JythonHelper
JythonHelper.get().addSysPath(getBundlePath())

import shutil
import os
import time 
from threading import Timer

os.getenv('sdfsadf','sdf')
class BotWatchDog:
    APP_NAME = os.getenv('WATCH_DOG_APP_NAME', "Diablo III")
    SCRENSHOTS_DIR = os.getenv('WATCH_DOG_SCRENSHOTS_DIR', os.getenv('TEMP', "/tmp/"))
    LOG_FILE = os.getenv('WATCH_DOG_LOG_FILE', "/var/log/system.log")
    MAX_SCREENSHOTS = int(os.getenv('WATCH_DOG_MAX_SCREENSHOTS', "40"))
    SCREENSHOTS_TIMEOUT = int(os.getenv('WATCH_DOG_SCREENSHOTS_TIMEOUT', "2"))

    screenshots_taken = []
    crashes_amount = 0

    def screenshot_name(self):
        return "%s.png" % time.strftime("%Y%m%d-%H%M%S")


    def clean_old_screenshots(self):
        indx = len(self.screenshots_taken)-self.MAX_SCREENSHOTS
        for screnshot in self.screenshots_taken[:indx]:
            print "-scr: %s" % screnshot
            os.remove(os.path.join(self.SCRENSHOTS_DIR, screnshot))
        self.screenshots_taken = self.screenshots_taken[indx:]

    def take_screenshot(self):
        region = App(self.APP_NAME).window()
        if region is None:
            region = Screen().getBounds()
        img = capture(region)
        scr = self.screenshot_name()
        shutil.move(img, os.path.join(self.SCRENSHOTS_DIR, scr))
        print "+scr: %s" % scr
        self.screenshots_taken.append(scr)
        if len(self.screenshots_taken)>self.MAX_SCREENSHOTS:
            self.clean_old_screenshots()
        self.timer = Timer(self.SCREENSHOTS_TIMEOUT, lambda: self.take_screenshot(), ())
        self.timer.setDaemon(True)
        self.timer.start()

dog = BotWatchDog()

print """Running BotWatchDog: 
    WATCH_DOG_APP_NAME = %s
    WATCH_DOG_SCRENSHOTS_DIR = %s
    WATCH_DOG_LOG_FILE = %s
    WATCH_DOG_MAX_SCREENSHOTS = %d
    WATCH_DOG_SCREENSHOTS_TIMEOUT = %d

""" %(BotWatchDog.APP_NAME, 
    BotWatchDog.SCRENSHOTS_DIR, 
    BotWatchDog.LOG_FILE, 
    BotWatchDog.MAX_SCREENSHOTS,
    BotWatchDog.SCREENSHOTS_TIMEOUT
    )
dog.take_screenshot()



from server import run_server


run_server(dog)


