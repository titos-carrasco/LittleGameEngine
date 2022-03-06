import random
import time

from lge.Engine import Engine
from lge.Canvas import Canvas


class MiJuego():
    def __init__( self ):
        self.niters = 60*20
        self.nobjs = 0

        # creamos el juego
        Engine.Init( (800,600), "Bouncing", (255,255,255) )

        # cargamos los recursos que usaremos
        Engine.LoadTTFFont( "monospace", 16, "../fonts/FreeMono.ttf" )

        # agregamos la barra de info
        infobar = Canvas( (0, 580), (800, 20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # agregamos el suelo
        ground = Canvas( (0, 0), (800, 100), "ground" )
        ground.Fill( (200,200,200) )
        ground.SetTag( "ground" )
        ground.SetColliders()
        Engine.AddGObject( ground, 1 )

        # los objetos a rebotar
        for i in range( 50 ):
            x = 50 + random.random()*700
            y = 200 + random.random()*350
            vx = -20 + random.random()*20
            vy = 0
            gobj = Objeto( x, y, vx, vy )
            Engine.AddGObject( gobj, 1 )

        # el control central del juego
        Engine.SetOnUpdate( self.MainControl )

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

    def Run( self ):
        #Engine.ShowColliders( (255,0,0) )
        Engine.EnableOnEvent( Engine.E_ON_COLLISION )
        import cProfile
        cProfile.run( "Engine.Run( 60 )" )


class Objeto(Canvas):
    def __init__( self, x, y, vx, vy ):
        super().__init__( (x,y), (20,20) )
        self.vx = vx
        self.vy = vy
        self.g = 240
        self.e = 0.5
        self.SetColliders()

    def OnUpdate( self, dt ):
        x, y = self.GetPosition()

        x  = x + self.vx*dt
        y  = y + self.vy*dt
        self.vy = self.vy - self.g*dt

        self.SetPosition( x, y )
        self.Fill( (0,255,0, 64) )

    def OnCollision( self, dt, collisions ):
        x, y = self.GetPosition()

        for gobj, rect in collisions:
            if( gobj.GetTag() != "ground" ): continue

            x1, y1, x2, y2 = rect.GetPoints()
            self.SetPosition( x, y2 + 1 )

            self.vy = -self.vy*self.e
            if( abs( self.vy ) < 30 ):
                self.vy = 0
                self.vx = 0
                self.g = 0
            break


# -- show time
game = MiJuego()
game.Run()
