#Yan-Ru homework
from visual import*
scene = display(width=800,height=800,center=(0,-0.5,0),background=(0.5,0.5,0))
#variable
L=1.0 #oringinal length of string
k=1E5 #N/m
string_force=0 #strength
r=2.0
ball_ms=1 #the mass of ball
ball_rs=0.03 #the radius of ball
degree=30 #this is degree
g=9.8 # acceleration of gravity
vz=0 #the velocity in z axis
dt=0.001 #time

#degree_to_radian_function
def theta_change(degree):
    theta=degree*pi/180
    return theta
theta=theta_change(degree)

  

#object
ball=sphere(pos=(L*sin(theta),-L*cos(theta),0),radius=ball_rs,mass=ball_ms,color=color.red,make_trail=True,trail_type="points",interval=20,retain=80)
string=cylinder(radius=0.006,pos=vector(0,0,0))
vz=sqrt(L*g*sin(theta)*tan(theta))


#force_function
def force(r):
    string_force=-k*(mag(r)-(L))*r/mag(r)
    return string_force


#period (useless function)
"""def T(t,E,bvx):
    if E==False:
        if bvx>0:
            print t*2
            t=0
            E=True
            
                
    elif E==True:
        if bvx<0:
            print t*2
            t=0
            E=False  """

#for printing the period            
def print_time(t):
    print "The period is %s"%(t*2)
    t=0
    return t
    
                
#main       
def pendulum():
    ball.v=vector(0,0,vz) #ball_initial_v
    t=0
    e=False
    
    while True:
        rate(1000)
        string.axis=ball.pos-string.pos
        r=string.axis
        ball.a=vector(0,-g,0)+force(r)/ball_ms
        ball.v += ball.a*dt
        ball.pos += ball.v*dt

        #record the time
        t=t+dt

        if e==False:
            if ball.v.x>0:
                t=print_time(t)
                e=True
        elif e==True:
            if ball.v.x<0:
                t=print_time(t)
                e=False
        
#theoretical value
def the_value(L,theta):
    T=2*pi*sqrt(L*cos(theta)/g)
    return T
    
T=the_value(L,theta)
print "The theoretical value of the period is %s"%(T)

#simulation
pendulum()
 
        

    
