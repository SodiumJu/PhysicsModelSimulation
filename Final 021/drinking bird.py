from visual import*
from visual.graph import*
#unit:kg/m/s
#variable
#balls:

#lower ball
lower_ball_r=0.895E-2 #radius of lower ball
lower_ball_ir=0.865E-2 #internal radius of lower ball
#upper ball
upper_ball_r=0.735E-2 #radius of upper ball
upper_ball_ir=0.705E-2 #internal radius of upper ball

#tube:
tube_len=6.68E-2 #length of tube
tube_r=0.285E-2 #radius of tube
tube_ir=0.2E-2 #internal radius of tube
tube_m=0.865E-3 #mass of tube

#others:
glass_d=2.10E3 #density of glass
h1=0.2E-2 #height from ball to tube
dt=0.01E-2 #delta t
J=vector(0,0,0) #torque
L=vector(0,0,0) #angular momentum
I=0 #inertia
g=9.8 #gravity constant
phi=vector(0,0,0) #initial angle
omega=vector(0,0,0) #initial angular velocity
b=0.0001 #damping factor
t=0 #time
sponge_m=0.0013 #mass of sponge


#room temperature
T_room=295.44
#temperature of head
T_h=0
#pressure
P_h=0 #Pressure of head
P_b=0 #Pressure of body
delta_P=0 #delta of pressure between head and body

#liquid
liquid_d=1.336E3
liquid_V=2.711E-6

#beak
beak_h=0.1E-2
beak_l=0.4E-2
beak_w=0.2E-2
beak_m=1.0E-3

#scene
scene = display(width=800, height=800,background=(1,1,1))
scene_T_t = gdisplay(y=40,width=800,height=300,xtitle='time',ytitle='Temperature of head',background=(0,0,0),ymax=296.0,ymin=295.0)
scene_P_t = gdisplay(y=40,width=800,height=600,xtitle='time',ytitle='Pressure of head',background=(0,0,0),ymax=5.3E4,ymin=5.2E4)
scene_phi = gdisplay(y=40,width=800,height=600,xtitle='time',ytitle='phi',background=(0,0,0))
#graph
T_t=gcurve(color=color.red,gdisplay=scene_T_t)
P_t=gcurve(color=color.yellow,gdisplay=scene_P_t)
phi_t=gcurve(color=color.white,gdisplay=scene_phi)
#class

class bird_ball:
    def __init__(self,frame,pos,radius,iradius,liq_v,liq_d):
        self.ball=sphere(frame=frame,pos=pos,radius=radius,color=color.cyan,opacity=0.3)
        self.iradius=iradius
        self.ball.m=self.glass_ball_mass(radius,iradius)
        self.m_liq=liq_v*liq_d
        self.m_all=self.ball.m+self.m_liq
        self.I=self.inertia()
        
    def glass_ball_mass(self,radius,iradius):
        ball_m_temp=4.0/3.0*pi*((radius)**3-(iradius)**3)*glass_d
        return ball_m_temp
    def inertia(self):
        ball_i_mass=4.0/3.0*pi*(self.iradius**3)*glass_d
        ball_o_mass=4.0/3.0*pi*(self.ball.radius**3)*glass_d
        I_ball=2.0/5.0*(ball_o_mass*self.ball.radius**2-ball_i_mass*self.iradius**2)+self.m_all*(self.ball.radius-h1+tube_len/2)**2
        return I_ball
    def get(self,h_m):
        self.m_liq=liquid_d*liquid_V-h_m
        
        
        
class tube:
    def __init__(self,frame,pos,radius,iradius,length):
        self.tube=cylinder(frame=frame,pos=pos,radius=radius,axis=(0,length,0),color=color.blue,opacity=0.2)
        self.iradius=iradius
        self.h=0 #liquid height in tube
        self.h_m=0 #liquid mass in tube
        self.tube.m=self.tube_mass(radius,iradius)
        #liquid
        self.liquid=cylinder(frame=frame,pos=pos+(0,1.726E-2-h1,0),axis=(0,self.h,0),radius=iradius,color=color.red,opacity=0.5)
        self.I=self.inertia()
        
    def tube_mass(self,radius,iradius):
        tube_mass_tem=pi*(radius**2-iradius**2)*tube_len*glass_d
        return tube_mass_tem
    def inertia(self):
        tube_i_mass=pi*self.iradius**2*self.tube.length*glass_d
        tube_o_mass=pi*self.tube.radius**2*self.tube.length*glass_d
        I_tube=(1.0/4*tube_o_mass*self.tube.radius**2+1.0/12*tube_o_mass*self.tube.length**2)-(1.0/4*tube_i_mass*self.iradius**2+1.0/12*tube_i_mass*self.tube.length**2)
        return I_tube
    def get(self,h):
        self.h=h
        self.h_m=liquid_d*h*pi*self.iradius**2
        self.liquid.axis=(0,self.h,0)
  
        
