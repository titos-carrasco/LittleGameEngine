from lge.Engine import Engine
from lge.Canvas import Canvas


class Game():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (640,640), "Pong" )
        Engine.SetOnUpdate( self.MainUpdate )

        field = Canvas( (5,35), (630,524), "field" )
        field.Fill( (0,0,100) )
        Engine.AddGObject( field, 0 )

        # cargamos los recursos que usaremos
        Engine.LoadTTFFont( "monospace", 16, "../fonts/FreeMono.ttf" )

        # agregamos la barra de info
        infobar = Canvas( (0,620), (640,20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # los bordes
        wall = Canvas( (0,560), (640,4)  )
        wall.Fill( (255,255,255) )
        wall.SetTag( "wall-horizontal" )
        wall.SetColliders()
        Engine.AddGObject( wall, 1 )

        wall = Canvas( (0,30), (640,4) )
        wall.Fill( (255,255,255) )
        wall.SetTag( "wall-horizontal" )
        wall.SetColliders()
        Engine.AddGObject( wall, 1 )

        wall = Canvas( (20,34), (4,526) )
        wall.Fill( (255,255,255) )
        wall.SetTag( "wall-vertical" )
        wall.SetColliders()
        Engine.AddGObject( wall, 1 )

        wall = Canvas( (616,34), (4,526) )
        wall.Fill( (255,255,255) )
        wall.SetTag( "wall-vertical" )
        wall.SetColliders()
        Engine.AddGObject( wall, 1 )

        # los actores
        ball = Ball( (320,400), (8,8), "ball" )
        ball.Fill( (255,255,255) )
        ball.SetColliders()
        Engine.AddGObject( ball, 1 )

        paddle = Canvas( (90,270), (8,60), "user-paddle" )
        paddle.Fill( (255,255,255) )
        paddle.SetTag( "paddle")
        paddle.SetColliders()
        Engine.AddGObject( paddle, 1 )

        paddle = Canvas( (540,270), (8,60), "system-paddle" )
        paddle.Fill( (255,255,255) )
        paddle.SetTag( "paddle")
        paddle.SetColliders()
        Engine.AddGObject( paddle, 1 )

        self.paddle_speed = 240
        self.key_pressed = -1

    def MainUpdate( self, dt ):
        # abortamos con la tecla Escape
        if( Engine.KeyUp( Engine.CONSTANTS.K_ESCAPE ) ):
            Engine.Quit()

        # mostramos info
        fps = Engine.GetFPS()
        fps = "FPS: %07.2f" % fps

        ngobjs = len( Engine.GetGObject( "*") )
        ngobjs = "gObjs: %03d" % ngobjs

        mx, my = Engine.GetMousePosition()
        mb1, mb2, mb3 = Engine.GetMouseButtons()
        minfo = "Mouse: (%3d,%3d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

        infobar = Engine.GetGObject( "infobar" )
        infobar.Fill( (255,255,255,20) )
        infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (50,0), "monospace", (255,255,255) )

        # el campo de juego
        field = Engine.GetGObject( "field" ).GetRectangle()

        # user paddle
        user_paddle = Engine.GetGObject( "user-paddle" )
        speed = self.paddle_speed*dt
        x, y = user_paddle.GetPosition()

        if( self.key_pressed == -1 ):
            if( Engine.KeyDown( Engine.CONSTANTS.K_DOWN ) ): self.key_pressed = Engine.CONSTANTS.K_DOWN
            elif( Engine.KeyDown( Engine.CONSTANTS.K_UP ) ): self.key_pressed = Engine.CONSTANTS.K_UP
        else:
            if( Engine.KeyUp( self.key_pressed ) ):
                self.key_pressed = -1

        if( self.key_pressed == Engine.CONSTANTS.K_UP ):
            user_paddle.SetPosition( x, y+speed, field )
        elif( self.key_pressed == Engine.CONSTANTS.K_DOWN ):
            user_paddle.SetPosition( x, y-speed , field )

        # system paddle
        system_paddle = Engine.GetGObject( "system-paddle" )
        pw, ph = system_paddle.GetSize()
        px, py = system_paddle.GetPosition()
        bx, by = Engine.GetGObject( "ball").GetPosition()

        if( py + ph/2 < by ): py = py + speed
        elif( py + ph/2 > by ): py = py - speed
        system_paddle.SetPosition( px, py, field )


    # main loop
    def Run( self ):
        Engine.Run( 60 )


class Ball( Canvas ):
    def __init__( self, position, size, name ):
        super().__init__( position, size, name )
        self.speedX = 180
        self.speedY = -180

    def OnUpdate( self, dt ):
        dx = self.speedX*dt
        dy = self.speedY*dt

        x, y = self.GetPosition()
        self.SetPosition( x+dx, y+dy )

    def OnCollision( self, dt, collisions ):
        x, y = self.GetPosition()
        dx = self.speedX*dt
        dy = self.speedY*dt

        for gobj, r  in collisions:
            if( gobj.GetTag() == "wall-horizontal" ):
                self.speedY = -self.speedY
                dy = -dy
            if( gobj.GetTag() == "paddle" ):
                self.speedX = -self.speedX
                dx = -dx
            if( gobj.GetTag() == "wall-vertical" ):
                x, y = 320, 400
        self.SetPosition( x+dx, y+dy )



# ----
game=Game()
game.Run()
