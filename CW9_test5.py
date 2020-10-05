#Yan-Ru b03b01001
#Pratice 5
from visual import *

#variable
#bool
bool_p=False

A,N,omega = 0.10,50,2*pi/1.0 #original
size,m,k,d = 0.06,0.1,10.0,0.4
Unit_k,n = 2*pi/(N*d),10
wave_vector = Unit_k*n
angular_freq=0.0
phase = wave_vector*arange(N)*d
scene = display(title='spring wave',width = 1200,height = 300,background = (0.5,0.5,0.0),range = N*d/2+0.5,center=((N-1)*d/2,0,0))
##ball = [sphere(radius = size, color = color.red, pos = vector(i*d,0,0), v=vector(0,0,0))for i in range(N)]
##spring = [helix(radius = size/2.0,thickness = d/15.0,pos = vector(i*d,0,0),axis = vector(d,0,0))for i in range(N-1)]

#new
c = curve(display = scene)
ball_pos,ball_orig,ball_v,spring_len = arange(N)*d+A*sin(phase),arange(N)*d,zeros(N),ones(N)*d

t,dt,count = 0,0.0001,0
while True:
    rate(10000)
    t=t+dt
    ##ball_pos[0] = A*sin(omega*t)
    spring_len[0:-1] = ball_pos[1:]-ball_pos[0:-1]
    spring_len[-1] = ball_pos[0]-ball_pos[-1]+N*d
    ball_v[1:] += k*((spring_len[1:]-ones(N-1)*d)-(spring_len[0:-1]-ones(N-1)*d))/m*dt
	
	#for periodic waves
    ball_v[0] += k*((spring_len[0]-d)-(spring_len[-1]-d))/m*dt
	
    ball_pos += ball_v*dt

    #new
    ##for i in range(N): ball[i].pos.x = ball_pos[i] #3 
    ##for i in range(N-1): #3 
    ##	spring[i].pos = ball[i].pos #3 
    ##	spring[i].axis = ball[i+1].pos - ball[i].pos #3


    ball_dis = ball_pos - ball_orig
    c.x = ball_orig
    c.y = ball_dis*4.0+1.0
	
    if(bool_p==True):
        if(ball_v[1]>=0):
            bool_p=False
            
    elif(bool_p==False):
        if(ball_v[1]<=0):
            count +=1
            bool_p=True
            if(count>1):
                print 'period=',t
                angular_freq=2*pi/t
                print 'angular frequence=',angular_freq
                angular_freq=0.0
            t=0
            
