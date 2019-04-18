import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

x_rotate = 0.
y_rotate = 0.
z_rotate = 0.

x_angle = 45.
y_angle = 36.264

x_origin = 0.
y_origin = 0.
z_origin = 0.

scene_x_offset = 0.
scene_y_offset = 0.
scene_x = 0.
scene_y = 0.

zoom = 45

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

def cursor_callback(window, xpos, ypos):
    global x_rotate, y_rotate
    global scene_x_offset, scene_y_offset
    global scene_x, scene_y
    if flag_left_press == True:
        x_rotate = xpos - scene_x
        y_rotate = ypos - scene_y
    elif flag_right_press == True:
        scene_x_offset = xpos - scene_x
        scene_y_offset = ypos - scene_y
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
    global x_angle, y_angle, x_rotate, y_rotate
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)     
    glEnable(GL_DEPTH_TEST)     
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )     
    glLoadIdentity() 

    #gluPerspective(zoom, 1, 1, 10)

    x_angle += x_rotate/10.
    y_angle += y_rotate/10.
    x_rotate = 0.
    y_rotate = 0.
    glRotatef(y_angle, 1, 0, 0)
    glRotatef(-x_angle, 0, 1, 0)

    #glTranslatef(-3, -3, -3)

    drawFrame()


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
