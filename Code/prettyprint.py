import itertools
import time
import sys
import threading

global done, start_time, text

done = False

# From: https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running
def animate():
    global done, start_time, text

    while True:
        if done:
            break
        sys.stdout.write('\r' + text + " [Time Elapsed: {:4f} seconds]".format((time.time() - start_time)) + '\t')
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\r' + text + " [Time Elapsed: {:4f} seconds]".format((time.time() - start_time)) + ' - done!     \t')

# Call this to stop the whole shindig :)
def stop_animation():
    global done
    done = True
    time.sleep(0.3)
    print()

# Call this to start the print
def start_animation(text1 = ""):
    global done, start_time, text
    start_time = time.time()
    text = text1
    done = False
    t = threading.Thread(target=animate)
    t.start()

# Call this to change the print's text -> "new text" + [time elapsed: time] |
def set_text(text1):
    global text
    text = text1