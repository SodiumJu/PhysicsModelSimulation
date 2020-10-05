#Yan-Ru Ju
from visual import*
import copy
#The constant
ee,em,eh,eht=False,False,False,False
ecount,mcount,hcount=0,0,0
et=0 #Earth t
mt=0 #Mars t
ht=0 #Halley t
dt=86400.0
G=6.673E-11
halley_end_point=0
halley_int_point=0
#The position of sun is at (0,0,0)

#The radius of Celestial bodies
radius_dic={"Sun":695700,"Earth":6371,"Halley":6.5,"Mars":3397}
#The mass of Celestial bodies
mass_dic={"Sun":1.989E30,"Earth":5.972E24,"Mars":6.39E23, "Halley":2.2E14}
#The data of perihelion
perihelion_dic={"Earth_d":1.495E11,"Earth_v":2.9783E4,"Mars_d":2.279E11,"Mars_v":2.4077E4,"Halley_d":8.82E10,"Halley_v":54400}
#material of Celestial bodies
material_dic={"Sun":materials.shiny,"Earth":materials.earth,"Mars":materials.wood}
#The function of G_force
def G_force(m,position_vector):
    F=-G*mass_dic['Sun']*m/(mag(position_vector)**2)*norm(position_vector)
    return F

#class of Celestial bodies
class as_obj(sphere):
    
    
    def potential_energy(self):
        
        PE=-G*mass_dic['Sun']*self.m/(self.pos).mag
        return PE
    
    def kinetic_energy(self):
        
        KE=0.5*self.m*(self.v.mag**2)
        return KE
    def Total_energy(self):
        TE=self.potential_energy()+self.kinetic_energy()
        return TE
#printer    
def eprinter(Unknow,t):
    print 'T^2/R^3(Earth):',t,((t*dt)**2/perihelion_dic['Earth_d']**3)
def mprinter(Unknow,t):
    print 'T^2/R^3(Mars):',t,((t*dt)**2/perihelion_dic['Mars_d']**3)
def hprinter(Unknow,t):
    print 'Halley\'s period:',t/365,'years'

#Discriminator for earth
def Discriminator_for_earth(Unknow):
    global ee,et,ecount
    if ee==False:
        if (Unknow.v.x>=0):
            ee=True
    elif ee==True:
        if (Unknow.v.x<=0):
            ecount=ecount+1
            if ecount==1:
                eprinter(Unknow,et)
            et=0
            ee=False
#Discriminator for mars
def Discriminator_for_mars(Unknow):
    global em,mt,mcount
    if em==False:
        if (Unknow.v.x>=0):
            em=True
    elif em==True:
        if (Unknow.v.x<=0):
            mcount=mcount+1
            if mcount==1:
                mprinter(Unknow,mt)
            mt=0
            em=False
#Discriminator for halley
def Discriminator_for_halley(Unknow):
    global eh,ht,hcount,halley_end_point
    if eh==False:
        if (Unknow.v.x<=0):
            if hcount>0:
                print "-------------------perihelion----------------------"
                hprinter(Unknow,ht)
                print 'Areas of perihelion sweep for an earth day:',cross(halley.pos,halley.v).mag
                print 'Kinetic energy:',Unknow.kinetic_energy(),' Potential energy:',Unknow.kinetic_energy()
                print 'Total energy:',Unknow.Total_energy()
                print "-------------------perihelion----------------------"
            ht=0
            eh=True
    elif eh==True:
        if (Unknow.v.x>=0):
            hcount=hcount+1
        
            print "-------------------aphelion------------------------"
            print 'Areas of aphelion swept for an earth day:',cross(halley.pos,halley.v).mag
            print 'Kinetic energy:',Unknow.kinetic_energy(),' Potential energy:',Unknow.kinetic_energy()
            print 'Total energy:',Unknow.Total_energy()
            print "-------------------aphelion------------------------"
            halley_end_point=halley.pos.x
            eh=False
