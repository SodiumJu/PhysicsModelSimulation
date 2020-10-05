from visual import*
size=[0.15,0.10]
mass=[0.1,0.1]
colors=[color.yellow,color.green]
position=[vector(1,0.2,0),vector(0,0,0)]
velocity=[vector(-0.5,0,0),vector(0,0,0)]
def af_col_v(v1,v2,x1,x2):
    v1_prime=v1+(dot((v2-v1),(x1-x2))/(abs(x1-x2))**2)*vector(x1-x2)
    v2_prime=v2+(dot((v1-v2),(x2-x1))/(abs(x2-x1))**2)*vector(x2-x1)
    
    return(v1_prime,v2_prime)
scene=display(width=800,height=800,x=600,y=100,background=(0.3,0.3,0))
ball_reference=sphere(pos=(0,0,0),radius=0.02,color=color.red)

balls=[]
for i in [0,1]:
    balls.append(sphere(pos=position[i],radius=size[i],color=colors[i]))
    balls[i].v=velocity[i]
dt=0.001
while True:
    rate(1000)
    for a in balls:
        a.pos+=a.v*dt
    if(abs(balls[0].pos-balls[1].pos)<=size[0]+size[1] and
       dot(balls[0].pos-balls[1].pos,balls[0].v-balls[1].v)<=0):
       (balls[0].v,balls[1].v)=af_col_v(balls[0].v,balls[1].v,balls[0].pos,balls[1].pos)
