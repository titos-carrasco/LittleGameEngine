import cv2
import numpy
import pygame
import queue
import threading
import time

from lge.Canvas import Canvas
from lge.LittleGameEngine import LittleGameEngine
from lge.Rectangle import Rectangle


class WebCam(Canvas):

    def __init__(self):
        super().__init__((200, 656), (256, 144))

        self.cam = cv2.VideoCapture(0)
        # self.cam.set( cv2.CAP_PROP_POS_FRAMES, 1 )
        # self.cam.set( cv2.CAP_PROP_FRAME_WIDTH, 160 )
        # self.cam.set( cv2.CAP_PROP_FRAME_HEIGHT, 120 )

        self.queue = queue.Queue(1)
        self.running = False
        self.task = threading.Thread(target=self._TCapture, args=(), name='_TCapture')
        self.task.start()

    def _TCapture(self):
        self.running = True
        while(self.running):
            ret, frame = self.cam.read()
            if(ret):
                try:
                    self.queue.get_nowait()
                except:
                    pass

                frame = cv2.resize(frame, self.getSize(), interpolation=cv2.INTER_AREA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = numpy.rot90(frame)

                surface = pygame.surfarray.make_surface(frame)
                self.queue.put(surface)
            cv2.waitKey(10)

    # @Override
    def onUpdate(self, dt):
        if(not self.running):
            return
        try:
            surface = self.queue.get_nowait()
            self.drawSurface((0, 0), surface)
        except Exception as e:
            pass

    # @Override
    def onQuit(self):
        self.running = False
        self.task.join()
