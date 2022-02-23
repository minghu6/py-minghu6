
from minghu6.etc.cmd import CommandRunner

def test_cmd_realtime_run():
    #cmd = 'ffmpeg -i test.mp4 -c:v libx265 output.mp4'
    cmd = 'find ~/coding/Go -name a -print'
    CommandRunner.realtime_run(cmd)



if __name__ == '__main__':

    test_cmd_realtime_run()
