











#----------------------

import org.sikuli.util.JythonHelper
JythonHelper.get().addSysPath(getBundlePath())

import shutil
import os
import time 
from threading import Timer


import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class BotWatchDog:
    APP_NAME = os.getenv('WATCH_DOG_APP_NAME', "Diablo III")
    SCRENSHOTS_DIR = os.getenv('WATCH_DOG_SCRENSHOTS_DIR', os.getenv('TEMP', "/tmp/"))
    LOG_FILE = os.getenv('WATCH_DOG_LOG_FILE', "/var/log/system.log")
    MAX_SCREENSHOTS = int(os.getenv('WATCH_DOG_MAX_SCREENSHOTS', "30"))
    SCREENSHOTS_TIMEOUT = int(os.getenv('WATCH_DOG_SCREENSHOTS_TIMEOUT', "1"))
    SLEEP_AFTER = int(os.getenv('WATCH_DOG_SLEEP_AFTER', "60"))


    screenshots_taken = []
    crashes_amount = 0

    def screenshot_name(self):
        return "%s_%s.png" % (time.strftime("%Y_%m_%d-%H_%M_%S"), id_generator(6))


    def clean_old_screenshots(self, number_max=-1):
        if number_max==-1:
            number_max = self.MAX_SCREENSHOTS
        indx = len(self.screenshots_taken)-number_max

        scrs_to_remove = self.screenshots_taken[:indx]
        self.screenshots_taken = self.screenshots_taken[indx:]
        # print "after ", self.screenshots_taken, " removed: ", scrs_to_remove

        for screnshot in scrs_to_remove:
            print "-scr: %s" % screnshot
            os.remove(os.path.join(self.SCRENSHOTS_DIR, screnshot))

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
        if time.time() < self.sleep_after_timestamp:
            self.timer = None
            self._setTimer()
        else:
            self.timer = None
            self.clean_old_screenshots(1)

    def _setTimer(self):
        if self.timer is None:
            self.timer = Timer(self.SCREENSHOTS_TIMEOUT, lambda: self.take_screenshot(), ())
            self.timer.setDaemon(True)
            self.timer.start()

    def wake(self):
        self.sleep_after_timestamp = time.time() + self.SLEEP_AFTER
        self.take_screenshot()

dog = BotWatchDog()

print """Running BotWatchDog: 
    WATCH_DOG_APP_NAME = %s
    WATCH_DOG_SCRENSHOTS_DIR = %s
    WATCH_DOG_LOG_FILE = %s
    WATCH_DOG_MAX_SCREENSHOTS = %d
    WATCH_DOG_SCREENSHOTS_TIMEOUT = %d
    WATCH_DOG_SLEEP_AFTER = %d

""" %(BotWatchDog.APP_NAME, 
    BotWatchDog.SCRENSHOTS_DIR, 
    BotWatchDog.LOG_FILE, 
    BotWatchDog.MAX_SCREENSHOTS,
    BotWatchDog.SCREENSHOTS_TIMEOUT,
    BotWatchDog.SLEEP_AFTER
    )
dog.wake()



from server import run_server


run_server(dog)


