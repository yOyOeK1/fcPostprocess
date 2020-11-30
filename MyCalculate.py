
import math
#from GPoint import *

class MyCalculate:
    
    
    def distance(self, p0, p1):
        if p0.x and p0.y and p1.x and p1.y:
            return math.sqrt((p1.x - p0.x)**2 + (p1.y - p0.y)**2)
        return None
    
    
    def angle( self, p0, p1, p2 = None):
        if p2==None:
            deltax = p1.x- p0.x
            deltay = p1.y- p0.y
            a = math.atan2(deltay,deltax)
            return math.degrees(a)
            
        else:
            a0 = self.angle(p1, p2)
            a1 = self.angle( p1, p0)
            if a0>=a1:
                a =  a0 - a1
            else:
                a = a1 - a0 
            return a
    
    def newPoint(self, pStart, pEnd, dist, floatRate = None):
        if pStart.x and pStart.y and pEnd.x and pEnd.y:
            distSE = self.distance(pStart, pEnd)
            if distSE > dist or (distSE*-1)>dist:
                
                if dist<0:
                    d = dist*-1
                else:
                    d = distSE-dist
                
                ang = self.angle(pStart, pEnd)
                xn = pStart.x + d * math.cos( math.radians(ang) )
                yn = pStart.y + d * math.sin( math.radians(ang))
                
                #et = (pEnd.e -pStart.e)/distSE
                
                
                #pc = GPoint()
                #pc.setXYZ(xn, yn, pEnd.z, pEnd.e-(dist*et), pEnd.f)
                import copy
                pc = copy.copy(pEnd)
                pc.x = xn
                pc.y = yn
                #pc.z = pEnd.z
                #pc.e = pEnd.e-(dist*et)
                #pc.f = pEnd.f
                
                return pc
                
            else:
                return None
            
        return None
    
    
    
    def scale(self, a, b):
        return a/b
    
    def scaleForOffset(self, xo, yo, scale, step, tpx, tpy ):
        w = tpx
        h = tpy
        
        xoff = ((xo-w)/scale)
        yoff = ((yo-h)/scale)
        
        scale*=step
        
        xo = (xoff * scale)+w
        yo = (yoff * scale)+h
    
        return [scale, xo, yo]
    
    def mRound(self, val, accu):
        return round(val,accu)
        