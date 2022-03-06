import random
import uuid
import math

from lge.Engine import Engine
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle


class MiJuego():
    def __init__( self ):
        self.niters = 60*20
        self.nobjs = 0

        # creamos el juego
        Engine.Init( (800,600), "Demo de Canvas", (255,255,255) )

        # cargamos los recursos que usaremos
        Engine.LoadTTFFont( "monospace", 16, "../fonts/FreeMono.ttf" )

        # agregamos la barra de info
        infobar = Canvas( (0, 580), (800, 20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # un canvas para plotear y usar de piso
        ground = Canvas( (0, 0), (800, 100), "ground" )
        ground.Fill( (200,200,200) )
        ground.SetColliders()
        ground.SetTag( "ground" )
        ground.physics = Physics( 0, 0 )
        Engine.AddGObject( ground, 1 )

        # configuramos la camara
        camera = Engine.GetCamera()
        camera.SetBounds( Rectangle( (0, 0), (800, 600) ) )

        # el control central del juego
        Engine.SetOnUpdate( self.MainControl )
        Engine.ShowColliders( (255,0,0) )

    def MainControl( self, dt ):
        # abortamos con la tecla Escape
        if( Engine.KeyUp( Engine.CONSTANTS.K_ESCAPE ) ):
            Engine.Quit()

        # mostramos info
        fps = Engine.GetFPS()
        fps = "FPS: %07.2f" % fps

        ngobjs = len( Engine.GetGObject( "*" ) )
        ngobjs = "gObjs: %05d" % ngobjs

        mx, my = Engine.GetMousePosition()
        mb1, mb2, mb3 = Engine.GetMouseButtons()
        minfo = "Mouse: (%3d,%3d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

        infobar = Engine.GetGObject( "infobar" )
        infobar.Fill( (0,0,0,20) )
        infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (140, 0), "monospace", (0,0,0) )

        # agregamos nuevos objetos
        if( self.nobjs < 20 ):
            if( (self.niters % 5) == 0 ):
                if( random.random()< 0.5 ):
                    gobj = Circle( self.niters )
                else:
                    gobj = Box( self.niters )
                Engine.AddGObject( gobj, 1 )

                self.nobjs += 1

        self.niters -= 1
        if( self.niters <= 0 ): Engine.Quit()

    def Run( self ):
        import cProfile
        cProfile.run( "Engine.Run( 60 )" )


class Circle( Canvas ):
    def __init__( self, niters ):
        r = round( 5 + random.random()*25 )
        x, y = random.random()*(800-r*2), 500
        super().__init__( (x, y), (r*2, r*2), "gobj-" + uuid.uuid4().hex )
        self.DrawCircle( (r, r), r, (0,255,0,128), False )

        d = r/math.sqrt(2)
        self.SetColliders()

        vx = -50 + random.random()*50
        vy = -120
        self.physics = Physics( vx, vy )

    def OnUpdate( self, dt ):
        x1, y1, x2, y2 = self.GetRectangle().GetPoints()

        if( x2 < 0 or x2 > 800 or y2 < 0 or y2 > 600 ):
            Engine.DelGObject( self )
        else:
            self.physics.OnUpdate( dt, self )

    def OnCollision( self, dt, collisions ):
        self.physics.OnCollision( dt, self, collisions )

class Box( Canvas ):
    def __init__( self, niters ):
        w, h = round(10 + random.random()*50), round(10 + random.random()*50)
        x, y = random.random()*(800-w), 500
        super().__init__( (x, y), (w, h), "gobj-" + uuid.uuid4().hex )

        self.DrawRectangle( (0, 0), (w, h), (134,32,32,128), False )
        self.SetColliders()

        vx = -50 + random.random()*50
        vy = -120
        self.physics = Physics( vx, vy )

    def OnUpdate( self, dt ):
        x1, y1, x2, y2 = self.GetRectangle().GetPoints()

        if( x2 < 0 or x2 > 800 or y2 < 0 or y2 > 600 ):
            Engine.DelGObject( self )
        else:
            self.physics.OnUpdate( dt, self )

    def OnCollision( self, dt, collisions ):
        self.physics.OnCollision( dt, self, collisions )


class Physics():
    def __init__( self, vx, vy ):
        self.vx = vx
        self.vy = vy
        self.g  = 120
        self.e  = 0.4

    def SetSpeed( self, vx, vy):
        self.vx = vx
        self.vy = vy

    def GetSpeed( self ):
        return self.vx, self.vy

    def OnUpdate( self, dt, gobj ):
        x, y = gobj.GetPosition()
        w, h = gobj.GetSize()

        if( x + w < 0 or x > 800 or y + h < 0 or y > 600 ):
            Engine.DelGObject( self )
        else:
            x = x + self.vx*dt
            y = y + self.vy*dt
            gobj.SetPosition( x, y )
            self.vy = self.vy - self.g*dt

    def OnCollision( self, dt, gobj, collisions ):
        x, y = gobj.GetPosition()
        w, h = gobj.GetSize()

        for o, r in collisions:
            if( o.GetTag() != "ground" ): continue

            self.vy = -self.vy*self.e
            if( abs( self.vy ) < 30 ):
                x1, y1, x2, y2 = r.GetPoints()
                gobj.SetPosition( x, y2 + 1 )
                self.vx = 0
                self.vy = 0
                return

# -- show time
game = MiJuego()
game.Run()
