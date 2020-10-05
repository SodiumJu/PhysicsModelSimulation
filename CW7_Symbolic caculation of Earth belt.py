from visual import*
from sympy import*
x = symbols('x')
#caculating the belt of Earth

volume=2*integrate((6378E3*sin(x))**2*pi-(6357E3*cos(x))**2*pi,(x,0,pi/2))
print volume

#infinite integral : 81357768000000.0*pi*(x/2 - sin(x)*cos(x)/2) - 80822898000000.0*pi*(x/2 + sin(x)*cos(x)/2)
#the answer is 133717500000.0*pi**2
