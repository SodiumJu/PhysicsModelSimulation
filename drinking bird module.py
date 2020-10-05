from visual import*
from visual.graph import*
#unit:kg/m/s
#variable
#balls:
class drinking_bird:
    def __init__(self,lower_ball_r=0.895E-2,lower_ball_ir=0.865E-2,
                 upper_ball_r=0.735E-2,upper_ball_ir=0.705E-2,
                 tube_len=6.68E-2,tube_r=0.285E-2,tube_ir=0.2E-2,
                 tube_m=0.865E-3,glass_d=2.10E3,h1=0.2E-2,dt=0.01E-2,
                 J=vector(0,0,0),L=vector(0,0,0),I=0,g=9.8,phi=vector(0,0,0),
                 omega=vector(0,0,0),b=0.0001,t=0,sponge_m=0.0013,
                 T_room=295.44,T_h=0,P_h=0,P_b=0,delta_P=0,liquid_d=1.336E3,
                 liquid_V=2.711E-6,beak_h=0.1E-2,beak_l=0.4E-2,beak_w=0.2E-2,
                 beak_m=1.0E-3):
        self.__dict__['lower_ball_r']=float(lower_ball_r)
        self.__dict__['lower_ball_ir']=float(lower_ball_ir)
        self.__dict__['upper_ball_r']=float(upper_ball_r)
        self.__dict__['upper_ball_ir']=float(upper_ball_ir)
        self.__dict__['tube_len']=float(tube_len)
        self.__dict__['tube_r']=float(tube_r)
        self.__dict__['tube_ir']=float(tube_ir)
        self.__dict__['glass_d']=float(glass_d)
        self.__dict__['h1']=float(h1)
        self.__dict__['dt']=float(dt)
        self.__dict__['I']=float(I)
        self.__dict__['g']=float(g)
        self.__dict__['sponge_m']=float(sponge_m)
        self.__dict__['t']=float(t)
        self.__dict__['b']=float(b)
        self.__dict__['T_room']=float(T_room)
        self.__dict__['T_h']=float(T_h)
        self.__dict__['P_h']=float(P_h)
        self.__dict__['P_b']=float(P_b)
        self.__dict__['delta_P']=float(delta_P)
        self.__dict__['liquid_d']=float(liquid_d)
        self.__dict__['liquid_V']=float(liquid_V)
        self.__dict__['beak_h']=float(beak_h)
        self.__dict__['beak_l']=float(beak_l)
        self.__dict__['beak_w']=float(beak_w)
        self.__dict__['beak_m']=float(beak_m)

        self.__dict__['J']=vector(J)
        self.__dict__['L']=vector(L)
        self.__dict__['phi']=vector(phi)
        self.__dict__['omega']=vector(omega)

        self.drinking_bird=frame()
        self.Tube=tube(frame=self.drinking_bird,pos=vector(0,0,0)-(0,self.tube_len/2,0),radius=self.tube_r,
            iradius=self.tube_ir,length=self.tube_len,density=self.glass_d,liq_d=liquid_d)
        
        self.Lower_ball=bird_ball(frame=self.drinking_bird,pos=self.Tube.tube.pos+(0,self.lower_ball_r-self.h1,0),
            radius=self.lower_ball_r,iradius=self.lower_ball_ir,liq_v=self.liquid_V,liq_d=self.liquid_d,density=self.glass_d)
        
        self.Upper_ball=bird_ball(frame=self.drinking_bird,pos=self.Tube.tube.pos+self.Tube.tube.axis+(0,self.upper_ball_r-self.h1,0),
            radius=self.upper_ball_r,iradius=self.upper_ball_ir,liq_v=0,liq_d=0,density=self.glass_d)
        
        self.beak=box(frame=self.drinking_bird,pos=self.Upper_ball.ball.pos+vector(self.upper_ball_r+self.beak_l/2,0,0),
            height=self.beak_h,width=self.beak_w,length=self.beak_l,m=self.beak_m,color=color.red)
        self.eye1=points(frame=self.drinking_bird,pos=self.Upper_ball.ball.pos+vector(self.upper_ball_r-1.0E-3,2.0E-3,-2.0E-3),size=10,material=materials.emissive,color=color.red)
        self.eye2=points(frame=self.drinking_bird,pos=self.Upper_ball.ball.pos+vector(self.upper_ball_r-1.0E-3,2.0E-3,2.0E-3),size=10,material=materials.emissive,color=color.red)
        self.support=cylinder(pos=(0,0,self.tube_r),axis=(0,-5E-2,0),radius=(0.1E-2),color=color.red,opacity=0.7)
        self.drinking_bird.pos=(0,0,0)
        self.locate=arrow(pos=(0,0,0),axis=(0,0.25E-2,0),color=color.red)
        self.main(self.dt)

    def main(self,dt):
        self.P_b=self.Clapeyron_equation(self.T_room)
        while(True):
            rate(10000)
            self.t+=dt
            
            self.T_h=self.delta_T(self.t)
            self.P_h=self.Clapeyron_equation(self.T_h)
            #delta pressure
            self.delta_P=self.P_b-self.P_h
            self.BR_aka_BuzzRhyme(self.delta_P,self.Tube)
            #time lapsed
            self.time_lapsed(dt)

        
    def rotation(self,vector,angle):
        new_vector=rotate(vector,abs(angle),angle)
        return new_vector

    def Inertia(self):
        #Total
        total_I=self.Tube.I+self.Lower_ball.I+self.Upper_ball.I
        return total_I

    def time_lapsed(self,dt):
        #global self.J,self.L,self.phi,self.omega
        self.I=self.Inertia()
        #Torque
        #Torque from bird
        ###
        J_bird=(self.Lower_ball.m_all)*cross(vector(0,-self.g,0),self.rotation((self.Tube.tube.axis)/2,self.phi))-self.Upper_ball.m_all*cross(vector(0,
        -self.g,0),self.rotation((self.Tube.tube.axis)/2,self.phi))-(self.beak.m+self.sponge_m)*cross((0,-self.g,0),(self.rotation(self.beak.pos,self.phi)-self.drinking_bird.pos))
        #Torque from liquid
        liquid_com=self.rotation((self.Tube.liquid.axis-self.Tube.liquid.pos)/2,self.phi)
        J_liq=self.Tube.h_m*cross(vector(0,-self.g,0),(self.drinking_bird.pos-liquid_com))
        #Torque Total
        self.J=J_liq+J_bird
        #omega
        self.omega+=self.J/self.I*dt
        #damping 
        self.omega-=self.omega*self.b
        self.phi+=self.omega*dt
        self.drinking_bird.rotate(angle=abs(self.omega)*dt,axis=self.omega)
    def delta_T(self,t):
        head_T = -0.01*(t%20.0) + self.T_room
        return head_T
    #For Dichloromethane
    def Clapeyron_equation(self,T):
        P_sat=exp((log(760/101.325)-10.08632*log(T)-6030.610/(T)+80.87786+9.812512E-6*(T)**2))*1.0336E5/760.0
        return P_sat
    def BR_aka_BuzzRhyme(self,dP,Tube):
        h=dP/(self.liquid_d*self.g)
        self.Tube.get(h)
        self.Lower_ball.get(self.Tube.h_m)


