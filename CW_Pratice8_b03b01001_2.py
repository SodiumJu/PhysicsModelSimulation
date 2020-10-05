#Yan-Ru Ju
from visual import*
from visual.graph import*

#variables
size_1,size_2,m=0.02,0.04,0.2 #ball size = 0.02 m, ball mass = 0.2 kg
L,k,K=0.2,20.0,5.0 #spring original length = 0.2m,force constant = 20 N/m
b_1,b_2=0.05*m*sqrt(k/m),0.0025*m*sqrt(k/m)#damping factor
count=0 #count
omega = [0.1*i + 0.7*sqrt((k+K)/m) for i in range(1, int(0.5*sqrt((k+K)/m)/0.1))]

#scene
scene3=gdisplay(y=400,width=800,height=300, xtitle='omega',ytitle='average_power',background=(0.4,0.4,0))
p=gcurve(color=color.cyan,gdisplay=scene3)

#function

def Sinusoidal_Force(t):
    sin_force=vector(f_a*sin(omega_d*t),0,0)

    return sin_force


def Resistance_Force(b,ball_v):
    res_force=-b*ball_v        
        
    return res_force

class obj:pass
wall_right,wall_left,ball_1,ball_2,spring_1,spring_2,spring_3=obj(),obj(),obj(),obj(),obj(),obj(),obj()

print 'Wait for a moment!Thanks a lot.'
for omega_d in omega:

    f_a=0.1 #constant
    amplitude=0.003 #amplitude
    T=2*pi/omega_d #period
    loop_t=0 #time for loop
    P=0 #Power
    t,dt=0,0.001 #time 
    #scene=display(width=800,height=400,fov=0.03,range=0.5,center=(0.3,0,0),background=(0.5,0.5,0))

    #walls
    #wall_left=box(length=0.005,height=0.3,width=0.3,color=color.blue) #left wall
    #wall_right=box(length=0.005,height=0.3,width=0.3,color=color.blue) #right wall

    #2 balls
    #ball_1=sphere(radius=size_2,color=color.green)
    #ball_2=sphere(radius=size_1,color=color.red)

    #3 springs
    #spring_1=helix(radius=size_1,thickness=0.01)
    #spring_2=helix(radius=size_1,thickness=0.005)
    #spring_3=helix(radius=size_1,thickness=0.01)


    #walls' position
    wall_left.pos,wall_right.pos=vector(0,0,0),vector(3*L,0,0)

    #balls
    ball_1.pos,ball_1.v,ball_1.m=vector(L,0,0),vector(0,0,0),m
    ball_2.pos,ball_2.v,ball_2.m=vector(2*L,0,0),vector(0,0,0),m


    #main
    while True:
        rate(100000)                                              
        t+=dt
        loop_t+=dt
        
        spring_1.pos=wall_left.pos
        spring_2.pos=ball_1.pos
        spring_3.pos=ball_2.pos
        
        spring_1.axis=ball_1.pos-spring_1.pos
        spring_2.axis=ball_2.pos-ball_1.pos
        spring_3.axis=wall_right.pos-spring_3.pos
        
        
        #spring force
        spring_1_force=-k*(mag(spring_1.axis)-L)*norm(spring_1.axis)
        spring_2_force=-K*(mag(spring_2.axis)-L)*norm(spring_2.axis)
        spring_3_force=-k*(mag(spring_3.axis)-L)*norm(spring_3.axis)

        sin_force=Sinusoidal_Force(t)   
        
        total_1_force=spring_1_force-spring_2_force+sin_force+Resistance_Force(b_1,ball_1.v)    #force on ball_1
        total_2_force=spring_2_force-spring_3_force+Resistance_Force(b_2,ball_2.v)  #force on ball_2
        
        
        ball_1.a=total_1_force/ball_1.m
        ball_2.a=total_2_force/ball_2.m
        
        ball_1.v+=ball_1.a*dt                                       
        ball_1.pos+=ball_1.v*dt

        ball_2.v+=ball_2.a*dt                                       
        ball_2.pos+=ball_2.v*dt
        
        P+=dot(sin_force,ball_1.v)

        if(loop_t>=T):
            count+=1
            average_power=P/T

            if count>=100:
                p.plot(pos=(omega_d,average_power))
                count=0
                P=0
                loop_t=0
                average_power=0
                break
            
            
            P=0
            loop_t=0
            average_power=0

    
    
    
       
        
    

