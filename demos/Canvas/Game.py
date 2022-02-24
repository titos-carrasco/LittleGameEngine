from random import random
from uuid import uuid4

from lge.Engine import Engine
from lge.Canvas import Canvas
from lge.Rect import Rect


class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (800,600), "Demo de Canvas", (255,255,255) )

        # cargamos los recursos que usaremos
        Engine.LoadTTFFont( "monospace", 16, "../fonts/FreeMono.ttf" )

        # agregamos la barra de info
        infobar = Canvas( (0,580), (800,20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # un canvas para plotear
        ground = Canvas( (0,0), (800,100), "ground" )
        ground.Fill( (200,200,200) )
        ground.SetColliders( True )
        Engine.AddGObject( ground, 1 )

        # configuramos la camara
        camera = Engine.GetCamera()
        camera.SetBounds( Rect( (0,0), (800,600) ) )

        # el control central del juego
        Engine.SetOnUpdate( self.MainControl )

        #Engine.ShowColliders( (255,0,0) )

    def MainControl( self, dt ):
        # abortamos con la tecla Escape
        if( Engine.IsKeyDown( Engine.CONSTANTS.K_ESCAPE ) ):
            Engine.Quit()

        # mostramos info
        fps = Engine.GetFPS()
        fps = "FPS: %07.2f" % fps

        ngobjs = len( Engine.GetGObject( "*") )
        ngobjs = "gObjs: %03d" % ngobjs

        mx, my = Engine.GetMousePos()
        mb1, mb2, mb3 = Engine.GetMousePressed()
        minfo = "Mouse: (%3d,%3d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

        infobar = Engine.GetGObject( "infobar" )
        infobar.Fill( (0,0,0,20) )
        infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (140,0), "monospace", (0,0,0) )

        #
        ground = Engine.GetGObject( "ground" )

        # agregamos nuevos objetos
        mx, my = Engine.GetMousePos()
        mb1, mb2, mb3 = Engine.GetMousePressed()

        if( Engine.IsKeyUp( Engine.CONSTANTS.K_p ) ):
            x, y = int(random()*800), int(random()*100)
            for i in range( 50 ):
                dx, dy = -10 + int(random()*20), -10 - int(random()*20)
                ground.DrawPoint( (x+dx,y+dy), (255,0,0) )
        elif( Engine.IsKeyUp( Engine.CONSTANTS.K_c ) ):
            gobj = Circle()
            Engine.AddGObject( gobj, 1 )
        elif( Engine.IsKeyUp( Engine.CONSTANTS.K_b ) ):
            gobj = Box()
            Engine.AddGObject( gobj, 1 )
        elif( Engine.IsKeyUp( Engine.CONSTANTS.K_l ) ):
            pass
        elif( Engine.IsKeyUp( Engine.CONSTANTS.K_d ) ):
            Engine.DelGObject( "gobj-*" )
            ground.Fill( (200,200,200) )


    def Run( self ):
        Engine.Run( 60 )

class Circle( Canvas ):
    def __init__( self ):
        r = round( 5 + random()*25 )
        x, y = random()*(800-r*2), 100 + random()*500
        super().__init__( (x,y), (r*2,r*2), "gobj-" + uuid4().hex )
        self.DrawCircle( (r,r), r, (0,255,0,128), False )
        self.SetColliders( True )
        self.vx = 0
        self.vy = 120

    def OnUpdate( self, dt ):
        x, y = self.GetPosition()
        y = y - self.vy*dt
        self.SetPosition( (x,y) )

    def OnPostUpdate( self, dt ):
        x, y = self.GetPosition()
        gnd = Engine.GetGObject( "ground" )
        if( self.GetRect().CollideRect( gnd.GetRect() ) ):
            ox, oy = gnd.GetPosition()
            ow, oh = gnd.GetSize()
            y = oy + oh
            self.SetPosition( (x,y) )
            if( self.vy > -60 and self.vy < 60 ):
                self.vy = 0
            else: self.vy = -self.vy/3
        else:
            self.vy = self.vy + 4

class Box( Canvas ):
    def __init__( self ):
        w, h = round(10 + random()*50), round(10 + random()*50)
        x, y = random()*(800-w), 100 + random()*500
        super().__init__( (x,y), (w,h), "gobj-" + uuid4().hex )
        self.DrawRectangle( (0,0), (w,h), (134,32,32,128), False )
        self.SetColliders( True )
        self.vx = 0
        self.vy = 240

    def OnUpdate( self, dt ):
        x, y = self.GetPosition()
        y = y - self.vy*dt
        self.SetPosition( (x,y) )

    def OnPostUpdate( self, dt ):
        x, y = self.GetPosition()
        gnd = Engine.GetGObject( "ground" )
        if( self.GetRect().CollideRect( gnd.GetRect() ) ):
            ox, oy = gnd.GetPosition()
            ow, oh = gnd.GetSize()
            y = oy + oh
            self.SetPosition( (x,y) )
            if( self.vy > -60 and self.vy < 60 ):
                self.vy = 0
            else: self.vy = -self.vy/3
        else:
            self.vy = self.vy + 4

# -- show time
game = MiJuego()
game.Run()
