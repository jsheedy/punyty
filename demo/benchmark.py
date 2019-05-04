import time


class Benchmark():
    def __init__(self, renderer, n_frames=30):
        self.renderer = renderer
        self.t0 = time.time()
        self.n_frames = n_frames

    def update(self, t):
        if self.renderer.frame % self.n_frames == 0:
            dt = t - self.t0
            self.t0 = t
            fps = self.n_frames / dt
            return f'fps: {fps:.2f}'
