import pygame as pg
pg.init()

import sys
sys.path.append('./engine')
import engine.app as app

if __name__ == '__main__':
    a = app.App((1024, 600))
    a.run()
    sys.exit()

