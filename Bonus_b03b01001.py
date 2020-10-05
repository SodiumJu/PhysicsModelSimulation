#Yan-Ru Ju Bonus homework
from visual import*
scene = display(width=800,height=800,center=(0,-0.5,0),background=(0.5,0.5,0))
#variable
L=2.0 #oringinal length of string
k=1E5 #N/m
string_force=0 #strength
r=2.0
ball_ms=1 #the mass of ball
ball_rs=0.03 #the radius of ball
degree=30 #this is degree
g=9.8 # acceleration of gravity
vz=0 #the velocity in z axis
dt=0.001 #time
omega=6.94*1E-4 #the rotational angular velocity of the earth
delta=23.5

#degree_to_radian_function
def theta_change(degree):
    theta=degree*pi/180
    return theta
theta=theta_change(degree)

  

#object
ball=sphere(pos=(L*sin(theta),-L*cos(theta),0),radius=ball_rs,mass=ball_ms,color=color.red,make_trail=True,trail_type="points",interval=20,retain=80)
string=cylinder(radius=0.006,pos=vector(0,0,0))
#vz=sqrt(L*g*sin(theta)*tan(theta))


#force_function
def force(r):
    string_force=-k*(mag(r)-(L))*r/mag(r)
    return string_force

#Coriolis acceleration
def Coriolis(ball,omega,theta):
    theta=theta_change(theta)
    Cori_a=2*omega*vector(-ball.v.z*sin(theta),ball.v.z*cos(theta),ball.v.x*sin(theta)-ball.v.y*cos(theta))
    return Cori_a            
#main       
def pendulum():
    ball.v=vector(0,0,vz) #ball_initial_v
    n=0 #counter
    e=False
    
    while True:
        rate(1000000)
        string.axis=ball.pos-string.pos
        r=string.axis
        Cori_a=Coriolis(ball,omega,theta)
        ball.a=vector(0,-g,0)+force(r)/ball_ms+Cori_a
        ball.v += ball.a*dt
        ball.pos += ball.v*dt

        #record the time
        

        if e==False:
            if ball.v.x>0:
                n=n+1
                if n==1:
                    A=vector(ball.x,0,ball.z)-vector(0,0,0)
                    arrowA=arrow(color=color.white,axis=A/mag(A),shaftwidth=0.05)
                    print "%s time"%(n)
                elif n==1000:
                    B=vector(ball.x,0,ball.z)-vector(0,0,0)
                    arrowB=arrow(color=color.black,axis=B/mag(B),shaftwidth=0.05)
                    print "%s times"%(n)
                    diff_AB=diff_angle(A,B)
                    print "The angle between is %s"%(diff_AB*53)
                    
                e=True
        elif e==True:
            if ball.v.x<0:
                e=False
        

    


#simulation
pendulum()
