from visual import*
size,m_o,m_c,k_bond = 310E-12,16.0/6E23,12.0/6E23,1860.0
d=2.5*size
dt = 1E-16

def collision(a1,a2):
    v1prime = a1.v - 2*(a2.m/(a1.m+a2.m))*(a1.pos-a2.pos)*dot(a1.v-a2.v,a1.pos-a2.pos)/abs(a1.pos-a2.pos)**2
    v2prime = a2.v - 2*(a1.m/(a1.m+a2.m))*(a2.pos-a1.pos)*dot(a2.v-a1.v,a2.pos-a1.pos)/abs(a2.pos-a1.pos)**2
    return v1prime,v2prime

class CO_molecule:
    def __init__(self,pos,axis):
        self.O = sphere(pos=pos,radius=size)
        self.C = sphere(pos=pos+axis,radius=size,color=color.black)
        self.bond = cylinder(pos=pos,axis=axis,radius=size/2.0)
        self.O.m,self.C.m=m_o,m_c
        self.bond.k=k_bond
    #default
        
    def bond_force_on_O(self):
        return self.bond.k*(mag(self.bond.axis)-d)*norm(self.bond.axis)
    # return bond force acted on the O atom
    
    def time_lapse(self,dt):
        self.bond.pos = self.O.pos
        self.bond.axis = self.C.pos-self.O.pos
        self.O.a,self.C.a = self.bond_force_on_O()/self.O.m,-self.bond_force_on_O()/self.C.m
        for i in [self.O,self.C]:
            i.v+=i.a*dt
            i.pos+=i.v*dt

    # by bond's force, calculate a, v and pos of C and O, and bond's pos and axis after dt    
           
    def com(self):
        return (self.O.pos*self.O.m+self.C.pos*self.C.m)/(self.O.m+self.C.m) 
    # return position of center of mass
    
    def com_v(self):
        return (self.O.v*self.O.m+self.C.v*self.C.m)/(self.O.m+self.C.m)
    # return velocity of center of mass
    
    def v_P(self):
        return 0.5*self.bond.k*(abs(self.bond.axis)-d)**2
    # return potential energy of the bond of the vibration motion
    
    def v_K(self):
        O_v=self.O.v-self.com_v()
        C_v=self.C.v-self.com_v()
        return 0.5*(self.O.m)*mag2(O_v) + 0.5*(self.C.m)*mag2(C_v)
    # return kinetic energy of the vibration motion

    def com_K(self):
        return 0.5*(self.O.m+self.C.m)*self.com_v().mag**2
    #return kinetic energy of the translational motion of the center of mass

if __name__=='__main__':
    a = CO_molecule(pos=vector(0,0,0),axis=(2.6*size,0,0))
    a.O.v,a.C.v=vector(1.0,0,0),vector(2.0,0,0)
    a.time_lapse(dt)
    print a.bond_force_on_O().x,a.com(),a.com_v(),a.v_P(),a.v_K(),a.com_K()

    
