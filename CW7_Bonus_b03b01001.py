from visual import*
#Just answer few questions
#setting
#3.84400E5
#The mass of Celestial bodies
mass_dic={"Sun":1.989E30,"Earth":5.972E24,"Moon":7.36E22}
distance_dic={"Moon":1 }
g=9.8
l, r = 0.50, 0.002 #for shaft
w=0.001 #for earth belt
theta=66.5*pi/180.0
Omega=(1/86400.0)*2*pi*vector(cos(theta),sin(theta),0)
dt = 1.0 


#The function of G_force
def G_force(m,position_vector):
    F=-G*mass_dic['Sun']*m/(mag(position_vector)**2)*norm(position_vector)
    return F
#For Celestial bodies
class as_obj(sphere):
    
    
    def potential_energy(self):
        PE=-G*mass_dic['Sun']*self.m/(self.pos).mag
        return PE
    
    def kinetic_energy(self):
        KE=0.5*self.m*(self.v.mag**2)
        return KE

#Earth
def Earth():
    global earth
    earth=as_obj()
    earth.radius= 0.125
    earth.material=materials.earth
    earth.m=mass_dic['Earth']
    earth.pos=(l/2,0,0)
def Moon():
    global moon
    moon=as_obj(radius=0.08,color=color.gray(0.5),mass=mass_dic['Moon'],pos=(earth.pos.x+distance_dic['Moon'],earth.pos.y,0))

#the setting of Earth

ER=6371*1E3 #the radius of Earth
ad=5.5 #The average density of the Earth is 5.5 g/cm3

#Use three layers to caculate Inertia

ERCr=17*1E3 #the average thickness of crust radius is 17 km
CrdE=2.80*1E3 #density of the Crust is 2.8 g/cm3(2800kg/m3)

ERM=2883*1E3 #the average thickness of mantle radius is 1883 km
MdE=4.50*1E3 #density of the Mantle is 4.5 g/cm3(4500kg/m3)

ERCo=3471*1E3 #the average thickness of core radius is 3471 km
CodE=10.70*1E3 #density of the Core is 10.70 g/cm3(10700kg/m3)

#Volume of different layers

Volume_to_Crust=4.0/3.0*ER**3*pi #Whole
Volume_to_Mantle=4.0/3.0*(ER-ERCr)**3*pi #To_Middle
Volume_to_Core=4.0/3.0*(ERCo)**3*pi #Just_Inside


#Inertia of different layers
I_of_Crust=(3.0/5.0)*ER**2*(CrdE*Volume_to_Crust)-(3.0/5.0)*(ER-ERCr)**2*(CrdE*Volume_to_Mantle)

I_of_Mantle=(3.0/5.0)*ERM**2*(MdE*Volume_to_Mantle)-(3.0/5.0)*(ERCo)**2*(MdE*Volume_to_Core)

I_of_Core=(3.0/5.0)*ERCo**2*(CodE*Volume_to_Core)

#Inertia of Earth
I_of_Earth=I_of_Crust+I_of_Mantle+I_of_Core
print 'Inertia of Earth : ',I_of_Earth

#Using the caculation from CW7_Symbolic caculation of Earth belt.py
Earth_belt_Volume=133717500000.0*pi**2
Earth_belt_Mass=Earth_belt_Volume*ad
print 'The mass of the belt : ',Earth_belt_Mass
    

#main

scene=display(width=1000,height=1000,background=(0.5,0.5,0))
spintop = frame()
#shaft
shaft = cylinder(frame=spintop, pos=(0,0,0), axis =(l,0,0), radius=r, color=color.red)
#Earth
Earth()
earth.frame=spintop
#belt of earth
earth_belt=cylinder(frame=spintop, pos=(l/2-w,0,0), axis =(w,0,0), radius=0.125, color=color.red,mass=Earth_belt_Mass)
spintop.pos = (0,0,0)
#base
base = cone(pos=(0,-0.2,0), axis=(0,0.2,0), color = color.blue, radius=0.1)
#about moon
#Moon()
#spinmoon=frame()
#spinmoon.pos=(0,0,0)
#moon.frame=spinmoon






while True:
    rate(100000)
    spintop.axis = norm(Omega)
    delta_angle = mag(Omega)*dt
    spintop.rotate(angle=delta_angle, axis=spintop.axis)
    
