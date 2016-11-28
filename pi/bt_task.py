class BT_task:
    """
    Class for packing command ID and data when sending
    commands and corresponding answers over Bluetooth.
    """

    def __init__(self, cmd_id=0, data=0):
        self.cmd_id = int(cmd_id)
        self.data = data
