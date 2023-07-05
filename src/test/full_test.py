import Tester
import numpy as np

# clase de prueba
class Test(Tester):

    def __init__(self, x):
        self.x = x + 1

    # funcion 1
    def prueba1(self, y):
        if self.x < y and y != 0 or self.x != 0:
            while y != 0:
                y = y - 1
        else:
            y = "Hola"
        return y + 2

    def prueba2(self, z):
        z = z + 1
        if self.x == z and z > 0:
            self.x = z * 2
        return z
        

def prueba3(z):
    # prueba 3
    print("Prueba 3")
    if z == 1:
        print("If")
        return z + 1
    elif z == 2:
        print("Elif 1")
        return z + 2
    elif z == 3:
        print("Elif 2")
        return z + 3
    else:
        print("Else")
        return "Else"


t1 = Test(10)
a = t1.prueba1(12)
b = t1.prueba2(1)
c = prueba3(2)
print(a)