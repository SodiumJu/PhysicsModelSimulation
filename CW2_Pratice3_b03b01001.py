from visual import*
import ruler

#Yan-Ru's homework

#variable

g=9.8
size=0.25
drag_C=0.4 #drag coefficient C
drag_power=1.5 #drag_coef*v**drag_power
v_initial=12
theta=0
distance=0
pre_distance=0
counter=0
i=1 #variable for the angle

#scene

scene=display(title='bouncing projectile',center=(0,5,0),width=1200,height=800,background=(0.5,0.5,0))
floor=box(length=30,height=0.01,width=4,color=color.blue)
ball=sphere(radius=size,color=color.red,make_trail=True)
ruler_1=ruler.ruler(vector(-15,0,1),vector(1,0,0),unit=2.0,length=30.0,thickness=0.2)
ruler_2=ruler.ruler(vector(-15,0,1),vector(0,1,0),unit=1.0,length=10.0,thickness=0.2)



 
dt=0.001

while distance >= pre_distance:
    pre_distance=distance
    theta+=i
    ball.pos=vector(-15.0,size,0.0)
    ball.v=v_initial*vector(cos(theta*pi/180),sin(theta*pi/180),0.0)
    while ball.pos.y>=size:
        rate(1000)
        ball.pos+=ball.v*dt
        ball.v.y+=-g*dt
        ball.v.x+=-drag_C*(abs(ball.v.x)**drag_power)*dt
        ball.v.y+=-drag_C*(abs(ball.v.y)**drag_power)*dt
    distance=ball.pos.x+15.0
    print distance
print 'ok'
theta=theta-i
ball.pos=vector(-15.0,size,0.0)
ball.v=v_initial*vector(cos(theta*pi/180),sin(theta*pi/180),0.0)
while counter<3:
        rate(1000)
        ball.pos+=ball.v*dt
        ball.v.y+=-g*dt
        ball.v.x+=-drag_C*(abs(ball.v.x)**drag_power)*dt
        ball.v.y+=-drag_C*(abs(ball.v.y)**drag_power)*dt
        if ball.y<=size and ball.v.y<0:
            ball.v.y=-ball.v.y
            counter+=1
distance=ball.pos.x+15.0        
print "The distance that the ball touches the ground for the third time is %s m with the optimal angle of %s degrees."%(distance,theta)
print 'end' 
