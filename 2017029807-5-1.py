import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
def render(M):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        # draw cooridnate
        glBegin(GL_LINES)
        glColor3ub(255, 0, 0)
        glVertex2fv(np.array([0.,0.]))
        glVertex2fv(np.array([1.,0.]))
        glColor3ub(0, 255, 0)
        glVertex2fv(np.array([0.,0.]))
        glVertex2fv(np.array([0.,1.]))
        glEnd()
        glColor3ub(255, 255, 255)
        # draw point p
        glBegin(GL_POINTS)
        glVertex3fv(M @ np.array([0.5,0,1]))
        glEnd()
        # draw vector v
        glBegin(GL_LINES)
        glVertex3fv(M @ np.array([0,0,0]))
        glVertex3fv(M @ np.array([0.5,0,0]))
        glEnd()
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2017029807-5-1", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    # set the number of screen refresh to wait before calling glfw.swap_buffer().
    # if your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        # get the current time, in seconds
        t = glfw.get_time()
        R = np.array([[np.cos(t), -np.sin(t), 0],
                      [np.sin(t), np.cos(t), 0],
                      [0, 0, 1]])
        T = np.array([[1, 0, 0.5],
                      [0, 1, 0],
                      [0, 0, 1]])
        M = R @ T
        render(M)
        glfw.swap_buffers(window)
    glfw.terminate()
    
if __name__ == "__main__":
    main()