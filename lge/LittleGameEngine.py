from glob import glob
import re
import pygame

from lge.Camera import Camera
from lge.Rectangle import Rectangle


class LittleGameEngine():
    CONSTANTS = pygame.constants
    VLIMIT = 0xFFFFFFFF
    GUI_LAYER = 0xFFFF
    E_ON_DELETE = 0b00000001
    E_ON_START = 0b00000010
    E_ON_PRE_UPDATE = 0b00000100
    E_ON_UPDATE = 0b00001000
    E_ON_POST_UPDATE = 0b00010000
    E_ON_COLLISION = 0b00100000
    E_ON_PRE_RENDER = 0b01000000
    E_ON_QUIT = 0b10000010

    lge = None

    # ------ game engine ------
    def __init__(self, camSize, title, bgColor):
        assert LittleGameEngine.lge is None, "LittleGameEngine ya se encuentra activa"
        LittleGameEngine.lge = self

        self.fps_data = [0]*30
        self.fps_idx = 0

        self.running = False
        self.on_main_update = None
        self.on_events_enabled = 0x00

        self.bgColor = bgColor
        self.collidersColor = None

        self.fonts = {}
        self.sounds = {}
        self.images = {}

        self.gObjects = {}
        self.gLayers = {}
        self.gObjectsToAdd = []
        self.gObjectsToDel = []

        self.camera = Camera((0, 0), camSize)

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.key.set_repeat(0)
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode(camSize)

        self.mouse_buttons = pygame.mouse.get_pressed()
        self.mouse_position = pygame.mouse.get_pos()
        self.mouse_clicked = [0]*len(self.mouse_buttons)
        self.keys_pressed = pygame.key.get_pressed()

    def GetLGE():
        return LittleGameEngine.lge

    def GetFPS(self):
        dt = 0.0
        for val in self.fps_data:
            dt += val
        dt = dt / len(self.fps_data)
        return 0 if dt == 0 else 1/dt

    def ShowColliders(self, color):
        self.collidersColor = color

    def SetOnEvents(self, on_events_enabled):
        self.on_events_enabled = on_events_enabled

    def SetOnMainUpdate(self, func):
        self.on_main_update = func

    def Quit(self):
        self.running = False

    def Run(self, fps):
        clock = pygame.time.Clock()
        self.running = True
        while(self.running):
            # events
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.running = False
                elif(event.type == pygame.MOUSEMOTION):
                    self.mouse_buttons = pygame.mouse.get_pressed()
                    self.mouse_position = pygame.mouse.get_pos()
                elif(event.type == pygame.MOUSEBUTTONDOWN):
                    self.mouse_buttons = pygame.mouse.get_pressed()
                    self.mouse_position = pygame.mouse.get_pos()
                    self.mouse_clicked[event.button - 1] = self.mouse_position
                elif(event.type == pygame.MOUSEBUTTONUP):
                    self.mouse_buttons = pygame.mouse.get_pressed()
                    self.mouse_position = pygame.mouse.get_pos()
                    pos = self.mouse_clicked[event.button - 1]
                    if(isinstance(pos, tuple)):
                        if(pos[0] == self.mouse_position[0] and pos[1] == self.mouse_position[1]):
                            self.mouse_clicked[event.button - 1] = 1
                        else:
                            self.mouse_clicked[event.button - 1] = 0

            self.keys_pressed = pygame.key.get_pressed()

            # --- tiempo en ms desde el ciclo anterior
            dt = clock.tick(fps)/1000.0
            self.fps_data[self.fps_idx] = dt
            self.fps_idx += 1
            self.fps_idx %= len(self.fps_data)

           # --- Del gobj and gobj.OnDelete
            ondelete = []
            for gobj in self.gObjectsToDel:
                self.gObjects[gobj.name].remove()
                gLayers[gobj.layer].remove(gobj)
                if(self.camera.target == gobj):
                    self.camera.target = None
                if((self.on_events_enabled & LittleGameEngine.E_ON_DELETE) and (gobj.on_events_enabled & LittleGameEngine.E_ON_DELETE)):
                    self.ondelete.append(gobj)
            self.gObjectsToDel = []
            for gobj in ondelete:
                gobj.OnDelete()
            del ondelete

            # --- Add Gobj and gobj.OnStart
            reorder = False
            onstart = []
            for gobj in self.gObjectsToAdd:
                layer = gobj.layer
                if(not layer in self.gLayers):
                    self.gLayers[layer] = []
                    reorder = True
                gobjs = self.gLayers[layer]
                if(not gobj in gobjs):
                    self.gLayers[gobj.layer].append(gobj)
                    if((self.on_events_enabled & LittleGameEngine.E_ON_START) and (gobj.on_events_enabled & LittleGameEngine.E_ON_START)):
                        onstart.append(gobj)
            self.gObjectsToAdd = []
            for gobj in onstart:
                gobj.OnStart()
            del onstart

            # ---
            if(reorder):
                self.gObjects = dict(sorted(self.gObjects.items()))
                reorder = False
            # --

            # --- gobj.OnPreUpdate
            if(self.on_events_enabled & LittleGameEngine.E_ON_PRE_UPDATE):
                list(gobj.OnPreUpdate(dt)
                        for layer, gobjs in self.gLayers.items()
                            for gobj in gobjs
                                if gobj.on_events_enabled & LittleGameEngine.E_ON_PRE_UPDATE
                     )

            # --- gobj.OnUpdate
            if(self.on_events_enabled & LittleGameEngine.E_ON_UPDATE):
                list(gobj.OnUpdate(dt)
                        for layer, gobjs in self.gLayers.items()
                            for gobj in gobjs
                                if gobj.on_events_enabled & LittleGameEngine.E_ON_UPDATE
                     )

            # --- gobj.OnPostUpdate
            if(self.on_events_enabled & LittleGameEngine.E_ON_POST_UPDATE):
                list(gobj.OnPostUpdate(dt)
                        for layer, gobjs in self.gLayers.items()
                            for gobj in gobjs
                                if gobj.on_events_enabled & LittleGameEngine.E_ON_POST_UPDATE
                     )

            # --- game.OnUpdate
            if(self.on_main_update):
                self.on_main_update(dt)

            # --- gobj.OnCollision
            if(self.on_events_enabled & LittleGameEngine.E_ON_COLLISION):
                oncollisions = []
                for layer, gobjs in self.gLayers.items():
                    if(layer == LittleGameEngine.GUI_LAYER):
                        continue
                    with_use_colliders = list( [gobj for gobj in gobjs if gobj.use_colliders ] )
                    with_on_collision  = list( [gobj for gobj in with_use_colliders if gobj.on_events_enabled & LittleGameEngine.E_ON_COLLISION ] )

                    for o1 in with_on_collision:
                        colliders = []
                        for o2 in with_use_colliders:
                            if o1 != o2:
                                if o1.rect.Intersects( o2.rect ):
                                    colliders.append(o2)
                        oncollisions.append((o1, colliders))
                list(gobj.OnCollision(dt, colliders)
                        for gobj, colliders in oncollisions
                            if colliders
                    )
                del oncollisions

            # --- gobj.OnPreRender
            if(self.on_events_enabled & LittleGameEngine.E_ON_PRE_RENDER):
                list(gobj.OnPreRender(dt)
                        for layer, gobjs in self.gLayers.items()
                            for gobj in gobjs
                                if gobj.on_events_enabled & LittleGameEngine.E_ON_PRE_RENDER
                     )

            # --- Camera Tracking
            self.camera.FollowTarget()

            # --- Rendering
            self.screen.fill(self.bgColor)

            # layers
            for layer, gobjs in self.gLayers.items():
                if(layer != LittleGameEngine.GUI_LAYER):
                    for gobj in [gobj for gobj in gobjs if(gobj.rect.Intersects(self.camera.rect))]:
                        x, y = self.Fix_XY(gobj)
                        if(gobj.surface != None):
                            self.screen.blit(gobj.surface, (x, y))

                        if(self.collidersColor and gobj.use_colliders):
                            pygame.draw.rect(self.screen, self.collidersColor, pygame.Rect((x, y), (gobj.rect.width, gobj.rect.height)), 1)

            # GUI
            for layer, gobjs in self.gLayers.items():
                if(layer == LittleGameEngine.GUI_LAYER):
                    for gobj in gobjs:
                        if(gobj.surface != None):
                            x, y = gobj.GetPosition()
                            w, h = gobj.GetSize()
                            self.screen.blit(gobj.surface, (x, self.camera.rect.height-y-h))

            # ---
            pygame.display.update()

        # --- gobj.OnQuit
        if(self.on_events_enabled & LittleGameEngine.E_ON_QUIT):
            list(gobj.OnQuit()
                    for layer, gobjs in self.gLayers.items()
                        for gobj in gobjs
                            if gobj.on_events_enabled & LittleGameEngine.E_ON_QUIT
                 )

        # eso es todo
        pygame.quit()

    # sistema cartesiano y zona visible dada por la camara
    def Fix_XY(self, gobj):
        xo = gobj.rect.x
        yo = gobj.rect.y
        #wo = gobj.rect.width
        ho = gobj.rect.height

        wh = LittleGameEngine.VLIMIT

        vx = self.camera.rect.x
        vy = self.camera.rect.y
        #vw = self.camera.rect.width
        vh = self.camera.rect.height

        dy = wh - (vy + vh)
        x = xo - vx
        y = wh - (yo + ho) - dy

        return x, y

    # ------ gobjects ------
    def AddGObject(self, gobj, layer):
        assert gobj.layer < 0, "'gobj' ya fue agregado"
        assert layer >= 0 and layer <= LittleGameEngine.GUI_LAYER, "'layer' invalido"
        gobj.layer = layer
        self.gObjects[gobj.name] = gobj
        self.gObjectsToAdd.append(gobj)

    def AddGObjectGUI(self, gobj):
        self.AddGObject(gobj, LittleGameEngine.GUI_LAYER)

    def GetGObject(self, name):
        return self.gObjects[name]

    def GetCountGObjects(self):
        return len(self.gObjects)

    def GetGObjects(self, pattern=None):
        if(pattern == None):
            return list(self.gObjects.values())

        pattern = pattern.replace("*", ".*")
        return [gobj for gobj in gObjects if not re.match(pattern, gobj.name) is None]

    def DelGObject(self, gobj):
        assert gobj.layer >= 0, "'gobj' no ha sido agregado"
        self.gObjectsToDel.append(gobj)

    def DelGObjectByPattern(pattern):
        pattern = pattern.replace("*", ".*")
        for gobj in gObjects:
            if not re.match(pattern, gobj.name) is None:
                self.DelGObject(gobj)

    def IntersectGObjects(self, gobj):
        if(gobj.use_collider):
            return [o for o in gObjects if o != gobj and o.use_colliders and gobj.rect.Intersects(o.rect)]
        else:
            return []

    # ------ camera ------
    def GetCameraPosition(self):
        return self.camera.GetPosition()

    def GetCameraSize(self):
        return self.camera.GetSize()

    def SetCameraTarget(self, gobj, center=True):
        assert gobj.layer >= 0, "'gobj' no ha sido agregado"
        assert gobj.layer != LittleGameEngine.GUI_LAYER, "'gobj' invalido"

        self.camera.target = gobj
        self.camera.target_center = center

    def SetCameraBounds(self, bounds):
        self.camera.SetBounds(bounds)

    def SetCameraPosition(self, x, y):
        self.camera.SetPosition(x, y)

    # ------ keys ------
    def KeyPressed(self, key):
        return self.keys_pressed[key]

    # ------ mouse ------
    def GetMouseButtons(self):
        return self.mouse_buttons

    def GetMousePosition(self):
        x, y = self.mouse_position
        wh = self.camera.rect.height
        return x, wh - y - 1

    def GetMouseClicked(self, button):
        r = self.mouse_clicked[button]
        if(r == 1):
            self.mouse_clicked[button] = 0
            return True
        else:
            return False

    # ------ fonts ------

    def GetSysFonts(self):
        return pygame.font.get_fonts()

    def LoadSysFont(self, name, size, bold=False, italic=False):
        if(not name in self.fonts):
            font = pygame.font.SysFont(name, size, bold, italic)
            self.fonts[name] = font

    def LoadTTFFont(self, name, path, size):
        if(not name in self.fonts):
            font = pygame.font.Font(path, size)
            self.fonts[name] = font

    def GetFont(self, fname):
        return self.fonts[fname]

    # ------ sounds ------
    def LoadSound(self, name, fname):
        self.sounds[name] = pygame.mixer.Sound(fname)

    def PlaySound(self, name, loop, level):
        if(loop):
            loop = -1
        else:
            loop = 0
        self.sounds[name].set_volume(level/100)
        self.sounds[name].play(loop)

    def StopSound(self, name):
        self.sounds[name].stop()

    def SetSoundVolume(self, name, level):
        self.sounds[name].set_volume(level/100)

    def GetSoundVolume(self, name):
        return self.sounds[name].get_volume()*100

    #  ------ images ------
    def CreateOpaqueImage(self, width, height):
        return pygame.Surface((width, height))

    def CreateTranslucentImage(self, width, height):
        return pygame.Surface((width, height), pygame.SRCALPHA)

    def GetImages(self, iname):
        return [image for image in self.images[iname]]

    def LoadImage(self, iname, pattern, scale=None, flip=None):
        if("*" in pattern):
            fnames = sorted(glob(pattern))
        else:
            fnames = [pattern]

        if(flip):
            fx, fy = flip
        surfaces = []
        for fname in fnames:
            surface = pygame.image.load(fname).convert_alpha()
            if(scale):
                if(not isinstance(scale, tuple)):
                    w, h = surface.get_size()
                    scale = (int(w*scale), int(h*scale))
                surface = pygame.transform.smoothscale(surface, scale)
            if(flip):
                surface = pygame.transform.flip(surface, fx, fy)
            surfaces.append(surface)
        self.images[iname] = surfaces
