import platform
import os
if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"

import GameFrameWork
import StartScene
import FirstStageScene

from pico2d import *


#open_canvas(GameFrameWork.Width, GameFrameWork.Height, sync = True)
GameFrameWork.run(StartScene)
#close_canvas()