from visual import*


#variable of spring
r=0.3 #spring oringinal length
k=25.0 #spring constant

#variable of system
size=[0.05,0.04,0.03]
mass=[0.3,0.4,0.3]
colors=[color.yellow,color.green,color.blue] #ball color
position=[vector(0,0,0),vector(0,-r,0),vector(0.25,-0.45,0)] #ball initial position
velocity=[vector(0,0,0),vector(0,0,0),vector(-0.2,0.42,0)] #ball initial velocity

#event variable
colli=False
dt=0.001
check=False
e=False

#variable of whatever
CMV=vector(0,0,0)   #velocity of C.M.
IVPEa=0 #Internal Vibrational Potential Energy averaged over a period
IVKEa=0 #Internal Vibrational Kinetic Energy averaged over a period
IRKEa=0 #Internal Rotational Kinetic Energy averaged over a period
CMKE=0  #Center of Mass Kinetic Energy
KEb2=0  #Kinetic Energy of ball[2]
TE=0    #Total Energy 
LMsps=0 #Linear Momentum of the spring‐ball system
LMb2=0  #Linear Momentum of ball [2]
TLM=0   #Total Linear Momentum

#function for Internal Vibrational Potential Energy averaged over a period
def IVPEaf():
    global IVPEa
    IVPEa=IVPEa+(0.5)*k*(abs(balls[0].pos-balls[1].pos)-r)**2
    return IVPEa
def IVKEaf():
    global IVKEa
    IVKEa=IVKEa+((0.5)*mass[0]*mag(proj(balls[0].v-CMV,spring.axis))**2+(0.5)*mass[1]*mag(proj(balls[1].v-CMV,spring.axis))**2)
    return IVKEa
def IRKEaf():
    global IRKEa
    #I=(mass[0]*((mag(spring.axis)*(4.0/7.0))**2) + mass[1]*((mag(spring.axis)*(3.0/7.0))**2)) #Inertia
    #omega=v/r
    #vvertical=balls[0].v-CMV #vertical vector of ball.v relative to CMV
    #omega=mag(vvertical)/(mag(spring.axis)*(4.0/7.0))
    #IRKEa=IRKEa+(0.5)*I*omega**2
    IRKEa=IRKEa+(0.5)*mass[0]*(mag(cross(balls[0].v-CMV,spring.axis))/spring.axis.mag)**2+(0.5)*mass[1]*(mag(cross(balls[1].v-CMV,spring.axis))/spring.axis.mag)**2
    return IRKEa
def CMKEf():
    global CMKE
    CMKE=(0.5)*(mass[0]+mass[1])*CMV.mag**2
    #CMKE=(CMV.mag*(mass[0]+mass[1]))**2/(2*(mass[0]+mass[1]))
    return CMKE
def KEb2f():
    global KEb2
    KEb2=(0.5)*mass[2]*(balls[2].v.mag**2)
    return KEb2
def TEf():
    global TE
    global t
    TE = IVPEa/t+IVKEa/t+IRKEa/t+(CMKE+KEb2)
    return TE
def LMspsf():
    global LMsps
    LMsps=(balls[0].v*mass[0])+(balls[1].v*mass[1])
    return LMsps
def LMb2f():
    global LMb2
    LMb2 = balls[2].v*mass[2]
    return LMb2
def TLMf():
    global TLM
    TLM=LMsps+LMb2
    return TLM

#function for velocity of C.M.
def CMVf():
    global CMV
    CMV=((balls[0].v*mass[0])+(balls[1].v*mass[1]))/(mass[0]+mass[1])
    return CMV
    

#recorder
t=0
springlength=[]

#function for collision
def af_col_v(v1,v2,x1,x2,m1,m2):
    v1_prime= v1 + (2*m2/(m1+m2))*(dot((v2-v1),(x1-x2))/(abs(x1-x2)**2))*vector(x1-x2)
    v2_prime= v2 + (2*m1/(m1+m2))*(dot((v1-v2),(x2-x1))/(abs(x2-x1)**2))*vector(x2-x1)
    return(v1_prime,v2_prime)

