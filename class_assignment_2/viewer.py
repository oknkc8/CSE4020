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

zoom = 3.

flag_left_press = False
flag_right_press = False

M = np.identity(4)

file_path = None

vertex_arr = np.array([[]], 'float32')
index_arr = np.array([[]],'int32')
normal_arr = np.array([[]],'float32')
face_arr = np.array([[[]]])

toggle_mode = GL_LINE
shading_mode = 1
count_v_f = []

gVertexArraySeparate = None
gVertexArraySeparate_smooth = None

count_3_v = 0
count_4_v = 0
count_m4_v = 0

def init():
    global toggle_mode, shading_mode, count_v_f
    global gVertexArraySeparate, gVertexArraySeparate_smooth
    global count_3_v, count_4_v, count_m4_v
    toggle_mode = GL_LINE
    shading_mode = 1
    count_v_f = []

    gVertexArraySeparate = None
    gVertexArraySeparate_smooth = None

    count_3_v = 0
    count_4_v = 0
    count_m4_v = 0

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

        angleC = np.cos(y_rotate*np.pi/180)
        angleS = np.sin(y_rotate*np.pi/180)
        rotate_y_M = np.array([[1, 0, 0, 0],
                  [0, angleC, -angleS, 0],
                  [0, angleS, angleC, 0],
                  [0, 0, 0, 1]])
        
        M = rotate_y_M @ M
        M = rotate_x_M @ M

    elif flag_right_press == True:
        scene_x_pos = xpos - scene_x
        scene_y_pos = ypos - scene_y
        translate_M = np.array([[1, 0, 0, scene_x_pos/100],
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

def key_callback(window, key, scancode, action, mods):
    global toggle_mode, shading_mode
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_Z:
            if toggle_mode == GL_LINE:
                toggle_mode = GL_FILL
            else:
                toggle_mode = GL_LINE
        elif key==glfw.KEY_S:
            shading_mode *= -1


def size_callback(window, width, height):
    global g_Width, g_Height
    g_Width = width
    g_Height = height
    glViewport(0, 0, g_Width, g_Height)

def drop_callback(window, paths):
    global file_path
    file_path = paths[0]
    parse_obj()

def parse_obj():
    init()
    global file_path, count_3_v, count_4_v, count_m4_v
    global vertex_arr, normal_arr, face_arr, index_arr
    global gVertexArraySeparate, gVertexArraySeparate_smooth
    f = open(file_path, 'r')
    lines = f.readlines()

    vertex_arr = np.array([[0,0,0]], 'float32')
    index_arr = np.array([[0,0,0]],'int32')
    normal_arr = np.array([[0,0,0]],'float32')
    face_arr = np.array([[[0,0,0],[0,0,0],[0,0,0]]])

    sum_x = sum_y = sum_z = 0.
    for line in lines:
        # comment
        if line.startswith('#'): 
            continue
        
        # split space (reduce null)
        val = line.split(' ')
        val = [x for x in val if x]

        if val[0] == 'v':
            tmp_v = np.array([[float(val[1]), float(val[2]), float(val[3])]], 'float32')
            sum_x+=float(val[1])
            sum_y+=float(val[2])
            sum_z+=float(val[3])
            vertex_arr = np.append(vertex_arr, tmp_v, axis=0)
            count_v_f.append([])
        elif val[0] == 'vn':
            tmp_vn = np.array([[float(val[1]), float(val[2]), float(val[3])]], 'float32')
            normal_arr = np.append(normal_arr, tmp_vn, axis=0)
        elif val[0] == 'f':
            if val[len(val)-1] == '\n':
                val = np.delete(val, len(val)-1, 0)

            if len(val) == 4:
                count_3_v += 1
            elif len(val) == 5:
                count_4_v += 1
            elif len(val) > 5:
                count_m4_v += 1

            v1 = val[1].split('/')
            while len(v1) < 3:
                v1.append(-1)
            for i in range(3):
                if v1[i] == '':
                    v1[i] = -1
            v2 = val[2].split('/')
            while len(v2) < 3:
                v2.append(-1)
            for i in range(3):
                if v2[i] == '':
                    v2[i] = -1
            v3 = val[3].split('/')
            while len(v3) < 3:
                v3.append(-1)
            for i in range(3):
                if v3[i] == '':
                    v3[i] = -1

            tmp_face = np.array([[[int(v1[0])-1, int(v1[1]), int(v1[2])], [int(v2[0])-1, int(v2[1]), int(v2[2])], [int(v3[0])-1, int(v3[1]), int(v3[2])]]])
            face_arr = np.append(face_arr, tmp_face, axis=0)
            tmp_index = np.array([[int(v1[0])-1, int(v2[0])-1, int(v3[0])-1]])
            count_v_f[int(v1[0])-1].append(len(index_arr)-1)
            count_v_f[int(v2[0])-1].append(len(index_arr)-1)
            count_v_f[int(v3[0])-1].append(len(index_arr)-1)
            index_arr = np.append(index_arr, tmp_index, axis=0)
        else:
            continue

    vertex_arr = np.delete(vertex_arr, 0, 0)
    # move to origin
    '''
    sum_x /= len(vertex_arr)
    sum_y /= len(vertex_arr)
    sum_z /= len(vertex_arr)
    for i in range(len(vertex_arr)):
        vertex_arr[i][0] -= sum_x
        vertex_arr[i][1] -= sum_y
        vertex_arr[i][2] -= sum_z
    '''

    normal_arr = np.delete(normal_arr, 0, 0)
    face_arr = np.delete(face_arr, 0, 0)
    index_arr = np.delete(index_arr, 0, 0)

    gVertexArraySeparate, gVertexArraySeparate_smooth = createVertexArraySeparate()

    # console output
    print()
    print("--------------------------------------------------------------------------")
    print("File Name : ", file_path)
    print("Total Number of Faces : ", len(face_arr))
    print("Number of faces with 3 vertices : ", count_3_v)
    print("Number of faces with 4 vertices : ", count_4_v)
    print("Number of faces with more than 4 vertices : ", count_m4_v)
    print("--------------------------------------------------------------------------")
    print()

def createVertexArraySeparate():
    global shading_mode
    varr = np.array([[0,0,0]], 'float32')
    face_nv_arr = np.array([[0,0,0]], 'float32')
    vertex_nv_arr = np.array([[0,0,0]], 'float32')
    for i in range(len(face_arr)):
        # no normal vector in face array

        # calculate normal vector
        a = vertex_arr[face_arr[i][1][0]] - vertex_arr[face_arr[i][0][0]]
        b = vertex_arr[face_arr[i][2][0]] - vertex_arr[face_arr[i][0][0]]
        n0 = n1 = n2 = np.cross(a,b)
        tmp = np.array([n0], 'float32')
        face_nv_arr = np.append(face_nv_arr, tmp, axis = 0)
        if face_arr[i][0][2] != -1.0:
            # get normal vector from obj file
            n0 = normal_arr[face_arr[i][0][2]-1]
            n1 = normal_arr[face_arr[i][1][2]-1]
            n2 = normal_arr[face_arr[i][2][2]-1]

        n0 = np.array([n0], 'float32')
        n1 = np.array([n1], 'float32')
        n2 = np.array([n2], 'float32')
        
        varr = np.append(varr, n0, axis = 0)
        varr = np.append(varr, np.array([vertex_arr[face_arr[i][0][0]]], 'float32'), axis = 0)
        varr = np.append(varr, n1, axis = 0)
        varr = np.append(varr, np.array([vertex_arr[face_arr[i][1][0]]], 'float32'), axis = 0)
        varr = np.append(varr, n2, axis = 0)
        varr = np.append(varr, np.array([vertex_arr[face_arr[i][2][0]]], 'float32'), axis = 0)

    face_nv_arr = np.delete(face_nv_arr, 0, 0)
    varr = np.delete(varr, 0, 0)

    varr2 = np.array(varr)
    # forced smooth shading
    # calculate normal vector for vertex
    for i in range(len(vertex_arr)):
        sum = np.array([0,0,0], 'float32')
        for idx in count_v_f[i]:
            sum += face_nv_arr[idx]
        sum /= len(count_v_f[i])
        sum = np.array([sum])
        vertex_nv_arr = np.append(vertex_nv_arr, sum, axis = 0)

    vertex_nv_arr = np.delete(vertex_nv_arr, 0, 0)
    for i in range(len(face_arr)):
        varr2[i*6 + 0] = vertex_nv_arr[face_arr[i][0][0]]
        varr2[i*6 + 2] = vertex_nv_arr[face_arr[i][1][0]]
        varr2[i*6 + 4] = vertex_nv_arr[face_arr[i][2][0]]

    return varr, varr2

def render():
    global M
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)     
    glEnable(GL_DEPTH_TEST)     
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )     
    glLoadIdentity() 
    gluLookAt(0, 0, g_fViewDistance, 0, 0, 0, 0., .1, 0)
	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, float(g_Width)/float(g_Height), g_nearPlane, g_farPlane)
    glTranslatef(0., 0., -500)
    glMatrixMode(GL_MODELVIEW)

    glMultMatrixf(np.transpose(M))

    drawFrame()
    drawXZ()

    if file_path == None:
        return

    glColor3ub(255, 255, 255)
    # draw obj model

    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glEnable(GL_RESCALE_NORMAL)  # try to uncomment: lighting will be incorrect if you scale the object
    
    # light intensity for each color channel
    lightColor = (1.,0.,0.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    lightPos = (10.,10.,10.,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    
    lightColor = (0.,0.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    lightPos = (-5.,-6.,-3.,0.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    
    # material reflectance for each color channel
    objectColor = (0.5,0.5,0.5,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPolygonMode(GL_FRONT, toggle_mode)
    global vertex_arr, index_arr
    global gVertexArraySeparate, gVertexArraySeparate_smooth
    
    if shading_mode == 1:
        varr = gVertexArraySeparate
    else:
        varr = gVertexArraySeparate_smooth
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

    glDisable(GL_LIGHTING)
    
def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "2017029807-obj-viewer", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_framebuffer_size_callback(window, size_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.set_key_callback(window, key_callback)

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
