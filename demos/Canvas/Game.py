import random
import uuid
import math

from lge.Engine import Engine
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle


class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (800,600), "Demo de Canvas", (255,255,255) )

        # cargamos los recursos que usaremos
        Engine.LoadTTFFont( "monospace", 16, "../fonts/FreeMono.ttf" )

        # agregamos la barra de info
        infobar = Canvas( (0,550), (800,50), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # un canvas para plotear y usar de piso
        ground = Canvas( (0,0), (800,100), "ground" )
        ground.physics = Physics( 0, 0, 0, 0, 0 )
        ground.Fill( (200,200,200) )
        ground.SetColliders()
        Engine.AddGObject( ground, 1 )

        # configuramos la camara
        camera = Engine.GetCamera()
        camera.SetBounds( Rectangle( (0,0), (800,600) ) )

        # el control central del juego
        Engine.SetOnUpdate( self.MainControl )

        Engine.ShowColliders( (255,0,0) )

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
        infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (140,30), "monospace", (0,0,0) )
        infobar.DrawText( "Presione B(ox), C(ircle), D(elete)", (240,5), "monospace", (0,0,0) )

        #
        ground = Engine.GetGObject( "ground" )

        # agregamos nuevos objetos
        mx, my = Engine.GetMousePos()
        mb1, mb2, mb3 = Engine.GetMousePressed()

        if( Engine.IsKeyUp( Engine.CONSTANTS.K_p ) ):
            x, y = int(random.random()*800), int(random.random()*100)
            for i in range( 50 ):
                dx, dy = -10 + int(random.random()*20), -10 - int(random.random()*20)
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

        # ajustamos acorde a nuestra pseudo-fisica
        for gobj in Engine.GetGObject( "*" ):
            if( hasattr( gobj, "physics") ):
                Physics.Update( dt, gobj )


    def Run( self ):
        Engine.Run( 60 )

class Circle( Canvas ):
    def __init__( self ):
        r = round( 5 + random.random()*25 )
        x, y = random.random()*(800-r*2), 500
        super().__init__( (x,y), (r*2,r*2), "gobj-" + uuid.uuid4().hex )
        self.DrawCircle( (r,r), r, (0,255,0,128), False )

        d = r/math.sqrt(2)
        self.SetColliders()

        sx = -1 if round( random.random() ) == 0 else 1
        self.physics = Physics( sx*60, -120, 240, 0.4, 0.4 )

    def OnUpdate( self, dt ):
        x, y = self.GetPosition()
        w, h = self.GetSize()
        if( x + w < 0 or x > 800 or y + h < 0 or y > 600 ):
            Engine.DelGObject( self.name )


class Box( Canvas ):
    def __init__( self ):
        w, h = round(10 + random.random()*50), round(10 + random.random()*50)
        x, y = random.random()*(800-w), 500
        super().__init__( (x,y), (w,h), "gobj-" + uuid.uuid4().hex )
        self.DrawRectangle( (0,0), (w,h), (134,32,32,128), False )
        self.SetColliders()

        sx = -1 if round( random.random() ) == 0 else 1
        self.physics = Physics( sx*60, -240, 240, 0.4, 0.4 )

    def OnUpdate( self, dt ):
        x, y = self.GetPosition()
        w, h = self.GetSize()
        if( x + w < 0 or x > 800 or y + h < 0 or y > 600 ):
            Engine.DelGObject( self.GetName() )


class Physics():
    def __init__( self, vx, vy, a, e, f ):
        self.vx = vx        # "velocidad" en x - pixeles por segundo
        self.vy = vy        # "velocidad" en y - pixeles por segundo
        self.a = a          # "aceleración" (y) - pixeles por segundo
        self.e = e          # factor de "elasticidad"
        self.f = f          # factor de "friccion"

    def __repr__( self ):
        return "(vx: %30.28f, vy: %30.28f, a: %f, e: %f, f: %f )" % (self.vx, self.vy, self.a, self.e, self.f )

    # *** no esta finalizado aun ***
    def Update( dt, gobj ):
        phys = gobj.physics
        print( gobj.GetName(), phys )

        x, y = gobj.GetPosition()
        w, h = gobj.GetSize()

        x = x + phys.vx*dt
        y = y + phys.vy*dt
        gobj.SetPosition( (x,y) )

        if( phys.vy ):
            phys.vy = phys.vy - phys.a*dt

        collisions = Engine.GetCollisions( gobj.GetName() )
        if( not collisions ): return

        o, r = collisions[0]
        ox, oy = o.GetPosition()
        ow, oh = o.GetSize()

        r = gobj.GetRectangle().GetCollideRectangle( r )

        rx, ry = r.GetOrigin()
        rw, rh = r.GetSize()

        x, y = gobj.GetPosition()

        # golpe horizontal
        if( rh > rw ):
            if( phys.vx < 0 ): gobj.SetPosition( ( ox + ow, y ) )
            elif( phys.vx > 0 ): gobj.SetPosition( ( ox - w, y ) )
            phys.vx = -phys.vx*phys.e

        # golpe vertical
        else:
            if( phys.vy < 0 ): gobj.SetPosition( ( x, oy + oh ) )
            elif( phys.vy > 0 ): gobj.SetPosition( ( x, oy - w ) )
            phys.vy = -phys.vy*phys.e

        if( abs( phys.vy ) < 10 ):
            phys.vy = 0

        if( abs( phys.vx ) < 10 ):
            phys.vx = 0
        else:
            phys.vx = phys.vx*phys.f

# -- show time
game = MiJuego()
game.Run()
