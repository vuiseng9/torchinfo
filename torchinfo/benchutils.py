from functools import wraps
import time
from collections import OrderedDict
DUMP_MODELSUMMARY = False
DUMP_MODEL_ARCH = True

stats=[]

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        global stats
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        stats.append({func.__qualname__:total_time})
        # print(f'Function {func.__qualname__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

def report_timeit_stats():
    global stats
    print('-'*100)
    for e in stats:
        for k, v in e.items():
            print("{:10.3f} ms | {}".format(v*1000, k))
    print('-'*100)

class StopWatch:
    def __init__(self) -> None:
        self.enable()
        self.__call__()
    
    def reset(self):
        self._previous_ts = None
        self._triggered = False
        self.entry = OrderedDict()
    
    def disable(self):
        self._enable = False
    
    def enable(self):
        self._enable = True
        self.reset()

    def __call__(self, delta_label=None):
        if self._triggered is False:
            self._triggered = True
            self._previous_ts = time.perf_counter()
            return
        
        if delta_label is None:
            raise ValueError("logical error, your stopwatch call should be active and provide a label for each subsequent call")
        else:
            self._current_ts = time.perf_counter()
            self.entry[delta_label] = self._current_ts - self._previous_ts
            self._previous_ts = self._current_ts

    def report(self):
        e2e = 0.0
        for label, delta in self.entry.items():
            print("{:10.3f} ms | {}".format(delta*1000, label))
            e2e += delta

        print("{:10.3f} ms | {}".format(e2e*1000, "End-to-End"))