#for printing everything over the period            
def printer():
    global IVPEa,IVKEa,IRKEa,CMKE,KEb2,TE,LMsps,LMb2,TLM,t
    
    print "----------------------------------------------------------------------------"
    print "Kinetic Energy of ball3 = %s"%(before_KEb2)
    print "Linear Momentum of ball3 = %s"%(before_LMb2)

    print "----------------------------After collision---------------------------------"
    print "The period is %s, and the time is %s"%(t/1000,t/1000)
    print "Internal Vibrational Potential Energy averaged over a period = %s"%(IVPEa/t)
    print "Internal Vibrational Kinetic Energy averaged over a period = %s"%(IVKEa/t)
    print "Internal Rotational Kinetic Energy averaged over a period = %s"%(IRKEa/t)
    print "Center of Mass Kinetic Energy = %s"%(CMKE)
    print "Kinetic Energy of ball3 = %s"%(KEb2)
    print "Total Energy = %s"%(TE)
    print "Linear Momentum of the spring‐ball system = %s"%(LMsps)
    print "Linear Momentum of ball3 = %s"%(LMb2)
    print "Total Linear Momentum =%s"%(TLM)
    print "----------------------------------------------------------------------------"
    
    t,IVPEa,IVKEa,IRKEa,CMKE,KEb2=0,0,0,0,0,0
    

#function of spring system
def springandballs():
    global t,e
    spring.pos=balls[1].pos
    spring.axis=balls[0].pos-balls[1].pos
    
    spring_force=-k*(mag(spring.axis)-(r))*spring.axis/mag(spring.axis)
    balls[0].a,balls[1].a=vector(0,0,0)+spring_force/mass[0],vector(0,0,0)-spring_force/mass[1]
        
    
    balls[0].v+= balls[0].a*dt
    balls[0].pos+=balls[0].v*dt
    
    balls[1].v+= balls[1].a*dt
    balls[1].pos+=balls[1].v*dt
    q=len(springlength)
    
    if (colli==True):
        t=t+1
        springlength.append(mag(spring.axis))
        CMVf(),IVPEaf(),IVKEaf(),IRKEaf(),CMKEf(),KEb2f(),TEf(),LMspsf(),LMb2f(),TLMf()   #all the functions
        if (q>=2):
            if e==False:
                if (springlength[q-1]<=springlength[q-2]):
                    e=True
            elif e==True:
                if (springlength[q-1]>=springlength[q-2]):
                    printer()
                    e=False
        
    
    

#function of collision in 2D(blue ball and green ball)
def collision():
    global colli
    if(abs(balls[0].pos-balls[2].pos)<=size[0]+size[2] and
       dot(balls[0].pos-balls[2].pos,balls[0].v-balls[2].v)<=0):
       (balls[0].v,balls[2].v)=af_col_v(balls[0].v,balls[2].v,balls[0].pos,balls[2].pos,mass[0],mass[2])
       colli=True
    return colli   

#main
scene=display(width=800,height=800,x=600,y=100,background=(0.3,0.3,0))
ball_reference=sphere(pos=(0,0,0),radius=0.02,color=color.red) #reference ball
spring=helix(radius=0.02,thickness=0.01) #spring

balls=[]
for i in [0,1,2]:
    balls.append(sphere(pos=position[i],radius=size[i],color=colors[i],make_trail=True ))
    balls[i].v=velocity[i]
    
before_KEb2=KEb2f() #
before_LMb2=LMb2f() #


while True:
    rate(1000)
    for ball in balls:
        ball.pos+=ball.v*dt
    collision()
    springandballs()
    if(colli==True and check==False):
        print '-----------------------------------Collision--------------------------------'
        check=True


