"""
This example demonstrates the use of the SQLAlchemy job store.
On each run, it adds a new alarm that fires after ten seconds.
You can exit the program, restart it and observe that any previous alarms that have not fired yet
are still active. You can also give it the database URL as an argument.
See the SQLAlchemy documentation on how to construct those.
"""
import tornado.ioloop
import tornado.web
from time import localtime, strftime
import os

from datetime import datetime, timedelta
from pytz import utc
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

import i2c

#Create instance of  Atlas Device
# device = i2c.AtlasI2C()

# We are reading pH with addr = 99
# We are reading EC with addr = 100
# def readSensor(addr):
    #Set i2c Address for Atlas sensors
    # device.set_i2c_address(addr)
    # if addr==99:
    #     print("pH sensor: %s" % device.query("R"))
    # elif addr==100:
    #     print("EC sensor: %s" % device.query("R"))


def counter(timer_in_seconds):
    """
        Sets the number of seconds to run counter function

        Parameters
        ----------
        timer_in_seconds : int
            Number of seconds to run counter
        Returns
        -------
        TODO This function should be return only the calculated future time. Then it can be used in a function that
        checks if it is still in the future as the while statement does below
    """
    time_limit = datetime.now() + timedelta(seconds=timer_in_seconds)

    while time_limit > datetime.now():
        #print(time_limit-datetime.now())
        foo = True
        print('firing %s' % strftime("%A %d %b %Y %H:%M:%S", localtime()))

    return # break out and return to the calling function

def tick():
    counter(3)
    print('Counter function completed at %s' % strftime("%A %d %b %Y %H:%M:%S", localtime()))
    # readSensor(100)

def sensorTimerA():
    counter(3)
    # readSensor(99)

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(10)
}

job_defaults = {
    'coalesce' : False,
    'max_instances': 3
}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__== '__main__':
    scheduler = TornadoScheduler()
    # alarm_time = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(tick, 'interval', seconds=10)
    # scheduler.add_job(sensorTimerA, 'interval', seconds=19)
    print('To clear the alarms, delete the example.sqlite file.')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    scheduler.configure(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone=utc)
    scheduler.start()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

