import math

class Vector():
    
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + " , " + str(self.y) + " )"
    def __add__(self,other):
        return Vector(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return Vector(self.x-other.x,self.y-other.y)
    def __mul__(self,other):
        return Vector(self.x*other,self.y*other)
    def __truediv__(self,other):
        return Vector(self.x/other,self.y/other)
    

    def normalize(self):
        self = self/length(self)

    def rotate(self,angle):
        """
        Rotates a Vecotr

        Inputs:
        self (Vector)
        angle (float)

        Return:
            Vector

        """
        sx = self.x
        sy = self.y

        self.x = math.cos(angle) * sx + math.sin(angle)*sy
        self.y = -math.sin(angle) * sx + math.cos(angle)*sy
        return Vector(self.x,self.y)


def length(v):
    """
    Returns the length of a Vector
    
    Inputs:
        v (Vector)
    
    Returns:
        float
    """
    return math.sqrt(v.x**2+v.y**2)

def normalize(v):
    return Vector(v.x/length(v),v.y/length(v))

def dot(u,v):
    return u.x*v.x+u.y*v.y

def smallest_angle(u,v):
    return math.acos(dot(u,v)/(length(u)*length(v)))


def tupel_to_vector(tupel):
    return Vector(tupel[0],tupel[1])
    
def vector_to_tupel(Vector):
    return [Vector.x,Vector.y]