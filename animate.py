import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# draw a sphere of radius 1, centered at the origin.
# numLats: number of latitude segments
# numLongs: number of longitude segments
def drawSphere(numLats=12, numLongs=12, size=1, x_ratio=1, y_ratio=1, z_ratio=1):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0) * size
        zr0 = np.cos(lat0) * size

        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1) * size
        zr1 = np.cos(lat1) * size

        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)

        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng) * x_ratio
            y = np.sin(lng) * y_ratio
            glVertex3f(x * zr0, y * zr0, z0 * z_ratio)
            glVertex3f(x * zr1, y * zr1, z1 * z_ratio)
        
        glEnd()

def render():
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE ) 
    glLoadIdentity() 
    gluLookAt(3, 3, 4, 0, 0, 0, 0., .1, 0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 1., 1., 1000.)
    glMatrixMode(GL_MODELVIEW)

    t = glfw.get_time()
    glColor3ub(255, 255, 255)
    # draw body
    glPushMatrix()
    glTranslatef(0,np.sin(7*t)*0.1,0)
    drawSphere(30,30,2,.3,.8,.3)
    
    # draw head
    glPushMatrix()
    glTranslatef(0,2,0)
    drawSphere(30,30,.5, 1, 1, 1)
    glPopMatrix()

    # draw arm right-1
    glPushMatrix()
    glTranslatef(0, 1, .63)
    glRotatef(-30,1,0,0)
    glRotate(-np.sin(7*t)*50,0,0,1)
    glTranslate(0,-.6,0)
    drawSphere(10,10,.6,.25,1.3,.25)

    #draw arm right-2
    glPushMatrix()
    glTranslatef(0,-.6,0)
    glRotate(30,1,0,0)
    glRotate(-np.sin(7*t)*45+45,0,0,1)
    glTranslate(0,-.4,0)
    drawSphere(10,10,.4,.25,1.3,.25)
    glPopMatrix()

    glPopMatrix()

    # draw arm left-1
    glPushMatrix()
    glTranslatef(0, 1, -.63)
    glRotatef(30,1,0,0)
    glRotate(np.sin(7*t)*50,0,0,1)
    glTranslate(0,-.6,0)
    drawSphere(10,10,.6,.25,1.3,.25)

    #draw arm left-2
    glPushMatrix()
    glTranslatef(0,-.6,0)
    glRotate(-30,1,0,0)
    glRotate(np.sin(7*t)*45+45,0,0,1)
    glTranslate(0,-.4,0)
    drawSphere(10,10,.4,.25,1.3,.25)
    glPopMatrix()

    glPopMatrix()

    # draw leg right-1
    glPushMatrix()
    glTranslatef(0, -1, .43)
    glRotate(np.sin(7*t)*45,0,0,1)
    glTranslate(0,-.6,0)
    drawSphere(10,10,.7,.25,1,.25)

    # draw leg right-2
    glPushMatrix()
    glTranslatef(0,-.7,0)
    glRotate(np.sin(7*t)*45-45,0,0,1)
    glTranslate(0,-.4,0)
    drawSphere(10,10,.4,.4,1.3,.4)
    glPopMatrix()

    glPopMatrix()

    # draw leg left-1
    glPushMatrix()
    glTranslatef(0, -1, -.43)
    glRotate(-np.sin(7*t)*45,0,0,1)
    glTranslate(0,-.6,0)
    drawSphere(10,10,.7,.25,1,.25)

    # draw leg left-2
    glPushMatrix()
    glTranslatef(0,-.7,0)
    glRotate(-np.sin(7*t)*45-45,0,0,1)
    glTranslate(0,-.4,0)
    drawSphere(10,10,.4,.4,1.3,.4)
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()

def size_callback(window, width, height):
    global g_Width, g_Height
    g_Width = width
    g_Height = height
    glViewport(0, 0, g_Width, g_Height)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "2017029807-simple-viewer", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, size_callback)

    # set the number of screen refresh to wait before calling glfw.swap_buffer().
    # if your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()
    
if __name__ == "__main__":
    main()
