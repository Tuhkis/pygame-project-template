import pygame as pg
pg.init()

import sys
sys.path.append('./engine')
import engine.app as app

class Game (app.App):
    def __init__(self):
        app.App.__init__(self, (1024, 600))

if __name__ == '__main__':
    a = Game()
    a.run()
    sys.exit()

