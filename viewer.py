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

g_nearPlane = 1.
g_farPlane = 1000.

zoom = 10.

flag_left_press = False
flag_right_press = False

M = None

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

def cursor_callback(window, xpos, ypos):
    global x_rotate, y_rotate
    global scene_x_pos, scene_y_pos
    global scene_x, scene_y
    if flag_left_press == True:
        x_rotate += xpos - scene_x
        y_rotate += ypos - scene_y
    elif flag_right_press == True:
        scene_x_pos -= xpos - scene_x
        scene_y_pos -= ypos - scene_y
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
    global x_rotate, y_rotate
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)     
    glEnable(GL_DEPTH_TEST)     
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )     
    glLoadIdentity() 
    gluLookAt(0, 0, -g_fViewDistance, 0, 0, 0, 0., .1, 0)
	# Set perspective (also zoom)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, float(g_Width)/float(g_Height), g_nearPlane, g_farPlane)
    glMatrixMode(GL_MODELVIEW)

    #glLoadIdentity()
    #glPushMatrix()
    glTranslatef(scene_x_pos/500., 0., 0.)
    glTranslatef(0., scene_y_pos/500., 0.)

    #glPopMatrix()
    glRotatef(y_rotate/2., 1., 0., 0.)
    glRotatef(x_rotate/2., 0., 1., 0.)
    

    drawFrame()
    drawXZ()
    #drawCube()

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
