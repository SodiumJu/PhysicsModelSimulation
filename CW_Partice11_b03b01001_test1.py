from visual import*
from visual.graph import*
from diatomic import*

N=4
initial_v=100.0
count=0
v_P=0
v_K=0
com_K=0

#scene
scene_g = gdisplay(y=400,width=800,height=300,xtitle='t',ytitle='ratio of total energy',background=(0,0,0))
scene = display(width=800, height=800,background=(0.2,0.2,0), fov = 0.05)
container=box(length=N*1.90*d,height=size*2,width=size*2,opacity=0.3,color=color.green)

#curve
gv_P=gcurve(color=color.red,gdisplay=scene_g)
gv_K=gcurve(color=color.cyan,gdisplay=scene_g)
gcom_K=gcurve(color=color.yellow,gdisplay=scene_g)

COs=[]

for i in range(N):
    x = (i-N/2.0)*(1.90)*d+0.45*d
    CO = CO_molecule(pos=vector(x,0,0),axis=vector(1.0*d,0,0))
    CO.C.v = vector(initial_v,0,0)
    CO.O.v = vector(initial_v,0,0)
    COs.append(CO)

dt = 2.0E-16
t = 0

while True:
    rate(10000)
    t+=dt
    count+=1
    #for each CO in COs caculate the time lapsed result after dt
    for i in range(N):
        COs[i].time_lapse(dt)
    #check and handle the collision of the first molecule to the left wall and the last to the right wall
    for i in range(N):
        for j in range(N):
            if (abs(COs[i].O.pos-COs[j].C.pos)<=size*2 and i!=j and dot(COs[i].O.pos-COs[j].C.pos,COs[i].O.v-COs[j].C.v)<=0):
                COs[i].O.v,COs[j].C.v=collision(COs[i].O,COs[j].C)
                
        
    #check and handle the collision of the first molecule to the left wall and the last to the right wall
    #left
    if (abs(COs[0].O.pos.x-size)>=container.length/2 and dot(COs[0].O.pos.x,COs[0].O.v.x)>=0):
        COs[0].O.v.x = -COs[0].O.v.x
    #right
    if (abs(COs[N-1].C.pos.x+size)>=container.length/2 and dot(COs[N-1].C.pos.x,COs[N-1].C.v.x)>=0):
        COs[N-1].C.v.x = -COs[N-1].C.v.x
    #calculate the com_K, v_K, v_P, and total_energy, averaged since the beginning of the simulation
    for i in COs:
        v_P+=i.v_P()/N
        v_K+=i.v_K()/N
        com_K+=i.com_K()/N
    #print the averaged com_K/total_energy, v_K/total_energy, v_P/total_energy every 1000dt
    if (int(count%(1000))==0):
        Total_E=v_P/count+v_K/count+com_K/count
        gv_P.plot(pos=(t,v_P/count/Total_E))
        gv_K.plot(pos=(t,v_K/count/Total_E))
        gcom_K.plot(pos=(t,com_K/count/Total_E))
        """
        print 'v_K ratio = ',v_K/count/Total_E
        print 'v_P ratio = ',v_P/count/Total_E
        print 'com_K ratio = ',com_K/count/Total_E
        """
        v_P,v_K,com_K,Total_E=0,0,0,0
        
    

