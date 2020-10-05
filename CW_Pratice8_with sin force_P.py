from visual import*
from visual.graph import*
size,m=0.02,0.2 #ball size = 0.02 m, ball mass = 0.2 kg
L,k=0.2,20.0 #spring original length = 0.2m,force constant = 20 N/m
b=0.1*m*sqrt(k/m) #damping factor
f_a=0.1 #constant
omega_d=sqrt(k/m) #angular velocity
amplitude=0.03 #amplitude
T=2*pi/omega_d #period
loop_t=0 #time for loop
P=0 #Power

scene1=gdisplay(y=400,width=800,height=300,xtitle='t',ytitle='x',background=(0.5,0.5,0))
scene2=gdisplay(y=400,width=800,height=300, xtitle='t',ytitle='average_power',background=(0.4,0.4,0))

x=gcurve(color=color.red,gdisplay=scene1)
p=gdots(color=color.cyan,gdisplay=scene2) #add these two lines before scene1=....
 
scene=display(width=800,height=400,fov=0.03,range=0.5,center=(0.3,0,0),background=(0.5,0.5,0))
wall_left=box(length=0.005,height=0.3,width=0.3,color=color.blue) #left wall
ball=sphere(radius=size,color=color.green)
spring=helix(radius=size,thickness=0.01)



wall_left.pos=vector(0,0,0)
ball.pos,ball.v,ball.m=vector(L,0,0),vector(0,0,0),m

spring.pos=wall_left.pos

t,dt=0,0.001


def Spring_Force(Length):
    spring_force=-k*(mag(spring.axis)-Length)*norm(spring.axis)
    return spring_force

def Sinusoidal_Force(t):
    sin_force=vector(f_a*sin(omega_d*t),0,0)

    return sin_force

def Total_Force():
    total_force=spring_force+sin_force-b*ball.v
    return total_force




print omega_d
while True:
    rate(1000)                                              #spring extended from spring endpoint A to ball
    
    
    spring.axis=ball.pos-spring.pos
    spring_force=Spring_Force(L)                                   #spring force vector
    sin_force=Sinusoidal_Force(t)                                   #exerted sin_force
    total_force=Total_Force()
    ball.a=total_force/ball.m
    ball.v+=ball.a*dt                                       #ball acceleration=spring force/m
    ball.pos+=ball.v*dt
    t+=dt
    loop_t+=dt
    x.plot(pos=(t,ball.pos.x-L))
    P+=dot(sin_force,ball.v)
    
    #for the data related to Period
    if(loop_t>=T):
        average_power=P/loop_t
        P=0
        
        loop_t=0
        p.plot(pos=(t,average_power))
        average_power=0
        
        
    

