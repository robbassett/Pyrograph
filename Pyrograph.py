import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class Pyrograph():

    def __init__(self,hole=0.1,inner_frac=0.636,outer_R = 1.,xo=0.,yo=0.,nps=1000):
        self.npoints = nps
        self.R = outer_R
        self.r = self.R*inner_frac
        self.rho = self.r*hole

        dm = divmod(self.R,(1.-self.r))
        self.one_orb = 2.*np.pi*(dm[0]-1)
        if self.one_orb == 0.:
            self.one_orb = 2.*np.pi
        self.theta = 0.
        self.cx,self.cy = 0.,0.

        self.n = 0

    def one_orbit(self):

        theta = np.linspace(float(self.n)*self.one_orb,float(self.n+1)*self.one_orb,self.npoints)
        cx = (self.R-self.r)*np.cos(theta)
        cy = (self.R-self.r)*np.sin(theta)
        itheta = ((-1.)*(self.R-self.r)/self.r)*theta
        ix = self.rho*np.cos(itheta)
        iy = self.rho*np.sin(itheta)

        if self.n == 0.:
            self.x = cx+ix
            self.y = cy+iy
            self.n += 1
        else:
            self.x = np.vstack((self.x,cx+ix))
            self.y = np.vstack((self.y,cy+iy))
            self.n += 1

def testing():
    from color_tools import colorFader as cF
    
    fig = go.Figure()

    norb = 175
    c1 = 'm'
    c2 = 'darkcyan'
    test = Pyrograph()
    t2 = Pyrograph(hole=0.66,inner_frac=0.66,outer_R = .38)
    for i in range(norb):
        test.one_orbit()
        t2.one_orbit()
    for i in range(norb):
        col=cF(c1,c2,float(i)/float(norb-1))
        c22 = cF('limegreen','tab:orange',float(i)/float(norb-1))
        fig.add_trace(go.Scatter(x=test.x[i],y=test.y[i],mode='lines',line=dict(color=col)))
        fig.add_trace(go.Scatter(x=t2.x[i],y=t2.y[i],mode='lines',line=dict(color=c22)))
        
    fig.update_xaxes(range=[-.55,.55])
    fig.update_yaxes(range=[-.55,.55])
    fig.update_layout(yaxis=dict(scaleanchor='x',scaleratio=1,))
    fig.show()
                    
if __name__ == '__main__':

    testing()
