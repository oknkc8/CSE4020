import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

y_rotate = 0
x_rotate = 0
z_rotate = 0.

scene_x_pos = 0.
scene_y_pos = 0.
scene_x = 0.
scene_y = 0.

g_fViewDistance = 9.
g_Width = 600
g_Height = 600

g_nearPlane = 5
g_farPlane = 1000.

zoom = 50.

flag_left_press = False
flag_right_press = False

M = np.identity(4)
#rotate_M = np.identity(4)
#translate_M = np.identity(4)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def drawXZ():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    for i in range(-5,6):
        glVertex3fv(np.array([i,0,5]))
        glVertex3fv(np.array([i,0,-5]))
        glVertex3fv(np.array([5,0,i]))
        glVertex3fv(np.array([-5,0,i]))
    glEnd()

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

def drawRunner():
    t = glfw.get_time()
    glColor3ub(255, 255, 255)
    # draw body
    glPushMatrix()
    glTranslatef(0,np.sin(7*t)*0.1+3,0)
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

def cursor_callback(window, xpos, ypos):
    global x_rotate, y_rotate
    global scene_x_pos, scene_y_pos
    global scene_x, scene_y
    global M
    if flag_left_press == True:
        x_rotate = xpos - scene_x
        y_rotate = ypos - scene_y
        
        angleC = np.cos(x_rotate*np.pi/180)
        angleS = np.sin(x_rotate*np.pi/180)
        rotate_x_M = np.array([[angleC, 0, angleS, 0],
                                [0, 1, 0, 0],
                                [-angleS, 0, angleC, 0],
                                [0, 0, 0, 1]])

        angleC = np.cos(-y_rotate*np.pi/180)
        angleS = np.sin(-y_rotate*np.pi/180)
        rotate_y_M = np.array([[1, 0, 0, 0],
                  [0, angleC, -angleS, 0],
                  [0, angleS, angleC, 0],
                  [0, 0, 0, 1]])
        
        M = rotate_y_M @ M
        M = rotate_x_M @ M

    elif flag_right_press == True:
        scene_x_pos = xpos - scene_x
        scene_y_pos = ypos - scene_y
        translate_M = np.array([[1, 0, 0, -scene_x_pos/100],
                                [0, 1, 0, -scene_y_pos/100],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
        M = translate_M @ M
    
    scene_x = xpos
    scene_y = ypos

def button_callback(window, button, action, mod):
    global flag_left_press, flag_right_press
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            flag_left_press = True
        elif action == glfw.RELEASE:
            flag_left_press = False
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            flag_right_press = True
        elif action == glfw.RELEASE:
            flag_right_press = False
            

def scroll_callback(window, xoffset, yoffset):
    global zoom
    zoom -= yoffset

def render():
    global M
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)     
    glEnable(GL_DEPTH_TEST)     
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )     
    glLoadIdentity() 
    gluLookAt(0, 0, -g_fViewDistance, 0, 0, 0, 0., .1, 0)
	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, float(g_Width)/float(g_Height), g_nearPlane, g_farPlane)
    glTranslatef(0., 0., -30)
    glMatrixMode(GL_MODELVIEW)

    glMultMatrixf(np.transpose(M))

    drawFrame()
    drawXZ()

    drawRunner()

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
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
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