#Components
drinking_bird=frame()

#ground
ground=box(pos=(0,-5E-2,0),length=30E-2,height=0.01E-2,width=4E-2,color=color.blue)



Tube=tube(frame=drinking_bird,pos=vector(0,0,0)-(0,tube_len/2,0),radius=tube_r,iradius=tube_ir,length=tube_len)
Lower_ball=bird_ball(frame=drinking_bird,pos=Tube.tube.pos+(0,lower_ball_r-h1,0),radius=lower_ball_r,iradius=lower_ball_ir,liq_v=liquid_V,liq_d=liquid_d)
Upper_ball=bird_ball(frame=drinking_bird,pos=Tube.tube.pos+Tube.tube.axis+(0,upper_ball_r-h1,0),radius=upper_ball_r,iradius=upper_ball_ir,liq_v=0,liq_d=0)
beak=box(frame=drinking_bird,pos=Upper_ball.ball.pos+vector(upper_ball_r+beak_l/2,0,0),height=beak_h,width=beak_w,length=beak_l,m=beak_m)

#stick
support=cylinder(pos=(0,0,tube_r),axis=(0,-5E-2,0),radius=(0.1E-2),color=color.white)
drinking_bird.pos=(0,0,0)


#function
def rotation(vector,angle):
    new_vector=rotate(vector,abs(angle),angle)
    return new_vector

def Inertia(Tube,Lower_ball,Upper_ball):
    #Total
    total_I=Tube.I+Lower_ball.I+Upper_ball.I
    return total_I

def time_lapsed(dt):
    global J,L,phi,omega
    I=Inertia(Tube,Lower_ball,Upper_ball)
    #Torque
    #Torque from bird
    ###
    J_bird=(Lower_ball.m_all)*cross(vector(0,-g,0),rotation((Tube.tube.axis)/2,phi))-Upper_ball.m_all*cross(vector(0,
    -g,0),rotation((Tube.tube.axis)/2,phi))-(beak.m+sponge_m)*cross((0,-g,0),(rotation(beak.pos,phi)-drinking_bird.pos))
    #Torque from liquid
    liquid_com=rotation((Tube.liquid.axis-Tube.liquid.pos)/2,phi)
    J_liq=Tube.h_m*cross(vector(0,-g,0),(drinking_bird.pos-liquid_com))
    #Torque Total
    J=J_liq+J_bird
    #omega
    omega+=J/I*dt
    #damping 
    omega-=omega*b
    phi+=omega*dt
    drinking_bird.rotate(angle=abs(omega)*dt,axis=omega)
def delta_T(t):
    head_T = -0.01*(t%20.0) + T_room
    return head_T
#For Dichloromethane
def Clapeyron_equation(T):
    P_sat=exp((log(760/101.325)-10.08632*log(T)-6030.610/(T)+80.87786+9.812512E-6*(T)**2))*1.0336E5/760.0
    return P_sat
def BR_aka_BuzzRhyme(dP,Tube):
    h=dP/(liquid_d*g)
    Tube.get(h)
    Lower_ball.get(Tube.h_m)
#locate~
locate=arrow(pos=(0,0,0),axis=(0,0.25E-2,0),color=color.red)




#main
P_b=Clapeyron_equation(T_room)

while(True):
    rate(100000)
    t+=dt
    
    T_h=delta_T(t)
    P_h=Clapeyron_equation(T_h)
    #delta pressure
    delta_P=P_b-P_h
    BR_aka_BuzzRhyme(delta_P,Tube)
    #time lapsed
    time_lapsed(dt)
    #plot the change of source
    T_t.plot(pos=(t,T_h))
    P_t.plot(pos=(t,P_h))
    phi_t.plot(pos=(t,abs(phi)))
    







