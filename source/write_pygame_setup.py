import platform
import os
import sys

windows = False
macintosh = False
linux = False

if platform.win32_ver()[0]:
    windows = True
elif platform.mac_ver()[0]:
    macintosh = True
else:
    linux = True

if windows:
    SCRAP="SCRAP = -luser32 -lgdi32"
    EXTRA=""
elif macintosh:
    SCRAP="SCRAP = -lc"
    EXTRA="sdlmain_osx src/sdlmain_osx.m $(SDL) $(DEBUG)"
else:
    SCRAP="SCRAP = -lX11"
    EXTRA=""

    
TEMPLATE = """\
SDL =  -I{INSTALL}/include/SDL -I{INSTALL}/include  -L{INSTALL}/lib -D_REENTRANT -lSDL
FONT = -I{INSTALL}/include -L{INSTALL}/lib  -lSDL_ttf
IMAGE =  -I{INSTALL}/include -L{INSTALL}/lib -lSDL_image 
PNG = -I{INSTALL}/include -L{INSTALL}/lib  -lpng -lz
JPEG = -I{INSTALL}/include -L{INSTALL}i/lib  -ljpeg
{SCRAP}

DEBUG = 

#the following modules are optional. you will want to compile
#everything you can, but you can ignore ones you don't have
#dependencies for, just comment them out

imageext src/imageext.c $(SDL) $(IMAGE) $(PNG) $(JPEG) $(DEBUG)
font src/font.c $(SDL) $(FONT) $(DEBUG)
scrap src/scrap.c $(SDL) $(SCRAP) $(DEBUG)
{EXTRA}

GFX = src/SDL_gfx/SDL_gfxPrimitives.c 
#GFX = src/SDL_gfx/SDL_gfxBlitFunc.c src/SDL_gfx/SDL_gfxPrimitives.c 
gfxdraw src/gfxdraw.c $(SDL) $(GFX) $(DEBUG)


#these modules are required for pygame to run. they only require
#SDL as a dependency. these should not be altered

base src/base.c $(SDL) $(DEBUG)
cdrom src/cdrom.c $(SDL) $(DEBUG)
color src/color.c $(SDL) $(DEBUG)
constants src/constants.c $(SDL) $(DEBUG)
display src/display.c $(SDL) $(DEBUG)
event src/event.c $(SDL) $(DEBUG)
fastevent src/fastevent.c src/fastevents.c $(SDL) $(DEBUG)
key src/key.c $(SDL) $(DEBUG)
mouse src/mouse.c $(SDL) $(DEBUG)
rect src/rect.c $(SDL) $(DEBUG)
rwobject src/rwobject.c $(SDL) $(DEBUG)
surface src/surface.c src/alphablit.c src/surface_fill.c $(SDL) $(DEBUG)
surflock src/surflock.c $(SDL) $(DEBUG)
time src/time.c $(SDL) $(DEBUG)
joystick src/joystick.c $(SDL) $(DEBUG)
draw src/draw.c $(SDL) $(DEBUG)
image src/image.c $(SDL) $(DEBUG)
overlay src/overlay.c $(SDL) $(DEBUG)
transform src/transform.c src/rotozoom.c src/scale2x.c src/scale_mmx.c $(SDL) $(DEBUG) -D_NO_MMX_FOR_X86_64
mask src/mask.c src/bitmask.c $(SDL) $(DEBUG)
bufferproxy src/bufferproxy.c $(SDL) $(DEBUG)
pixelarray src/pixelarray.c $(SDL) $(DEBUG)
_arraysurfarray src/_arraysurfarray.c $(SDL) $(DEBUG)
"""

data = TEMPLATE.format(
    INSTALL=sys.argv[1],
    EXTRA=EXTRA,
    SCRAP=SCRAP)

sys.stdout.write(data)

    
