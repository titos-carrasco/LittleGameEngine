import random
import math

from lge.Engine import Engine
from lge.Canvas import Canvas


class MiJuego():
    def __init__( self ):
        self.niters = 60*20
        self.nobjs = 0

        # creamos el juego
        Engine.Init( (800,600), "Particles", (255,255,255) )

        # cargamos los recursos que usaremos
        Engine.LoadTTFFont( "monospace", 16, "../fonts/FreeMono.ttf" )

        # agregamos la barra de info
        infobar = Canvas( (0, 580), (800, 20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # un canvas para plotear
        panel = Canvas( (0, 0), (800, 600), "Panel" )
        panel.Fill( (255,255,255) )
        Engine.AddGObject( panel, 1 )

        # las particulas
        self.num_particles = 500
        self.particles = [0]*self.num_particles
        for i in range( self.num_particles ):
            x = 100 + random.random()*600
            y = 300 + random.random()*200
            vx = -60 + random.random()*120
            vy = -60 + random.random()*240
            m = 0.1 + random.random()
            self.particles[i] = Particle( x, y, vx, vy, m )

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

        # las particulas
        for i in range( self.num_particles ):
            particle = self.particles[i]
            particle.OnUpdate( dt )

        panel = Engine.GetGObject( "Panel" )
        panel.Fill( (255,255,255) )
        for i in range( self.num_particles ):
            particle = self.particles[i]
            x = round( particle.x )
            y = round( particle.y )
            r = round( particle.m*10 )
            #panel.DrawPoint( (x,y), (0,0,0) )
            #panel.DrawCircle( (x,y), r, (0,0,0) )
            panel.DrawRectangle( (x,y), (r,r), (0,0,0) )


    def Run( self ):
        import cProfile
        cProfile.run( "Engine.Run( 60 )" )

class Particle():
    def __init__( self, x, y, vx, vy, m ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m

    def ComputeForce( self ):
        #return 0, self.m * -9.81
        return 0, self.m * -60

    def OnUpdate( self, dt ):
        fx, fy  = self.ComputeForce()
        ax, ay  = fx/self.m, fy/self.m
        self.vx = self.vx + ax*dt
        self.vy = self.vy + ay*dt
        self.x  = self.x + self.vx*dt
        self.y  = self.y + self.vy*dt


# -- show time
game = MiJuego()
game.Run()
