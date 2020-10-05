from visual import*
import ruler

#Yan-Ru's homework

#variable

g=9.8
sizes=[0.05,0.04]
ms=[0.2,0.15]
r,k=0.5,15 #r is spring original length,k is force constant=10N/m   


#scene

scene=display(title='two balls with a spring',center=(0,-0.2,0),width=800,height=800,background=(0.5,0.5,0))
#ceiling=box(length=0.8,height=0.005,width=0.8,color=color.blue)



balls=[sphere(radius=sizes[0],mass=ms[0],color=color.red),sphere(radius=sizes[1],mass=ms[1])]
balls[0].pos,balls[1].pos=vector(0,0,0),vector(-r-0.2,0,0)
balls[0].v,balls[1].v=vector(0,0,0),vector(0,0,0)
spring=helix(radius=0.02,thickness=0.01)

t=0
dt=0.001
while True:
    rate(1000)
    t=t+dt
    
    spring.pos=balls[1].pos
    spring.axis=balls[0].pos-balls[1].pos

    spring_force=-k*(mag(spring.axis)-(r))*spring.axis/mag(spring.axis)
    balls[0].a,balls[1].a=vector(0,0,0)+spring_force/ms[0],vector(0,0,0)-spring_force/ms[1]
    

    balls[0].v+= balls[0].a*dt
    balls[0].pos+=balls[0].v*dt

    balls[1].v+= balls[1].a*dt
    balls[1].pos+=balls[1].v*dt
    if balls[0].x>=0 and balls[0].v>0:
        x=(balls[0].x*ms[0]+balls[1].x*ms[1])/(ms[0]+ms[1])
        print "averaged center of mass(x) = %s ,period of the oscillation = %s"%(x,t)
        print 'finished'
        t=0
    
    
    
        
