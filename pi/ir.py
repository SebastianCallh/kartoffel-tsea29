from datetime import datetime, timedelta


class IR:
    def __init__(self, navigator):
        self.navigator = navigator
        self.busy = False
        self.ir_left = 0
        self.ir_left_back = 0
        self.ir_right = 0
        self.ir_right_back = 0
        self.last_request = datetime.now()
        self.request_period = timedelta(milliseconds=1)

    def get_ir_left(self):
        return self.ir_left

    def get_ir_left_back(self):
        return self.ir_left_back

    def get_ir_right(self):
        return self.ir_right

    def get_ir_right_back(self):
        return self.ir_right_back

    def sensor_data_received(ir_left_mm, ir_right_mm, ir_right_back_mm, ir_left_back_mm):
        self.ir_left = ir_left_mm
        self.ir_right = ir_right_mm
        self.ir_right_back = ir_right_back_mm
        self.ir_left_back_mm = ir_left_back_mm
        self.busy = False
        self.navigator.sensor_data_received(ir_left_mm, ir_right_mm, ir_right_back_mm, ir_left_back_mm)

    def request_data(self):
        if not self.busy and datetime.now() - self.last_request > self.request_period:
            self.busy = True
            self.last_request = datetime.now()
            outbound.request_sensor_data()