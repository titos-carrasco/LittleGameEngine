import uuid
import random
import time

from lge.Engine import Engine
from lge.Text import Text
from lge.Canvas import Canvas
from lge.Rect import Rect

import pygame
class Game():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (640,640), "Pong" )
        Engine.SetUpdate( self.MainUpdate )

        field = Canvas( (5,35), (630,524), (0,0,100), "field" )
        Engine.AddGObject( field, 0 )

        # cargamos los recursos que usaremos
        Engine.LoadTTFFont( "monospace", 20, "../fonts/FreeMono.ttf" )

        # agregamos la barra de info
        infobar = Text( None, (0,610), "monospace", (255,255,255), None, "infobar" )
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # los bordes
        wall = Canvas( (0,560), (640,4), (255,255,255) )
        wall.SetTag( "wall-horizontal" )
        Engine.AddGObject( wall, 1 )

        wall = Canvas( (0,30), (640,4), (255,255,255) )
        wall.SetTag( "wall-horizontal" )
        Engine.AddGObject( wall, 1 )

        wall = Canvas( (20,34), (4,526), (255,255,255) )
        wall.SetTag( "wall-vertical" )
        Engine.AddGObject( wall, 1 )

        wall = Canvas( (616,34), (4,526), (255,255,255) )
        wall.SetTag( "wall-vertical" )
        Engine.AddGObject( wall, 1 )

        ball = Ball( (320,320), (8,8), (255,255,255), "ball" )
        Engine.AddGObject( ball, 1 )

        paddle = Canvas( (90,270), (8,60), (255,255,255), "user-paddle" )
        paddle.SetTag( "paddle")
        Engine.AddGObject( paddle, 1 )

        paddle = Canvas( (540,270), (8,60), (255,255,255), "system-paddle" )
        paddle.SetTag( "paddle")
        Engine.AddGObject( paddle, 1 )

        #Engine.ShowColliders( (255,0,255) )

    def MainUpdate( self, dt ):
        # abortamos con la tecla Escape
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_ESCAPE ) ):
            Engine.Quit()

        # mostramos info
        fps = Engine.GetFPS()
        fps = "FPS: %07.2f" % fps

        ngobjs = len( Engine.GetGObject( "*") )
        ngobjs = "gObjs: %03d" % ngobjs

        mx, my = Engine.GetMousePos()
        mb1, mb2, mb3 = Engine.GetMousePressed()
        minfo = "Mouse: (%3d,%3d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

        info = Engine.GetGObject( "infobar" )
        info.SetText( fps + " - " + ngobjs + " - " + minfo )

        # el campo de juego
        field = Engine.GetGObject( "field" ).GetRect()

        # user paddle
        user_paddle = Engine.GetGObject( "user-paddle" )
        x, y = user_paddle.GetPosition()
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_UP ) ):
            user_paddle.SetPosition( (x,y+4), field )
        elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_DOWN ) ):
            user_paddle.SetPosition( (x,y-4), field )

        # system paddle
        system_paddle = Engine.GetGObject( "system-paddle" )
        pw, ph = system_paddle.GetSize()
        px, py = system_paddle.GetPosition()
        bx, by = Engine.GetGObject( "ball").GetPosition()

        if( py + ph/2 < by ): py = py + 4
        elif( py + ph/2 > by ): py = py - 4
        system_paddle.SetPosition( (px,py), field )


    # main loop
    def Run( self ):
        Engine.Run( 60 )


class Ball( Canvas ):
    def __init__( self, position, size, color, name ):
        super().__init__( position, size, color, name )
        self.speedX = 4
        self.speedY = 5

    def OnUpdate( self, dt ):
        x, y = self.GetPosition()

        self.SetPosition( (x+self.speedX,y+self.speedY) )
        collisions = Engine.GetCollisions( self.GetName() )

        if( not collisions ):
            return
        if( [ True for t in collisions if t[0].GetTag() in [ "wall-horizontal" ] ] ):
            self.speedY = -self.speedY
        if( [ True for t in collisions if t[0].GetTag() in [ "wall-vertical", "paddle" ] ] ):
            self.speedX = -self.speedX

        self.SetPosition( (x+self.speedX,y+self.speedY) )

# ----
game=Game()
game.Run()
