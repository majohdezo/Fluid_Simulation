"""
Based on the Jos Stam paper https://www.researchgate.net/publication/2560062_Real-Time_Fluid_Dynamics_for_Games
and the mike ash vulgarization https://mikeash.com/pyblog/fluid-simulation-for-dummies.html
https://github.com/Guilouf/python_realtime_fluidsim
"""
import numpy as np
import math
import matplotlib
import sys, argparse, os
import matplotlib.cm as cm
import Color_Scheme as color
import random

file= ""

settings = []
behaviors=["verticalCurly","horizontalCurly", "swirl", "constant"]
colorVal=3
FRAMES=200
EMITTERS=1
objectsNumber = 0
objPos = []
objSize = []

class Fluid:

    def __init__(self):
        self.rotx = 1
        self.roty = 1
        self.cntx = 1
        self.cnty = -1

        self.size = 60  # map size
        self.dt = 0.2  # time interval
        self.iter = 2  # linear equation solving iteration number

        self.diff = 0.0000  # Diffusion
        self.visc = 0.0000  # viscosity

        self.s = np.full((self.size, self.size), 0, dtype=float)        # Previous density
        self.density = np.full((self.size, self.size), 0, dtype=float)  # Current density

        # array of 2d vectors, [x, y]
        self.velo = np.full((self.size, self.size, 2), 0, dtype=float)
        self.velo0 = np.full((self.size, self.size, 2), 0, dtype=float)

    def step(self):
        self.diffuse(self.velo0, self.velo, self.visc)

        # x0, y0, x, y
        self.project(self.velo0[:, :, 0], self.velo0[:, :, 1], self.velo[:, :, 0], self.velo[:, :, 1])

        self.advect(self.velo[:, :, 0], self.velo0[:, :, 0], self.velo0)
        self.advect(self.velo[:, :, 1], self.velo0[:, :, 1], self.velo0)

        self.project(self.velo[:, :, 0], self.velo[:, :, 1], self.velo0[:, :, 0], self.velo0[:, :, 1])

        self.diffuse(self.s, self.density, self.diff)

        self.advect(self.density, self.s, self.velo)

    def lin_solve(self, x, x0, a, c):
        """Implementation of the Gauss-Seidel relaxation"""
        c_recip = 1 / c

        for iteration in range(0, self.iter):
            # Calculates the interactions with the 4 closest neighbors
            x[1:-1, 1:-1] = (x0[1:-1, 1:-1] + a * (x[2:, 1:-1] + x[:-2, 1:-1] + x[1:-1, 2:] + x[1:-1, :-2])) * c_recip

            self.set_boundaries(x, False)

    def set_boundaries(self, table, isObject):
        """
        Boundaries handling
        :return:
        """
        

        if len(table.shape) > 2:  # 3d velocity vector array
            # Simulating the bouncing effect of the velocity array
            # vertical, invert if y vector
            table[:, 0, 1] = - table[:, 0, 1]
            table[:, self.size - 1, 1] = - table[:, self.size - 1, 1]
            if(isObject):
                for a in range (0,objectsNumber):
                    x= int(objPos[a][0])
                    y=int(objPos[a][1])
                    size=int(objSize[a])
                    table[y:y+size, x:x+size]=0

            # horizontal, invert if x vector
            table[0, :, 0] = - table[0, :, 0]
            table[self.size - 1, :, 0] = - table[self.size - 1, :, 0]

        table[0, 0] = 0.5 * (table[1, 0] + table[0, 1])
        table[0, self.size - 1] = 0.5 * (table[1, self.size - 1] + table[0, self.size - 2])
        table[self.size - 1, 0] = 0.5 * (table[self.size - 2, 0] + table[self.size - 1, 1])
        table[self.size - 1, self.size - 1] = 0.5 * table[self.size - 2, self.size - 1] + \
                                              table[self.size - 1, self.size - 2]

        

    def diffuse(self, x, x0, diff):
        if diff != 0:
            a = self.dt * diff * (self.size - 2) * (self.size - 2)
            self.lin_solve(x, x0, a, 1 + 6 * a)
        else:  # equivalent to lin_solve with a = 0
            x[:, :] = x0[:, :]

    def project(self, velo_x, velo_y, p, div):
        # numpy equivalent to this in a for loop:
        # div[i, j] = -0.5 * (velo_x[i + 1, j] - velo_x[i - 1, j] + velo_y[i, j + 1] - velo_y[i, j - 1]) / self.size
        div[1:-1, 1:-1] = -0.5 * (
                velo_x[2:, 1:-1] - velo_x[:-2, 1:-1] +
                velo_y[1:-1, 2:] - velo_y[1:-1, :-2]) / self.size
        p[:, :] = 0

        self.set_boundaries(div, False)
        self.set_boundaries(p,False)
        self.lin_solve(p, div, 1, 6)

        velo_x[1:-1, 1:-1] -= 0.5 * (p[2:, 1:-1] - p[:-2, 1:-1]) * self.size
        velo_y[1:-1, 1:-1] -= 0.5 * (p[1:-1, 2:] - p[1:-1, :-2]) * self.size

        self.set_boundaries(self.velo,False)

    def advect(self, d, d0, velocity):
        dtx = self.dt * (self.size - 2)
        dty = self.dt * (self.size - 2)

        for j in range(1, self.size - 1):
            for i in range(1, self.size - 1):
                tmp1 = dtx * velocity[i, j, 0]
                tmp2 = dty * velocity[i, j, 1]
                x = i - tmp1
                y = j - tmp2

                if x < 0.5:
                    x = 0.5
                if x > (self.size - 1) - 0.5:
                    x = (self.size - 1) - 0.5
                i0 = math.floor(x)
                i1 = i0 + 1.0

                if y < 0.5:
                    y = 0.5
                if y > (self.size - 1) - 0.5:
                    y = (self.size - 1) - 0.5
                j0 = math.floor(y)
                j1 = j0 + 1.0

                s1 = x - i0
                s0 = 1.0 - s1
                t1 = y - j0
                t0 = 1.0 - t1

                i0i = int(i0)
                i1i = int(i1)
                j0i = int(j0)
                j1i = int(j1)

                try:
                    d[i, j] = s0 * (t0 * d0[i0i, j0i] + t1 * d0[i0i, j1i]) + \
                              s1 * (t0 * d0[i1i, j0i] + t1 * d0[i1i, j1i])
                except IndexError:
                    # tmp = str("inline: i0: %d, j0: %d, i1: %d, j1: %d" % (i0, j0, i1, j1))
                    # print("tmp: %s\ntmp1: %s" %(tmp, tmp1))
                    raise IndexError
        self.set_boundaries(d, False)

    def turn(self):
        self.cntx += 1
        self.cnty += 1
        if self.cntx == 3:
            self.cntx = -1
            self.rotx = 0
        elif self.cntx == 0:
            self.rotx = self.roty * -1
        if self.cnty == 3:
            self.cnty = -1
            self.roty = 0
        elif self.cnty == 0:
            self.roty = self.rotx
        return self.rotx, self.roty

