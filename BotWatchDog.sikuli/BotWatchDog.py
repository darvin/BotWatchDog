import org.sikuli.util.JythonHelper
JythonHelper.get().addSysPath(getBundlePath())

import shutil
import os
import time 
from threading import Timer


class BotWatchDog:
    APP_NAME = "Photos"
    SCRENSHOTS_DIR = "/tmp/"
    LOG_FILE = "/var/log/system.log"
    MAX_SCREENSHOTS = 20

    screenshots_taken = []
    crashes_amount = 0

    def screenshot_name(self):
        return "%s.png" % time.strftime("%Y%m%d-%H%M%S")


    def clean_old_screenshots(self):
        indx = len(self.screenshots_taken)-self.MAX_SCREENSHOTS
        for screnshot in self.screenshots_taken[:indx]:
            print "-scr: %s" % screnshot
        self.screenshots_taken = self.screenshots_taken[indx:]

    def take_screenshot(self):
        region = App(self.APP_NAME).window()
        img = capture(region)
        scr = self.screenshot_name()
        shutil.move(img, os.path.join(self.SCRENSHOTS_DIR, scr))
        print "+scr: %s" % scr
        self.screenshots_taken.append(scr)
        if len(self.screenshots_taken)>self.MAX_SCREENSHOTS:
            self.clean_old_screenshots()
        Timer(1, lambda: self.take_screenshot(), ()).start()

dog = BotWatchDog()
dog.take_screenshot()



from server import run_server


run_server(dog)


