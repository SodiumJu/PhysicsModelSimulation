from visual import*
ee=False
count=0
time=0
dt = 0.0002

M,R,w,g=0.5,0.10,0.05,9.8
I=0.5*M*R**2
l,r=0.12,0.005
theta=70*pi/180.0
Omega=10*2*pi*vector(cos(theta),sin(theta),0)
lr=0.045

scene=display(width=1000,height=1000,range=0.6,background=(0.2,0.2,0))
spintop = frame()
shaft = cylinder(frame=spintop, pos=(0,0,0), axis =(l,0,0), radius=r, material = materials.wood)

disk = cylinder(frame=spintop, pos=(lr-w/2,0,0), axis = (w, 0, 0), radius=R, material = materials.wood)
spintop.pos = (0,0,0)
base = cone(pos=(0,-0.2,0), axis=(0,0.2,0), color = color.green, radius=0.1)

ball=sphere(radius=0.0001,make_trail=True,pos=norm(Omega)*shaft.axis.mag,color=color.red)
L=I*Omega #Angular momentum
theoretical_period=2*pi*I*Omega.mag/(M*g*lr)
print 'The theoretical period : ',theoretical_period

while True:
    rate(5000)
    spintop.axis = norm(Omega)
    delta_angle = mag(Omega)*dt
    spintop.rotate(angle=delta_angle, axis=spintop.axis)
    ball.pos=norm(Omega)*shaft.axis.mag
    J=M*(lr)*(cross(norm(Omega),vector(0,-g,0)))
    L+=J*dt
    Omega=L/I
    time=time+1*dt
    
    if ee==False:
        if (Omega.z<=0):
            count+=1
            if count>1:
                print 'The period : ',time,'\tseconds'
            time=0
            ee=True
    elif ee==True:
        if (Omega.z>=0):
            
            ee=False
    
