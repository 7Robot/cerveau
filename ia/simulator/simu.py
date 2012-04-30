# -*- coding: iso-8859-1 -*- 

from ia import IA
from mathutils.types import Vertex
from scene import Scene, Box
from robot.small_robot import Small_robot
from robot.simu_robot import Simu_robot, Spy
from tkinter import Frame, Canvas
from simulator.real_robot import Real_robot, Regulator
import threading


class Board:
    '''Là où on dessine'''
    def __init__(self, canvas):
        self.canvas   = canvas
        self.drawings = {}
        
    def add_drawing(self, drawing, item):
        self.drawings[item] = drawing
        
#    def adjust_vertex(self, vertex):
#        '''Retourne le vertex dans les coordonnées du canvas'''
#        vert = vertex*0.02
#        vert.y *= -1
#        vert.translate(150*2+1, -1-100*2 + int(self.canvas.cget("height")))
#        return vert
    
    def cx(self, x):
        '''Retourne une abscisse convertie dans le repère du canvas'''
        return x*0.02 + 150*2 + 1
    
    def cy(self, y):
        '''Retourne une ordonnée convertie dans le repère du canvas'''
        return -y*0.02 - 1 - 100*2 + int(self.canvas.cget("height"))
    
    def icx(self, x):
        '''Retourne une abscisse convertie dans le repère de l'ia'''
        return (x - 150*2 - 1)*50 
    
    def icy(self, y):
        '''Retourne une ordonnée convertie dans le repère de l'ia'''
        return -50 * (y + 1 + 100*2 - int(self.canvas.cget("height")))
        
    def create_rectangle(self, x1, y1, x2, y2, **kargs):
        return self.canvas.create_rectangle(self.cx(x1), self.cy(y1),
                                     self.cx(x2), self.cy(y2), kargs)
        
    def coords(self, item, *args):
        nargs = []
        for i in range(len(args)):
            if i%2 == 0:
                nargs.append(self.cx(args[i]))
            else:
                nargs.append(self.cy(args[i]))
        self.canvas.coords(item, *tuple(nargs))

        
    def find_graspable_drawing(self, x, y):
        found = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        for item in found:
            if item in self.drawings and self.drawings[item].graspable:
                return self.drawings[item]
        return None

class Drawing:
    def __init__(self, board, graspable=False):
        self.board     = board
        self.graspable = graspable
        
    def move(self):
        pass
        
    def select(self):
        pass
    
    def unselect(self):
        pass
    
    

class RobotD(Drawing):
    def __init__(self, board, robot, color="gray"):
        super(self.__class__, self).__init__(board, True)
        self.robot  = robot  
        self.robotd = self.board.create_rectangle(robot.pos.x-1000, 
                                               robot.pos.y-1000, 
                                               robot.pos.x+1000, 
                                               robot.pos.y+1000,
                                              width =1, fill=color)
        self.board.add_drawing(self, self.robotd)
        
    def draw(self):
        self.board.coords(self.robotd, self.robot.pos.x-1000, self.robot.pos.y-1000, 
                           self.robot.pos.x+1000, self.robot.pos.y+1000)
        
    def move(self, dx, dy):
        self.board.canvas.move(self.robotd, dx, dy)
        self.robot.pos.translate(self.board.icx(dx), self.board.icy(dy))
        
    def select(self):
        self.board.canvas.itemconfig(self.robotd, width =3)
        self.board.canvas.lift(self.robotd)
        
    def unselect(self):
        self.board.canvas.itemconfig(self.robotd, width =1)

      
class SceneD(Drawing):
    def __init__(self, board, scene):
        super(self.__class__, self).__init__(board)
        self.scene     = scene
        self.plateau   = BoxD(board, self.scene.plateau, "cyan")
        self.objects   = [BoxD(board, ob) for ob in scene.obstacles.values()]
        
        left_room      = Box(Vertex(0,15000), Vertex(5000, 20000))
        left_room.adjust(scene.dx, scene.dy, scene.s)
        self.objects.append(BoxD(board, left_room, "purple"))
        
        right_room      = Box(Vertex(25000,15000), Vertex(30000, 20000))
        right_room.adjust(scene.dx, scene.dy, scene.s)
        self.objects.append(BoxD(board, right_room, "red"))
        
    def draw(self):
        self.plateau.draw()
        for obj in self.objects:
            obj.draw()
      
class BoxD(Drawing):
    def __init__(self, board, box, color="blue"):
        super(self.__class__, self).__init__(board)
        self.box  = box
        self.rect = self.board.create_rectangle(self.box.corner1.x, self.box.corner1.y, 
                                              self.box.corner2.x, self.box.corner2.y,
                                              width =1, fill=color)
        self.board.add_drawing(self, self.rect)
        

    def draw(self):
        self.board.coords(self.rect, self.box.corner1.x, self.box.corner1.y, self.box.corner2.x, self.box.corner2.y)
        

class Controller:
    '''MVC pattern + Observer pattern'''
    def __init__(self, real_robot):
        self.real_robot = Regulator(real_robot)            
        self.view = None


        
    def update(self, type, event, *args):
        print("simu", event)
        if self.view != None:
            if type == "get":
                if event.__name__ == "asserv":
                    self.real_robot.asserv_speed(args[0])
            self.view.redraw_robot()
    
class View(Frame):
    '''MVC pattern'''
    def __init__(self, real_robot, robot, scene, controller, phys_sim):
        Frame.__init__(self)
        
        
        self.controller = controller
        self.phys_sim   = phys_sim

        self.board = Board(Canvas(self, width=602, height=402, bg='white'))
        self.scene = SceneD(self.board, scene)
        self.real_robot = RobotD(self.board, real_robot, "black")
        self.robot = RobotD(self.board, robot)
        self.item = None
        
    def init(self):
        
        self.board.canvas.pack(padx =5, pady =3)
        self.board.canvas.bind("<Button-1>", self.mouseDown)
        self.board.canvas.bind("<Button1-Motion>", self.mouseMove)
        self.board.canvas.bind("<Button1-ButtonRelease>", self.mouseUp)
        self.pack()
        
        self.scene.draw()
        self.robot.draw()
        if self.phys_sim:
            self.redraw_real_robot()
        
        
    def redraw_robot(self):
        self.robot.draw()
        
    def redraw_real_robot(self):
        if self.phys_sim:
            self.controller.real_robot.run()
            self.real_robot.draw()
            self.after(50, self.redraw_real_robot)

   
            
    def mouseDown(self, event):
        self.item= self.board.find_graspable_drawing(event.x, event.y)
        if self.item != None:
            self.item.select()
            self.mouse = event

        
    def mouseMove(self, event):
        if self.item != None:
            self.item.move(event.x-self.mouse.x, event.y-self.mouse.y)
        self.mouse = event   
        
    def mouseUp(self, event):
        if self.item != None:
            self.item.unselect()
    
class Simu:
    def __init__(self, robot, scene, phys_sim=False):
        self.real_robot = Real_robot(robot, 200, 60)
        self.controller = Controller(self.real_robot)
        Spy.add_observer(self.controller)
        self.view = View(self.real_robot, robot, scene, self.controller, phys_sim)
        self.controller.view = self.view
        self.view.init()
        
    def main(self):
        self.view.mainloop()
        
if __name__ == '__main__':
    robot = Simu_robot(Small_robot())
    ia = IA(Small_robot(), "r2d2")
    ia_thread = threading.Thread(None, ia.main, None, (), {})
    ia_thread.start()
    simu = Simu(robot, Scene())
    simu.main()
