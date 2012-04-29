# -*- coding: iso-8859-1 -*- 

from ia import IA
from mathutils.types import Vertex
from scene import Scene, Box
from robot.small_robot import Small_robot
from robot.simu_robot import Simu_robot
from tkinter import Frame, Canvas
import threading
from time import sleep

class RobotD:
    def __init__(self, canvas, robot):
        self.canvas = canvas
        self.robot  = robot  
        self.robotd = canvas.create_rectangle(0.01*robot.pos.x-10, 
                                              0.01*robot.pos.y-10, 
                                              0.01*robot.pos.x+10, 
                                              0.01*robot.pos.y+10,
                                              width =1, fill="gray")
        
    def draw(self):
        print(0.01*self.robot.pos.x-5, 0.01*self.robot.pos.y-5, 
                           0.01*self.robot.pos.x+5, 0.01*self.robot.pos.y+5)
        self.canvas.coords(self.robotd, 0.01*self.robot.pos.x-10, 0.01*self.robot.pos.y-10, 
                           0.01*self.robot.pos.x+10, 0.01*self.robot.pos.y+10)

      
class SceneD:
    def __init__(self, canvas, scene):
        self.canvas    = canvas
        self.scene     = scene
        self.plateau   = BoxD(canvas, self.scene.plateau, "cyan")
        self.objects   = [BoxD(canvas, ob) for ob in scene.obstacles.values()]
        
        left_room      = Box(Vertex(0,15000), Vertex(5000, 20000))
        left_room.adjust(scene.dx, scene.dy, scene.s)
        self.objects.append(BoxD(canvas, left_room, "purple"))
        
        right_room      = Box(Vertex(25000,15000), Vertex(30000, 20000))
        right_room.adjust(scene.dx, scene.dy, scene.s)
        self.objects.append(BoxD(canvas, right_room, "red"))
        
    def draw(self):
        self.plateau.draw()
        for obj in self.objects:
            obj.draw()
      
class BoxD:
    def __init__(self, canvas, box, color="blue"):
        dx = 150*2+1
        dy = -1-100*2 + int(canvas.cget("height"))
        s  = 0.02
        self.canvas = canvas
        self.box    = box.copy()
        self.box.corner1.y *= -1
        self.box.corner2.y *= -1
        self.box.adjust(dx, dy, s)
        
        self.rect   = canvas.create_rectangle(self.box.corner1.x, 
                                              self.box.corner1.y, 
                                              self.box.corner2.x, 
                                              self.box.corner2.y,
                                              width =1, fill=color)
        

    def draw(self):
        
        self.canvas.coords(self.rect,self.box.corner1.x, 
                                     self.box.corner1.y, 
                                     self.box.corner2.x, 
                                     self.box.corner2.y)
    def delete(self):
        self.canvas.delete(self.line)


class LineD:
    def __init__(self, v1, v2, canvas):
        self.v1 = v1
        self.v2 = v2
        self.line = canvas.create_line(self.v1.y, self.v1.x, self.v2.y, self.v2.x, width =1)
    def draw(self,  canvas):
        canvas.coords(self.line, self.v1.y, self.v1.x, self.v2.y, self.v2.x)
    def delete(self,  canvas):
        canvas.delete(self.line)
        

class Controller:
    '''MVC pattern + Observer pattern'''
    def __init__(self):            
        self.view = None
        
    def update(self, event):
        print("simu", event)
        if self.view != None:
            sleep(0.1)
            self.view.redraw_robot()
    
class View(Frame):
    '''MVC pattern'''
    def __init__(self, robot, scene, controller):
        Frame.__init__(self)
        
        self.controller = controller

        self.canvas = Canvas(self, width=602, height=402, bg='white')
        self.scene = SceneD(self.canvas, scene)
        self.robot = RobotD(self.canvas, robot)
        
    def init(self):
        
        self.canvas.pack(padx =5, pady =3)
        self.canvas.bind("<Button-1>", self.mouseDown)
        self.canvas.bind("<Button1-Motion>", self.mouseMove)
        self.canvas.bind("<Button1-ButtonRelease>", self.mouseUp)
        self.pack()
        
        self.scene.draw()
        self.robot.draw()
        
    def redraw_robot(self):
        self.robot.draw()
   
            
    def mouseDown(self, event):
        pass
        
    def mouseMove(self, event):
        pass
            
        
    def mouseUp(self, event):
        pass
    
class Simu:
    def __init__(self, robot, scene):
        self.controller = Controller()
        Simu_robot.add_observer(self.controller)
        self.view = View(robot, scene, self.controller)
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
