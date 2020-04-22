import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

T = np.array([[1, 0, 0.6],
              [0, 1, 0],
              [0, 0, 1]])

th = np.radians(30)
R = np.array([[np.cos(th), -np.sin(th), 0],
              [np.sin(th), np.cos(th), 0],
              [0, 0, 1]])

M = T @ R

def drawFrame():
        glBegin(GL_LINES)
        glColor3ub(255, 0, 0)
        glVertex2fv(np.array([0.,0.]))
        glVertex2fv(np.array([1.,0.]))
        glColor3ub(0, 255, 0)
        glVertex2fv(np.array([0.,0.]))
        glVertex2fv(np.array([0.,1.]))
        glEnd()
 
def drawTriangle():
        glBegin(GL_TRIANGLES)
        glColor3ub(255, 255, 255)
        glVertex2fv(np.array([0.,.5]))
        glVertex2fv(np.array([0.,0.]))
        glVertex2fv(np.array([.5,0.]))
        glEnd()


def drawFrameblue():
        glBegin(GL_LINES)
        glColor3ub(255, 0, 0)
        #glMultMatrixf(np.transpose(R @ T))
        glVertex3fv(M @ np.array([0.,0.,1.]))
        glVertex3fv(M @ np.array([1.,0.,1.]))
        glColor3ub(0, 255, 0)
        glVertex3fv(M @ np.array([0.,0.,1.]))
        glVertex3fv(M @ np.array([0.,1.,1.]))
        glEnd()
 
def drawTriangleblue():
        glBegin(GL_TRIANGLES)
        glColor3ub(0, 0, 255)
        #glMultMatrixf(np.transpose(R @ T))
        glVertex3fv(M @ np.array([0.,.5,1.]))
        glVertex3fv(M @ np.array([0.,0.,1.]))
        glVertex3fv(M @ np.array([.5,0.,1.]))
        glEnd()
 

def main():
        if not glfw.init():
                return
        window = glfw.create_window(480,480,"2017029807-5-2", None,None)
        if not window:
                glfw.terminate()
                return
        glfw.make_context_current(window)

        glfw.swap_interval(1)
        while not glfw.window_should_close(window):
                glfw.poll_events()
                drawFrame()
                drawTriangle()

                drawFrameblue()
                drawTriangleblue()
                glfw.swap_buffers(window)    
        glfw.terminate()
    
if __name__ == "__main__":
    main()
