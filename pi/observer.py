
class Observer:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, func):
        if func not in self.subscribers:
            self.subscribers.append(func)

    def notify(self, *args, **kwargs):
        for subscriber in self.subscribers:
            subscriber(*args, **kwargs)
