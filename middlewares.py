class CounterState:
    def __init__(self,step):
        self.step = step


    def __next__(self):
        if self.step <= 0:
            raise StopIteration
        self.step -= 1
        return self.step

class CountDown:
    def __init__(self,steps):
        self.steps = steps

    def __iter__(self):
        return CounterState(self.steps)


data = CounterState(10)


for i in data:
    print(i)