def setBehavior(behavior, VelY, VelX,  factor, frame):
    VelY = -VelY
    tempVel = [VelY, VelX]
    if behavior == behaviors[0]: #verticalCurly
        tempVel = [VelY, VelX * np.cos(factor * frame)]
    if behavior == behaviors[1]: #horizontalCurly
        tempVel = [VelY * np.cos(factor * frame), VelX]
    if behavior == behaviors[2]: #Swirl
        tempVel = [VelX * np.cos(factor * frame * 0.15), VelY * np.sin(factor * frame * 0.15 )]
    if behavior == behaviors[3]: #Constant
        tempVel = [VelY, VelX]
    return tempVel

if __name__ == "__main__":
    try:
        import matplotlib.pyplot as plt
        from matplotlib import animation

        print("Enter the name of the txt file with the fluids settings: ")
        file=input()

        while not os.path.exists(file):
            print("Invalid txt file, please enter again the file name")
            file=input()

        


        f = open(file, "r")
        settings= f.readlines()
        try:
            FRAMES=int(settings[0])
        except:
            print("Please, enter an integer value for the frames")
            sys.exit()
        try:
            EMITTERS=int(settings[1])
        except:
            print("Please, enter an integer value for the number of emitters")
            sys.exit()
        try:
            objectsNumber=int(settings[2+EMITTERS])
        except:
            print("Please, enter an integer value for the number of emitters")
            sys.exit()
        try:
            colorVal=int((settings[len(settings)-1]))            
        except:
            print("Please, enter an integer value for the Color Scheme")
            sys.exit()
        
        if(colorVal>15):
            print("Please, enter a value from 1 to 15 for the Color Scheme")
            sys.exit()        
        
        
            

        inst = Fluid()

        def update_im(i, ax):
            # We add new density creators in here
              # add density into a 3*3 square
            # We add velocity vector values in here

            #Validate emitters entered
            cont=0
            for x in range(0,EMITTERS):
                index=x+2                
                emitter_settings=settings[index].split()
                behavior=emitter_settings[0]
                try:
                    int(behavior)
                except:
                    if(isinstance(behavior, str)):
                        cont+=1
            
            if(cont!=EMITTERS):
                print("Please, enter the correct settings for each emitter, you added "+ str(EMITTERS) + " emitters, but you entered the settings for "+ str(cont) + " emitters")
                sys.exit() 

            cont=0     
            objects_settings=[]
            objValueError= False
            
            for x in range(0, objectsNumber):
                index=x+3+EMITTERS
                cont+=1                
                try:                
                    objects_settings=settings[index].split()                
                    objPos.append([objects_settings[0],objects_settings[1]])
                    objSize.append(objects_settings[2])
                    try:
                        X= int(objects_settings[0])   
                        Y= int(objects_settings[1])
                        SIZE= int(objects_settings[2])
                        
                    except:
                        print("Please, enter only int values to set the objects")
                        objValueError= True
                        sys.exit()

                except:
                    if(not objValueError):
                        cont-=1
                        print("Please, enter the correct settings for each object, you added "+ str(objectsNumber) + " objects")
                        print("Values  for each emitter: X position, Y position, object size")
                    sys.exit()                
                
                if(X < 0 or X >= inst.size):
                    print("X coordinate out of grid range for Object "+ str(x+1))
                    sys.exit()
                if(Y < 0 or Y >= inst.size):
                    print("Y coordinate out of grid range for Object "+str(x+1))
                    sys.exit()

                if((X + SIZE) >= inst.size):
                    print("Object out of grid range on the X axis, please decrease the size of Object "+ str(x+1))
                    sys.exit()
                        
                if((Y + SIZE) >= inst.size):
                    print("Object out of grid range on the Y axis, please decrease the size of Object "+ str(x+1))
                    sys.exit()

            inst.set_boundaries(inst.velo, True)
            
            for x in range(0,EMITTERS):
                index=x+2
                emitter_settings=settings[index].split()
                cont=0
                for a in range (0,8):
                    try:
                        value=emitter_settings[a]
                        cont+=1
                    except:    
                        print("Please, introduce all the values required for emitter "+ str(x+1))
                        print("You only introduced "+str(cont)+ " arguments, out of 8 required:")
                        print("Values required: behavior, X position, Y position, density, X velocity, Y velocity, emitter size and factor movement")
                        sys.exit() 

                behavior=emitter_settings[0]
                if(behavior not in behaviors):
                    print("Please, introduce a valid behavior for emitter "+ str(x+1))
                    sys.exit() 
                try:
                    posX= int(emitter_settings[1])
                    posY= int(emitter_settings[2])
                    density= int(emitter_settings[3])
                    velocityX= int(emitter_settings[4])
                    velocityY= int(emitter_settings[5])
                    size= int(emitter_settings[6])
                except:
                    print("Emitter "+str(x+1)+ " values must be an integer value")
                    sys.exit()

                try:
                    fact= float(emitter_settings[7])
                except:
                    print("Emitter "+str(x+1)+ " factor value must be a number (integer or float)")
                    sys.exit()

                #Validating X and Y coordinates
                if(posX < 0 or posX >= inst.size):
                    print("X coordinate out of grid range for emitter "+ str(x+1))
                    sys.exit()
                if(posY < 0 or posY >= inst.size):
                    print("Y coordinate out of grid range for emitter "+str(x+1))
                    sys.exit()

                if((posX + size) >= inst.size):
                    print("Emitter out of grid range on the X axis, please decrease the size of emitter "+ str(x+1))
                    sys.exit()
                
                if((posY + size) >= inst.size):
                    print("Emitter out of grid range on the Y axis, please decrease the size of emitter "+ str(x+1))
                    sys.exit()
                    
                #Updating the emitters
                inst.density[posY : posY + size, posX : posX + size] += abs(density)
                inst.velo[posY , posX] = setBehavior(behavior, velocityY, velocityX,  fact, i)
            
                        
            
            inst.step()
            im.set_array(inst.density)
            ax.set_title("Fluid Simulation")
            q.set_UVC(inst.velo[:, :, 1], inst.velo[:, :, 0])
            # print(f"Density sum: {inst.density.sum()}")
            im.autoscale()

        fig, ax = plt.subplots()

              

        # plot density
        im = plt.imshow(inst.density, vmax=100, interpolation='bilinear', cmap=color.selectColor(colorVal))

        # plot vector field
        q = plt.quiver(inst.velo[:, :, 1], inst.velo[:, :, 0], scale=10, angles='xy')
        anim = animation.FuncAnimation(fig, update_im, fargs=(ax, ), interval=0, frames=FRAMES)
        print("Simulating...")

        anim.save('movie.mp4',fps=30, bitrate=1800)

        


    except ImportError:
        import imageio

        frames = 30

        flu = Fluid()

        video = np.full((frames, flu.size, flu.size), 0, dtype=float)

        for step in range(0, frames):
            flu.density[4:7, 4:7] += 100  # add density into a 3*3 square
            flu.velo[5, 5] += [1, 2]

            flu.step()
            video[step] = flu.density

        imageio.mimsave('./video.gif', video.astype('uint8'))