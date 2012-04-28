# -*- coding: utf-8 -*-
'''
Created on 28 avr. 2012
'''
import unittest
from mathutils.types import Vertex, Vector, Segment
from mathutils.geometry import inSector, dot_product, orientation, is_segment_intersection

class Test_geometry(unittest.TestCase):
    
    def test_scal_Prod(self):
        print("scal_Prod")
        vect2 = Vector(-1, 2)
        vect3 = Vector(4, -5)
        self.assertEqual(dot_product(vect2, vect3), -14)
        
    def test_orient1(self):
        print("orient1")
        v0 = Vertex(0, 0)
        v1 = Vertex(1, 0)
        v2 = Vertex(1, 1)
        self.assertEqual(orientation(v0, v1, v2), 1)
    
    
    def test_intersect1(self):
        print("intersect1")
        s1 = Segment(Vertex(0, 0), Vertex(2, 0))
        s2 = Segment(Vertex(2, 1), Vertex(0, -1))
        self.assertEqual(is_segment_intersection(s1, s2), True)
        
    def test_intersect2(self):
        print("intersect2")
        s1 = Segment(Vertex(0, 0), Vertex(2, 0))
        s2 = Segment(Vertex(1, 1), Vertex(2, 1))
        self.assertEqual(is_segment_intersection(s1, s2), False)
        
    def test_intersect3(self):
        print("intersect3")
        s1 = Segment(Vertex(2, 0), Vertex(1, 1))
        s2 = Segment(Vertex(1, 2), Vertex(1, 1.01))
        self.assertEqual(is_segment_intersection(s1, s2), False)
    
    def test_inSector1(self):
        print("inSector1")
        v0 = Vector(1, 0)
        v1 = Vector(0, 1)
        v2 = Vector(1, 1)
        self.assertEqual(inSector(v0, v1, v2), True)
        
    def test_inSector2(self):
        print("inSector2")
        v0 = Vector(1, 0)
        v1 = Vector(0, 1)
        v2 = Vector(-1, 1)
        self.assertEqual(inSector(v0, v1, v2), False)
        
    def test_inSector3(self):
        print("inSector3")
        v0 = Vector(-1, -1)
        v1 = Vector(0, 1)
        v2 = Vector(1, -1)
        self.assertEqual(inSector(v0, v1, v2), True)
        
if __name__ == '__main__':
    unittest.main()