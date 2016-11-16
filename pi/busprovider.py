from emulated_bus import EmulatedBus


def initialize_with_hardwarebus():
    try:
        import smbus
        return smbus.SMBus(1)

    except ImportError:
        return initialize_with_emulated_bus()


def initialize_with_emulated_bus():
    return EmulatedBus()


WIRED_BUS = initialize_with_hardwarebus()

