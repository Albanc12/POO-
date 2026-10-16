class Timer:
    def __init__(self, fps):
        self.fps = fps
        self.frames = 0
        self.running = False

    def start(self):
        self.frames = 0
        self.running = True

    def stop(self):
        self.running = False

    def update(self):
        if self.running:
            self.frames += 1

    @property
    def seconds(self):
        return self.frames // self.fps
