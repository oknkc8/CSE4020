import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gComposedM = np.identity(3,dtype='float64')
newMw = np.array([[0.9,0,0],
                  [0,1,0],
                  [0,0,1]])
newMe = np.array([[1.1,0,0],
                  [0,1,0],
                  [0,0,1]])

angleC = np.cos(10*np.pi/180)
angleS = np.sin(10*np.pi/180)
newMs = np.array([[angleC,-angleS,0],
                  [angleS,angleC,0],
                  [0,0,1]])
angleCC = np.cos(-10*np.pi/180)
angleSC = np.sin(-10*np.pi/180)
newMd = np.array([[angleCC,-angleSC,0],
                  [angleSC,angleCC,0],
                  [0,0,1]])

newMx = np.array([[1,-0.1,0],
                  [0,1,0],
                  [0,0,1]])
newMc = np.array([[1,0.1,0],
                  [0,1,0],
                  [0,0,1]])

newMr = np.array([[1,0.,0],
                  [0,-1,0],
                  [0,0,1]])


def render(T):
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
        # draw triangle
        glBegin(GL_TRIANGLES)
        glColor3ub(255, 255, 255)
        glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
        glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
        glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
        glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if key == glfw.KEY_W and action == glfw.PRESS:
        gComposedM = newMw @ gComposedM
    elif key == glfw.KEY_E and action == glfw.PRESS:
        gComposedM = newMe @ gComposedM
    elif key == glfw.KEY_S and action == glfw.PRESS:
        gComposedM = newMs @ gComposedM
    elif key == glfw.KEY_D and action == glfw.PRESS:
        gComposedM = newMd @ gComposedM
    elif key == glfw.KEY_X and action == glfw.PRESS:
        gComposedM = newMx @ gComposedM
    elif key == glfw.KEY_C and action == glfw.PRESS:
        gComposedM = newMc @ gComposedM
    elif key == glfw.KEY_R and action == glfw.PRESS:
        gComposedM = newMr @ gComposedM
    elif key == glfw.KEY_1 and action == glfw.PRESS:
        gComposedM = np.identity(3,dtype='float64')    
    return


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2017029807-3-2", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    # set the number of screen refresh to wait before calling glfw.swap_buffer().
    # if your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # get the current time, in seconds
        t = glfw.get_time()

        render(gComposedM)

        glfw.swap_buffers(window)
    glfw.terminate()
    
if __name__ == "__main__":
    main()

