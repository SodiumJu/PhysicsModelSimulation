from visual import*
from visual.graph import*
size,m=0.02,0.2 #ball size =
L,k=0.2,20.0 #spring original length = 0.2m,force constant = 20 N/m
amplitude=0.03

scene1=gdisplay(y=400,width=800,height=300,xtitle='t',ytitle='x',background=(0.5,0.5,0))
x=gcurve(color=color.red,gdisplay=scene1)
scene=display(width=800,height=400,fov=0.03,range=0.5,center=(0.3,0,0),background=(0.5,0.5,0))
wall_left=box(length=0.005,height=0.3,width=0.3,color=color.blue) #left wall
ball=sphere(radius=size,color=color.red)
spring=helix(radius=size,thickness=0.01)
wall_left.pos=vector(0,0,0)
ball.pos,ball.v,ball.m=vector(L+amplitude,0,0),vector(0,0,0),m

spring.pos=wall_left.pos

t,dt=0,0.001
while True:
    rate(1000)                                              #spring extended from spring endpoint A to ball
    spring.axis=ball.pos-spring.pos
    spring_force=-k*(mag(spring.axis)-L)*norm(spring.axis)  #spring force vector
    ball.a=spring_force/ball.m
    ball.v+=ball.a*dt                                       #ball acceleration=spring force/m
    ball.pos+=ball.v*dt
    t+=dt
    x.plot(pos=(t,ball.pos.x-L))
    