def Discriminator_for_halley_half(Unknow):
    global eht,ht,halley_end_point
    half_way=(halley_end_point+perihelion_dic['Halley_d'])/2
    if (hcount>0):
        if eht==False:
            if (halley.x>half_way):
                print "-------------------half-way point------------------"
                print 'Areas of half-way point swept for an earth day:',cross(halley.pos,halley.v).mag
                print 'Kinetic energy:',Unknow.kinetic_energy(),' Potential energy:',Unknow.kinetic_energy()
                print 'Total energy:',Unknow.Total_energy()
                print "-------------------half-way point------------------"

                eht=True
        elif eht==True:
            if (halley.x<half_way):
                print "-------------------half-way point------------------"
                print 'Areas of half-way point swept for an earth day:',cross(halley.pos,halley.v).mag
                print 'Kinetic energy:',Unknow.kinetic_energy(),' Potential energy:',Unknow.kinetic_energy()
                print 'Total energy:',Unknow.Total_energy()
                print "-------------------half-way point------------------"
                eht=False



#creat Celestial bodies
Celestial_bodies=[]
#Setting of Earth
def Earth():
    global earth
    earth=as_obj(make_trail=True,retain=500,trail_type="curve")
    earth.trail_object.color=color.blue #(0,0.255,0.255)
    earth.radius=radius_dic['Earth']*500000 #200 times magnification
    earth.material=material_dic['Earth']
    #earth.color=color.red
    earth.m=mass_dic['Earth']
    earth.pos=vector(perihelion_dic['Earth_d'],0,0)
    earth.v=vector(0,0,-perihelion_dic['Earth_v'])
        

#Setting of Sun
def Sun():
    global sun
    sun=as_obj()
    sun.radius=radius_dic['Sun']*10000 #10 times magnification
    sun.material=material_dic['Sun']
    sun.color=color.yellow
    sun.m=mass_dic['Sun']
    sun.pos=vector(0,0,0)
    sun.v=(0,0,0)

#Setting of Mars
def Mars():
    global mars
    mars=as_obj(make_trail=True,retain=500,trail_type="curve")
    mars.trail_object.color=color.red
    mars.radius=radius_dic['Mars']*500000 #200 times magnification
    mars.color=color.red
    mars.m=mass_dic['Mars']
    mars.pos=vector(perihelion_dic['Mars_d'],0,0)
    mars.v=vector(0,0,-perihelion_dic['Mars_v'])
#Setting of Halley
def Halley():
    global halley
    halley=as_obj(make_trail=True,retain=500)
    halley.trail_object.color=color.yellow
    halley.radius=radius_dic['Halley']*500000 #200 times magnification
    halley.color=(0.218,0.165,0.32)
    halley.m=mass_dic['Halley']
    halley.pos=vector(perihelion_dic['Halley_d'],0,0)
    halley.v=vector(0,0,-perihelion_dic['Halley_v'])

       
#main
scene=display(width=1000,height=1000,center=(0,0,0),background=(0.025,0.025,0.112),forward=vector(0,-1,0))
Earth()
Mars()
Sun()
Halley()
#creat Celestial bodies list


EPE=earth.potential_energy()
EKE=earth.kinetic_energy()
print 'The half-way point values of Halley will show up after half of first period. Please wait for a moment. Thanks a lot!!!'
print 'Potential energy of Earth:',EPE,' Kinetic energy of Earth:',EKE,'at perihelion~~'


while True:
    rate(1000)
    
    #Earth
    earth.v += G_force(earth.m,earth.pos)/earth.m*dt
    earth.pos += earth.v*dt
    #Mars
    mars.v += G_force(mars.m,mars.pos)/mars.m*dt
    mars.pos += mars.v*dt
    #Halley
    halley.v += G_force(halley.m,halley.pos)/halley.m*dt
    halley.pos += halley.v*dt

    #Period recorder
    et=et+1
    mt=mt+1
    ht=ht+1
    Discriminator_for_earth(earth)
    Discriminator_for_mars(mars)
    Discriminator_for_halley(halley)
    Discriminator_for_halley_half(halley)
    

    
    
    
    
    
    
    
    

