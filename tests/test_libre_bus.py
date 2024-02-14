from libertv.libre_bus import LibreBus


def test_singelton():
    libre_bus = LibreBus()
    libre_bus_2 = LibreBus()
    assert libre_bus is libre_bus_2


def test_inserting_communicator(communicator_class_a, communicator_class_b):
    ca = communicator_class_a(bus=LibreBus)
    cb = communicator_class_b(bus=LibreBus)
    ca.register_communicator("test", ca.callback1)
    cb.register_communicator("test", cb.callback2)
    ca.counter = 7
    cb.counter = 2

    # cb has counter which increases by 1 if message is send
    # ca has counter which reacts to cb counter multiplying by 4
    assert 2 == cb.check_counter()
    assert 7 == ca.check_counter()
    ca.send_msg("test", "stopped")
    assert 3 == cb.check_counter()
    # bounce back
    assert 28 == ca.check_counter()
