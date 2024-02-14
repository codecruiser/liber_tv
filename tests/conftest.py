import pytest


class BusMixin:
    def __init__(self, bus=None):
        if bus:
            self.bus = bus()

    def register_communicator(self, channel_name, callback_func):
        if self.bus:
            self.bus.register(channel_name, callback_func)

    def send_msg(self, channel, message):
        if self.bus:
            self.bus.send_msg(channel, message)


class A(BusMixin):

    counter = 0

    def callback1(self, message=None):
        self.counter *= 4

    def check_counter(self):
        return self.counter


class B(BusMixin):

    counter = 0

    def callback2(self, message=None):
        self.counter += 1

    def check_counter(self):
        return self.counter


@pytest.fixture()
def communicator_class_a():
    return A


@pytest.fixture()
def communicator_class_b():
    return B