class bird_ball:
    def __init__(self,frame,pos,radius,iradius,liq_v,liq_d,density):
        self.ball=sphere(frame=frame,pos=pos,radius=radius,color=color.cyan,opacity=0.7)
        self.iradius=iradius
        self.density=density
        self.ball.m=self.glass_ball_mass(radius,iradius)
        self.liq_v=liq_v
        self.liq_d=liq_d
        self.m_liq=liq_v*liq_d
        self.m_all=self.ball.m+self.m_liq
        self.I=self.inertia()
            
    def glass_ball_mass(self,radius,iradius):
        ball_m_temp=4.0/3.0*pi*((radius)**3-(iradius)**3)*self.density
        return ball_m_temp
    def inertia(self):
        ball_i_mass=4.0/3.0*pi*(self.iradius**3)*self.density
        ball_o_mass=4.0/3.0*pi*(self.ball.radius**3)*self.density
        #!!
        I_ball=2.0/5.0*(ball_o_mass*self.ball.radius**2-ball_i_mass*self.iradius**2)+self.m_all*(self.ball.radius-0.2E-2+6.68E-2/2)**2
        return I_ball
    def get(self,h_m):
        self.m_liq=self.liq_v*self.liq_v-h_m
            
            
            
class tube:
    def __init__(self,frame,pos,radius,iradius,length,density,liq_d):
        self.tube=cylinder(frame=frame,pos=pos,radius=radius,axis=(0,length,0),color=color.yellow,opacity=0.3)
        self.iradius=iradius
        self.length=length
        self.density=density
        self.liq_d=liq_d
        self.h=0 #liquid height in tube
        self.h_m=0 #liquid mass in tube
        self.tube.m=self.tube_mass(radius,iradius)
        #liquid !!
        self.liquid=cylinder(frame=frame,pos=pos+(0,1.726E-2-0.2E-2,0),axis=(0,self.h,0),radius=iradius,color=color.red,opacity=0.5)
        self.I=self.inertia()
        
    def tube_mass(self,radius,iradius):
        tube_mass_tem=pi*(radius**2-iradius**2)*self.length*self.density
        return tube_mass_tem
    def inertia(self):
        tube_i_mass=pi*self.iradius**2*self.tube.length*self.density
        tube_o_mass=pi*self.tube.radius**2*self.tube.length*self.density
        I_tube=(1.0/4*tube_o_mass*self.tube.radius**2+1.0/12*tube_o_mass*self.tube.length**2)-(1.0/4*tube_i_mass*self.iradius**2+1.0/12*tube_i_mass*self.tube.length**2)
        return I_tube
    def get(self,h):
        self.h=h
        self.h_m=self.liq_d*h*pi*self.iradius**2
        self.liquid.axis=(0,self.h,0)

if __name__=='__main__':
    scene = display(width=800, height=800,background=(1,1,1))
    ground=box(pos=(0,-5E-2,0),length=5E-2,height=0.01E-2,width=4E-2,color=color.black)    
    a=drinking_bird()
      
            

 
    







