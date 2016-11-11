"""
As the robot will move autonomously it is crucial that it can be stopped both
fast and reliably in case of a failure. This class serves to mitigate possible
errors and provides means for externally aborting the operation of the robot.
"""
import signal

import sys
import traceback

from outbound import set_motor_speed


class Safety:
    @staticmethod
    def setup_terminal_abort():
        signal.signal(signal.SIGINT, Safety.handle_abort)

    @staticmethod
    def handle_abort():
        # Stop motors to avoid robot running amok
        set_motor_speed(0)
        sys.exit(0)

    @staticmethod
    def run_safely(func):
        # Wrap entire program after the motors has been started in a try-catch
        # to avoid risking not being able to shut down the robot remotely in
        # case of a failure.
        try:
            func()
        except:
            set_motor_speed(0)
            traceback.print_exc()

            sys.exit(0)
