import os
import inspect
import sys
import sdl2.ext

os.environ["PYSDL2_DLL_PATH"] = "include"

RESOURCES = sdl2.ext.Resources(__file__, "assets")

sdl2.ext.init()

window = sdl2.ext.Window("Hello World!", size=(640, 480))
window.show()

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
sprite = factory.from_image(RESOURCES.get_path("bandit_rue.png"))

spriterenderer = factory.create_sprite_render_system(window)
spriterenderer.render(sprite)

processor = sdl2.ext.TestEventProcessor()
processor.run(window)

sdl2.ext.quit()
