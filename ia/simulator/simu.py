# -*- coding: iso-8859-1 -*- 

from mathutils.types import Vertex
from scene import Scene, Box
from robot import Robot
from tkinter import Frame, Canvas

      
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
        pass
    
class View(Frame):
    '''MVC pattern'''
    def __init__(self, robot, scene, controller):
        Frame.__init__(self)
        self.robot = robot
        self.controller = controller

        self.canvas = Canvas(self, width=602, height=402, bg='white')
        self.scene = SceneD(self.canvas, scene)
        
        self.canvas.pack(padx =5, pady =3)
        self.canvas.bind("<Button-1>", self.mouseDown)
        self.canvas.bind("<Button1-Motion>", self.mouseMove)
        self.canvas.bind("<Button1-ButtonRelease>", self.mouseUp)
        self.pack()
        
        self.scene.draw()
      
   
            
    def mouseDown(self, event):
        pass
        
    def mouseMove(self, event):
        pass
            
        
    def mouseUp(self, event):
        pass
    
class Simu:
    def __init__(self, robot, scene):
        self.controller = Controller()
        self.view = View(robot, scene, self.controller)
        self.controller.view = self.view
        
    def main(self):
        self.view.mainloop()
        
if __name__ == '__main__':
    simu = Simu(Robot(0, 0, 0, 0, 0, 0, 0), Scene())
    simu.main()
