from visual import*
from random import random	#generate random numbers
from visual.graph import*

N = 50	#number of the He atoms
L = ((24.4E-3/(6E23))*N)**(1/3.0)/2 #/2? Length of cubic container box
m,size = 4E-3/6E23,310E-12	#atom mass,radius are ten times bigger for easier collision 
L_size = L-size #L-size ,used many times in programs
k,T = 1.38E-23,298.0 #boltsmann constant,T=temperature in unit K
t,dt = 0,0.5E-13
vrms=(3*k*T/m)**0.5
touch_wall = False

#collector
atoms=[]
pressure = 0;


#histogram on intialization
deltav = 100
vdist = gdisplay(x=800,y=0,ymax=N*deltav/1000,width=500,height=300,xtitle='v',ytitle='dN')
theory =gcurve(color=color.cyan)
dv=10
for v in arange(0.,30001.+dv,dv):
    theory.plot(pos=(v,(deltav/dv)*N*4.*pi*((m/(2.*pi*k*T))**1.5)*exp((-0.5*m*v**2)/(k*T))*v**2*dv))
observation = ghistogram(bins=arange(0.,3000.,deltav),accumulate=1,average=1,color=color.red) #step for histogram

#initialization of display,setting up for the random position distribution and random direction of atoms
scene= display(width=800,height=800,backgroung=(0.2,0.2,0))
container=box(length=2*L,height=2*L,width=2*L,opacity=0.2,color=color.yellow)
for i in range(N):
    position = vector(-L_size+2*L_size*random(),-L_size+2*L_size*random(),-L_size+2*L_size*random())
    if i == N-1:
	atom = sphere(pos=position,radius=size,color=color.yellow,make_trail=True,retain = 600)
    else:
	atom = sphere(pos = position,radius=size,color=(random(),random(),random()))
    ra,rb = pi*random(),2*pi*random()
    atom.m,atom.v = m,vector(vrms*sin(ra)*cos(rb),vrms*sin(ra)*sin(rb),vrms*cos(ra))
    atoms.append(atom)

def vcollision(a1,a2):
    v1prime = a1.v - 2*a2.m/(a1.m+a2.m)*(a1.pos-a2.pos)*dot(a1.v-a2.v,a1.pos-a2.pos)/abs(a1.pos-a2.pos)**2
    v2prime = a2.v - 2*a1.m/(a1.m+a2.m)*(a2.pos-a1.pos)*dot(a2.v-a1.v,a2.pos-a1.pos)/abs(a2.pos-a1.pos)**2
    return v1prime,v2prime
def record_pressure(a):
    global pressure
    global touch_wall
    pressure += a.m*abs(a.v)/dt
    touch_wall = False

while True:
    t+=dt
    rate(1000)

#calculate new positions for all atoms and plot histogram
    v=[]
    for i in range(N):
    #caculate new position for atoms
        atoms[i].pos += atoms[i].v*dt
	v.append(mag(atoms[i].v))
	if(i<N):
	    for j in range(i+1,N,1):
		if(abs(atoms[i].pos-atoms[j].pos)<=size*2 and dot(atoms[i].pos-atoms[j].pos,atoms[i].v-atoms[j].v)<=0):
		    (atoms[i].v,atoms[j].v) = vcollision(atoms[i],atoms[j])
	if(abs(atoms[i].x)+size>=L and dot(atoms[i].x,atoms[i].v.x)):
	    atoms[i].v.x = -atoms[i].v.x
	    touch_wall=True
	if(abs(atoms[i].y)+size>=L and dot(atoms[i].y,atoms[i].v.y)):
            atoms[i].v.y = -atoms[i].v.y
	    touch_wall=True
	if(abs(atoms[i].z)+size>=L and dot(atoms[i].z,atoms[i].v.z)):
	    atoms[i].v.z = -atoms[i].v.z
	    touch_wall=True

	if(touch_wall):
            record_pressure(atoms[i])
    observation.plot(data=v)
		




 



