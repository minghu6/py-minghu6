# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

import minghu6.io.alarm as alarm
import time
def test_alarm():
    def test1():
        alarm.alarm(2)
        time.sleep(1)
        return True
    def test2():
        alarm.alarm(1)
        time.sleep(2)

    assert test1()

    try:
        test2()
    except TimeoutError:
        pass

    print('timeout')



if __name__ == '__main__':
    test_alarm()
