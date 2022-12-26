import sched 
import threading
import time

def repetirintervalo(scheduler, event, interval, add_n = 1 ,start_t = None):
    if start_t is None:
        t = time.time()
        t = t - (t % interval) + interval
    else:
        t = start_t
    for i in range(add_n):
        scheduler.enterabs(t, 0, event)
        t += interval
    scheduler.enterabs(t - interval,0, repetirintervalo, kwargs = {
        "scheduler": scheduler,
        "event": event,
        "interval": interval,
        "add_n": add_n,
        "start_t": start_t,
       })



def main(robo , interval = 290):
    scheduler = sched.scheduler(time.time, time.sleep)
    repetirintervalo(scheduler,robo, interval )
    thread =  threading.Thread(target=scheduler.run)
    thread.start()

