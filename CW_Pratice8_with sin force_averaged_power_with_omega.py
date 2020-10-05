from visual import*
from visual.graph import*
size,m=0.02,0.2 #ball size = 0.02 m, ball mass = 0.2 kg
L,k=0.2,20.0 #spring original length = 0.2m,force constant = 20 N/m
b=0.05*m*sqrt(k/m) #damping factor
f_a=0.1 #constant
amplitude=0.03 #amplitude
loop_t=0 #time for loop
P=0 #Power
count=0 #times

##omega_d=(k/m)**(0.5) #angular velocity

def Spring_Force(Length):
        spring_force=-k*(mag(spring.axis)-Length)*norm(spring.axis)
        return spring_force

def Sinusoidal_Force(t,omega_d):
    sin_force=vector(f_a*sin(omega_d*t),0,0)
    return sin_force

def Total_Force():
    total_force=spring_force+sin_force-b*ball.v
    return total_force

omega = [0.1*i + 0.7*sqrt(k/m) for i in range(1, int(0.5*sqrt(k/m)/0.1))]
print omega

##scene1=gdisplay(y=400,width=800,height=300,xtitle='t',ytitle='x',background=(0.5,0.5,0))
##scene2=gdisplay(y=700,width=800,height=300, xtitle='t',ytitle='average_power',background=(0.4,0.4,0))
scene3=gdisplay(y=400,width=800,height=800, xtitle='omega',ytitle='average_power',background=(0.4,0.4,0))

##x=gcurve(color=color.red,gdisplay=scene1)
##p=gdots(color=color.cyan,gdisplay=scene2) #add these two lines before scene1=....
q=gcurve(color=color.cyan,gdisplay=scene3)

for omega_d in omega:
    
    T=2*pi/omega_d #period



    
    
    
    
     
    ##scene=display(width=800,height=400,fov=0.03,range=0.5,center=(0.3,0,0),background=(0.5,0.5,0))
    ##wall_left=box(length=0.005,height=0.3,width=0.3,color=color.blue) #left wall
    ##ball=sphere(radius=size,color=color.green)
    ##spring=helix(radius=size,thickness=0.01)

    class obj: pass
    wall_left, ball, spring = obj(), obj(), obj()

    wall_left.pos=vector(0,0,0)
    ball.pos,ball.v,ball.m=vector(L,0,0),vector(0,0,0),m

    spring.pos=wall_left.pos

    t,dt=0,0.001


    






    while True:
        #rate(1000000)                                              #spring extended from spring endpoint A to ball
        
        
        spring.axis=ball.pos-spring.pos
        spring_force=Spring_Force(L)                                  #spring force vector
        sin_force=Sinusoidal_Force(t,omega_d)                                   #exerted sin_force
        total_force=Total_Force()
        
        ball.a=(total_force)/ball.m
        ball.v+=ball.a*dt                                       #ball acceleration=spring force/m
        ball.pos+=ball.v*dt
        t+=dt
        loop_t+=dt
        #x.plot(pos=(t,ball.pos.x-L))
        P+=dot(sin_force,ball.v)
        
        
        #for the data related to Period
        if(loop_t>=T):
            count+=1
            average_power=P/T
            
            #plot averaged power comsumed
            if (count>=100):
                q.plot(pos=(omega_d,average_power))
                average_power=0
                P=0           
                loop_t=0
                spring_force=0
                sin_force=0
                total_force=0
                t=0
                count=0
                
                break
            
            #print count ,average_power
            #p.plot(pos=(t,average_power))
            average_power=0
            P=0           
            loop_t=0

        
        
        
    

