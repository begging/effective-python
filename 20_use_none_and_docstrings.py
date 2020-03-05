from datetime import datetime
from time import sleep

'''
datetime.now() is only executed a single time.

Default argument values are evaluated only once per module load, which usually
happens when a program starts up.
'''
def log(message, when=datetime.now()):
    print('%s: %s' % (when, message))

log('Hi there!')
sleep(0.1)
log('Hi again!')


'''
Use None as the default keyword value and write docstrings.
'''
def log(message, when=None):
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occurred.
                Defaults to the present time.
    """
    when = datetime.now() if when is None else when
    print('%s: %s' % (when, message))

log('Hi there!')
sleep(0.1)
log('Hi again!')
