#!/usr/bin/env python

# Purdue CS530 - Introduction to Scientific Visualization
# Spring 2020

# Simple example showing how to use PyQt5 to manipulate
# a visualization

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QSlider, QGridLayout, QLabel,QComboBox, QPushButton, QTextEdit
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import argparse
import sys
import numpy as np
from vtk.util import numpy_support

####################################################

####################################################

frame_counter = 0

veg_rgb = [
            [194, 178, 128],
            [168, 166, 92],
            [76, 187, 23], # kelly
            # [80, 200, 120], # emerald
            # [11, 102, 35] 
            [129, 134, 74]
        ]     

temp_rgb = [
            [0,255,249],
            [0,162,197],
            [1,98,156],
            [0,41,111],
            [1,0,41],
            [217,1,122],
            [237,23,23],
            [242,77,17],
            [246,131,12],
            [251,184,6],
            [255,238,0]
            ] 

rgb255 = [
            [68, 1, 84],
            [71, 16, 99],
            [72, 31, 112],
            [71, 45, 123],
            [68, 57, 131],
            [64, 70, 136],
            [59, 82, 139],
            [54, 93, 141],
            [49, 104, 142],
            [44, 114, 142],
            [40, 124, 142],
            [36, 134, 142],
            [33, 145, 140],
            [31, 154, 138],
            [32, 164, 134],
            [40, 174, 128],
            [53, 183, 121],
            [72, 193, 110],
            [94, 201, 98],
            [117, 208, 84],
            [144, 215, 67],
            [173, 220, 48],
            [200, 224, 32],
            [229, 228, 25],
            [253, 231, 37],
        ]

####################################################


####################################################

def convert(arr, r):
    
    a = []
    for temp in arr:
        # print(temp)
        x = temp[0]+180 # long
        y = temp[1] # lat
        x_new = r * np.cos(x * np.pi/180) * np.cos(y * np.pi/180)
        y_new = r * np.sin(x * np.pi/180) * np.cos(y * np.pi/180)
        z_new = r * np.sin(y * np.pi/180)
        temp2 = np.array([x_new, y_new, z_new], dtype=np.float32)
        a.append(temp2)
       
    aa = np.asarray(a)
    aaa = numpy_support.numpy_to_vtk(aa) 

    return aaa


def make_sphere(resolution_theta, resolution_phi, edge_radius):
    # create and visualize sphere
    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetRadius(1.0)
    sphere_source.SetCenter(0.0, 0.0, 0.0)
    sphere_source.SetThetaResolution(resolution_theta)
    sphere_source.SetPhiResolution(resolution_phi)

    # extract and visualize the edges
    edge_extractor = vtk.vtkExtractEdges()
    edge_extractor.SetInputConnection(sphere_source.GetOutputPort())
    edge_tubes = vtk.vtkTubeFilter()
    edge_tubes.SetRadius(edge_radius)
    edge_tubes.SetInputConnection(edge_extractor.GetOutputPort())
    return [sphere_source, edge_tubes]


def make_vegetation_table():
    rgb = []
    for i in range(len(veg_rgb)):
        rgb.append([veg_rgb[i][0] / 255, veg_rgb[i][1] / 255, veg_rgb[i][2] / 255])

    ctf =  vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToRGB() 
    ctf.AddRGBPoint(-0.1,rgb[0][0],rgb[0][1],rgb[0][2])
    ctf.AddRGBPoint(0.45,rgb[1][0],rgb[1][1],rgb[1][2])
    ctf.AddRGBPoint(0.6,rgb[2][0],rgb[2][1],rgb[2][2])
    # ctf.AddRGBPoint(0.75,rgb[3][0],rgb[3][1],rgb[3][2])
    ctf.AddRGBPoint(0.9,rgb[3][0],rgb[3][1],rgb[3][2])
    return ctf


def make_temp_table():
    rgb = []
    for i in range(len(temp_rgb)):
        rgb.append([temp_rgb[i][0] / 255, temp_rgb[i][1] / 255, temp_rgb[i][2] / 255])

    ctf =  vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToRGB() 
    ctf.AddRGBPoint(-25,rgb[0][0],rgb[0][1],rgb[0][2])
    ctf.AddRGBPoint(-15,rgb[1][0],rgb[1][1],rgb[1][2])
    ctf.AddRGBPoint(-10,rgb[2][0],rgb[2][1],rgb[2][2])
    ctf.AddRGBPoint(-5,rgb[3][0],rgb[3][1],rgb[3][2])
    ctf.AddRGBPoint(0,rgb[4][0],rgb[4][1],rgb[4][2])
    ctf.AddRGBPoint(5,rgb[5][0],rgb[5][1],rgb[5][2])
    ctf.AddRGBPoint(10,rgb[6][0],rgb[6][1],rgb[6][2])
    ctf.AddRGBPoint(15,rgb[7][0],rgb[7][1],rgb[7][2])
    ctf.AddRGBPoint(25,rgb[8][0],rgb[8][1],rgb[8][2])
    ctf.AddRGBPoint(35,rgb[9][0],rgb[9][1],rgb[9][2])
    ctf.AddRGBPoint(45,rgb[10][0],rgb[10][1],rgb[10][2])
    return ctf


def make_color_table():
    
     
    rgb = []
    for i in range(len(rgb255)):
        rgb.append([rgb255[i][0] / 255, rgb255[i][1] / 255, rgb255[i][2] / 255])
        
    ctf =  vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToRGB()
    ctf.AddRGBPoint(0, rgb[0][0], rgb[0][1], rgb[0][2])
    ctf.AddRGBPoint(10, rgb[1][0], rgb[1][1], rgb[1][2])
    ctf.AddRGBPoint(25, rgb[2][0], rgb[2][1], rgb[2][2])
    ctf.AddRGBPoint(75, rgb[3][0], rgb[3][1], rgb[3][2])
    ctf.AddRGBPoint(100, rgb[4][0], rgb[4][1], rgb[4][2])
    ctf.AddRGBPoint(110,rgb[5][0], rgb[5][1], rgb[5][2])  
    ctf.AddRGBPoint(125,rgb[6][0], rgb[6][1], rgb[6][2]) 
    ctf.AddRGBPoint(150,rgb[7][0], rgb[7][1], rgb[7][2]) 
    ctf.AddRGBPoint(170,rgb[8][0], rgb[8][1], rgb[8][2]) 
    ctf.AddRGBPoint(200,rgb[9][0], rgb[9][1], rgb[9][2]) 
    ctf.AddRGBPoint(250,rgb[10][0], rgb[10][1], rgb[10][2])   
    ctf.AddRGBPoint(300,rgb[11][0], rgb[11][1], rgb[11][2])   
    ctf.AddRGBPoint(400,rgb[12][0], rgb[12][1], rgb[12][2])  
    ctf.AddRGBPoint(500,rgb[13][0], rgb[13][1], rgb[13][2])   
    ctf.AddRGBPoint(600,rgb[14][0], rgb[14][1], rgb[14][2])  
    ctf.AddRGBPoint(700,rgb[15][0], rgb[15][1], rgb[15][2]) 
    ctf.AddRGBPoint(750,rgb[16][0], rgb[16][1], rgb[16][2]) 
    ctf.AddRGBPoint(800,rgb[17][0], rgb[17][1], rgb[17][2]) 
    ctf.AddRGBPoint(900,rgb[18][0], rgb[18][1], rgb[18][2]) 
    ctf.AddRGBPoint(1000,rgb[19][0], rgb[19][1], rgb[19][2]) 
    ctf.AddRGBPoint(1100,rgb[20][0], rgb[20][1], rgb[20][2])
    ctf.AddRGBPoint(1200,rgb[21][0], rgb[21][1], rgb[21][2])
    ctf.AddRGBPoint(1300,rgb[22][0], rgb[22][1], rgb[22][2])
    ctf.AddRGBPoint(1400,rgb[23][0], rgb[23][1], rgb[23][2])
    ctf.AddRGBPoint(1500,rgb[24][0], rgb[24][1], rgb[24][2])
    
    
    return ctf


def isoContoursGen(fileName):
    rainReader=vtk.vtkXMLImageDataReader()
    rainReader.SetFileName(fileName)
    # data/rainVTI/rain_2021.vti

    rainReader.Update()
    rainReader = rainReader
    rainFile = "data/rainVTI/rain_"
    
    arrele = rainReader.GetOutput().GetPointData().GetArray(0)
    
    # self.warp = warp
    #contour
    cfilter = vtk.vtkContourFilter()
    
    cfilter.SetInputConnection(rainReader.GetOutputPort())
    cfilter.GenerateValues(30, 0, 1500)
    cfilter.Update()
    cfilter = cfilter
    curves = cfilter.GetOutput()
    arr = curves.GetPoints().GetData()
    arrnp = numpy_support.vtk_to_numpy(arr)
    radius = 6385000
    # self.radius = radius
    coor_sphere = convert(arr=arrnp, r=radius)
    
    curves.GetPoints().SetData(coor_sphere)

    return curves


####################################################


####################################################

class colorbar_param:
    def __init__(self, title='No title', title_col=[1,1,1], title_font_size=22, label_col=[1,1,1], pos=[0.9, 0.5], width=80, height=400, nlabels=4, font_size=18, title_offset=10):
        self.title=title
        self.title_col=title_col
        self.label_col=label_col
        self.pos=pos
        self.width=width
        self.height=height
        self.nlabels=nlabels
        self.font_size=font_size
        self.title_offset=title_offset
        self.title_font_size=title_font_size


class colorbar:
    def __init__(self, ctf, param, is_float=True):
        # Create a color bar
        self.scalar_bar = vtk.vtkScalarBarActor()
        # size and relative position
        self.scalar_bar.SetLookupTable(ctf)
        self.scalar_bar.SetPosition(param.pos[0], param.pos[1])
        self.scalar_bar.SetMaximumWidthInPixels(param.width)
        self.scalar_bar.SetMaximumHeightInPixels(param.height)
        # title properties
        self.scalar_bar.SetTitle(param.title)
        self.scalar_bar.GetTitleTextProperty().SetColor(param.title_col[0], param.title_col[1],  param.title_col[2])
        self.scalar_bar.SetVerticalTitleSeparation(param.title_offset)
        self.scalar_bar.GetTitleTextProperty().ShadowOff()
        self.scalar_bar.GetTitleTextProperty().SetFontSize(param.title_font_size)
        self.scalar_bar.GetTitleTextProperty().BoldOn()
        self.scalar_bar.GetLabelTextProperty().SetFontSize(param.font_size)
        self.scalar_bar.GetLabelTextProperty().BoldOn()
        self.scalar_bar.UnconstrainedFontSizeOn()
        # label properties
        self.scalar_bar.SetNumberOfLabels(param.nlabels)
        self.scalar_bar.SetTextPad(8)
        self.scalar_bar.DrawTickLabelsOn()
        if is_float:
            format='%0.2f'
        else:
            format='%0.0f'
        self.scalar_bar.SetLabelFormat(format)
        self.scalar_bar.GetLabelTextProperty().SetColor(param.label_col[0],
                                                   param.label_col[1],
                                                   param.label_col[2])
        self.scalar_bar.GetLabelTextProperty().SetFontSize(param.font_size)
        self.scalar_bar.GetLabelTextProperty().BoldOff()
        self.scalar_bar.GetLabelTextProperty().ShadowOff()
    
    def get(self):
        return self.scalar_bar


####################################################


####################################################

class Ui_MainWindow(object):
    # global toggle_button
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('The Main Window')
        MainWindow.setWindowTitle('Simple VTK + PyQt5 Example')
        # in Qt, windows are made of widgets.
        # centralWidget will contains all the other widgets
        self.centralWidget = QWidget(MainWindow)
        # we will organize the contents of our centralWidget
        # in a grid / table layout
        # Here is a screenshot of the layout:
        # https://www.cs.purdue.edu/~cs530/projects/img/PyQtGridLayout.png
        self.gridlayout = QGridLayout(self.centralWidget)
        # vtkWidget is a widget that encapsulates a vtkRenderWindow
        # and the associated vtkRenderWindowInteractor. We add
        # it to centralWidget.
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        # Sliders
        self.slider_year = QSlider()
        self.year_label = QLabel()
        self.toggle_button = QPushButton()
        self.toggle_button.setText('Disable Rainfall')
        self.toggle_button.setCheckable(True)
        self.toggle_button2 = QPushButton()
        self.toggle_button2.setText('Disable Elevation')
        self.toggle_button2.setCheckable(True)
        # toggle_button = self.toggle_button1

        self.camera_info = QTextEdit()
        self.camera_info.setReadOnly(True)
        self.camera_info.setAcceptRichText(True)
        self.camera_info.setHtml("<div style='font-weight: bold'>Camera settings</div>")
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # We are now going to position our widgets inside our
        # grid layout. The top left corner is (0,0)
        # Here we specify that our vtkWidget is anchored to the top
        # left corner and spans 3 rows and 4 columns.
        
        
        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 4, 4)
        
        self.gridlayout.addWidget(QLabel("Year: "), 4, 0, 1, 1)
        self.gridlayout.addWidget(self.year_label, 4, 1, 1, 1)
        self.year_label.setText("2000")
        
        self.gridlayout.addWidget(QLabel("Year Value"), 5, 0, 1, 1)
        self.gridlayout.addWidget(self.slider_year, 5, 1, 1, 1)


        self.comboBox = QComboBox()
        self.comboBox.addItem("Vegetation")
        self.comboBox.addItem("Surface Temperature")

        self.gridlayout.addWidget(QLabel("Data to display : "), 6, 0, 1, 1)
        self.gridlayout.addWidget(self.comboBox, 6, 1, 1, 1)

        self.gridlayout.addWidget(QLabel( "Disable Rainfall "), 7, 0, 1, 1)
        self.gridlayout.addWidget(self.toggle_button, 7, 1, 1, 1)
        
        
        self.gridlayout.addWidget(QLabel( "Disable Elevation "), 8, 0, 1, 1)
        self.gridlayout.addWidget(self.toggle_button2, 8, 1, 1, 1)

    
        MainWindow.setCentralWidget(self.centralWidget)



class PyQtDemo(QMainWindow):
    global renderer
    
    def addActors(self):
        if not self.ui.toggle_button.isChecked():
            # print(self.cactor.GetProperty().GetLineWidth())
            print("Here " + str(self.cactor.GetProperty().GetLineWidth()))
            self.cactor.GetProperty().SetLineWidth(1.5)
            self.ren.AddActor(self.cactor)
            self.ren.AddActor(self.colorbar_actor)
            

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        global renderer
        global window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #self.scale = args.scale
        self.scale = 50
        self.year = 2000
        

        # Source
        ireader=vtk.vtkXMLPolyDataReader()        
        ireader.SetFileName("data/elevation/elevation_sphere_large.vtp")
        ireader.Update()


        sreader=vtk.vtkJPEGReader()
        file_name = "data/vegetation/vegetation_"+str(self.year)+".jpg"
        sreader.SetFileName(file_name)
        self.file = "vegetation/vegetation_"
        self.sreader = sreader

        texture=vtk.vtkTexture()
        texture.SetInputConnection(sreader.GetOutputPort())

        warp=vtk.vtkWarpScalar()
        warp.SetInputConnection(ireader.GetOutputPort())
        warp.SetScaleFactor(self.scale)
        warp.Update()
        self.warp = warp
        warp.SetScaleFactor(self.scale)

        imapper=vtk.vtkDataSetMapper() 
        imapper.SetInputConnection(warp.GetOutputPort())
        imapper.ScalarVisibilityOff()

        iactor=vtk.vtkActor()
        iactor.SetMapper(imapper)
        iactor.SetTexture(texture)
        

        ctf = make_color_table()
        colorbarparam = colorbar_param(title = "Rainfall")
        colorbar_actor = colorbar(ctf,colorbarparam).get()

        veg_ctf = make_vegetation_table()
        colorbarparam_veg = colorbar_param(title = "Vegetation",pos=[0.1,0.5])
        colorbar_actor_veg = colorbar(veg_ctf,colorbarparam_veg).get()

        temp_ctf = make_temp_table()
        colorbarparam_temp = colorbar_param(title = "Temperature (°C)",pos=[0.1,0.5])
        colorbar_actor_temp = colorbar(temp_ctf,colorbarparam_temp).get()


        curves = isoContoursGen(fileName="data/rainVTI/rain_2021.vti")

        cmapper=vtk.vtkPolyDataMapper() 
        cmapper.SetInputData(curves)
        self.cmapper = cmapper
        cmapper.SetLookupTable(ctf)
        # cmapper.ScalarVisibilityOff()
        cmapper.Update()

        cactor=vtk.vtkActor()
        cactor.SetMapper(cmapper)
        cactor.GetProperty().SetOpacity(1)


        # Create the Renderer
        self.ren = vtk.vtkRenderer()
        renderer = self.ren

        #camera
        camera = self.ren.GetActiveCamera()
        camera.SetPosition(-6016408.402472742, -21485231.33252782, 8849218.06925976)
        camera.SetFocalPoint(4050.0, 6022.75, -15222.5)
        camera.SetViewUp(-0.28714312753228705, 0.43288884593951726, 0.8544917035127549)
        camera.SetClippingRange(4602250.824907519, 48508541.6215622)
        
        iactor.GetProperty().SetOpacity(1)
            
        self.iactor = iactor
        self.cactor = cactor
        self.colorbar_actor = colorbar_actor
        self.colorbar_actor_veg = colorbar_actor_veg
        self.colorbar_actor_temp = colorbar_actor_temp
        
        self.ren.AddActor(self.iactor)
        self.ren.AddActor(self.colorbar_actor_veg)
        PyQtDemo.addActors(self=self)        
        
        self.ren.GradientBackgroundOn()  # Set gradient for background
        self.ren.SetBackground(0.75, 0.75, 0.75)  # Set background to silver
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

        # Setting up widgets
        def slider_setup(slider, val, bounds, interv):
            slider.setOrientation(QtCore.Qt.Horizontal)
            slider.setValue(int(val))
            slider.setTracking(False)
            slider.setTickInterval(interv)
            slider.setTickPosition(QSlider.TicksAbove)
            slider.setRange(bounds[0], bounds[1])





        
        slider_setup(self.ui.slider_year, self.year, [2000, 2022], 1)


    def combo_callback(self, val):
        # print("Combo selected :" , val)
        if val == 0 : 
            self.file="vegetation/vegetation_" 
            self.ren.AddActor(self.colorbar_actor_veg)
            self.ren.RemoveActor(self.colorbar_actor_temp)
        else : 
            self.file = "temp/surface_temp_"  
            self.ren.AddActor(self.colorbar_actor_temp)
            self.ren.RemoveActor(self.colorbar_actor_veg)            
        
        file_name = "data/"+self.file+str(self.year)+".jpg"
        self.sreader.SetFileName(file_name)
        self.sreader.Update()
        self.ui.log.insertPlainText("File Updated to {}".format(file_name))

        self.ui.vtkWidget.GetRenderWindow().Render()


    def year_callback(self, val):
        print("Year selected :" , val)
        self.year = val
        file_name = "data/"+self.file+str(self.year)+".jpg"
        self.sreader.SetFileName(file_name)
        self.sreader.Update()
        self.ui.log.insertPlainText("File Updated to {}".format(file_name))
        window.ui.year_label.setText(str(self.year))

        # self.ui.vtkWidget.GetRenderWindow().Render()
        # yr = int(self.year)-2000
        # if window.ui.toggle_button.isChecked():
        # print("File updated : "+"data/rainVTI/rain_"+str(self.year)+".vti")
        file = "data/rainVTI/rain_"+str(self.year)+".vti"
        curves = isoContoursGen(fileName=file)
        self.cmapper.SetInputData(curves)

        self.ui.vtkWidget.GetRenderWindow().Render()


    def camera_callback(self):
        print_camera_settings(self.ren.GetActiveCamera(), self.ui.camera_info, self.ui.log)


    def toggle_callback_iso(self):
        # print("Toggle Called")
        
        self.addActors()
        if not window.ui.toggle_button.isChecked():
            # print("Added")
            self.ren.AddActor(self.cactor)
            self.ren.AddActor(self.colorbar_actor)
            window.ui.toggle_button.setText("Disable Rainfall ")
        else:
            # self.cactor.SetVisibility(False)
            # self.colorbar_actor.SetVisibility(False)
            self.ren.RemoveActor(self.cactor)
            self.ren.RemoveActor(self.colorbar_actor)
            window.ui.toggle_button.setText("Enable Rainfall ")
            # print("Removed")
            
            
    def toggle_callback_ele(self):
        # print("Toggle2 Called")
        
        self.addActors()
        if window.ui.toggle_button2.isChecked():
            # print("Added2")
            self.scale = 0
            self.warp.SetScaleFactor(self.scale)
            window.ui.toggle_button2.setText("Enable elevation ")
        else:
            self.scale = 50
            self.warp.SetScaleFactor(self.scale)
            window.ui.toggle_button2.setText("Disable elevation ")
            # print("Removed2")
        
        self.ui.vtkWidget.GetRenderWindow().Render()

    # def scale_callback(self, val):
    #     # print("Year selected :" , val)
    #     self.scale = val
    #     self.warp.SetScaleFactor(self.scale)
    #     self.ui.log.insertPlainText('Theta resolution set to {}\n'.format(self.scale))
    #     self.ui.vtkWidget.GetRenderWindow().Render()



####################################################
 
 
 
 
 
####################################################
 
 
def print_camera_settings():
    global renderer
    # ---------------------------------------------------------------
    # Print out the current settings of the camera
    # ---------------------------------------------------------------
    camera = renderer.GetActiveCamera()
    print("Camera settings:")
    print("  * position:        %s" % (camera.GetPosition(),))
    print("  * focal point:     %s" % (camera.GetFocalPoint(),))
    print("  * up vector:       %s" % (camera.GetViewUp(),))
    print("  * clipping range:  %s" % (camera.GetClippingRange(),))


def key_pressed_callback(obj, event):
    global args
    # ---------------------------------------------------------------
    # Attach actions to specific keys
    # ---------------------------------------------------------------
    key = obj.GetKeySym()
    if key == "s":
        save_frame()
    elif key == "c":
        print_camera_settings()

    
def save_frame():
    print("Save Image")
    global frame_counter
    global window
    global args
    # ---------------------------------------------------------------
    # Save current contents of render window to PNG file
    # --------------------------------------------------------------


####################################################




####################################################


if __name__=="__main__":
    global args
    # global renderer

    parser= argparse.ArgumentParser(description='Assignment 1 Task 1')

    args=parser.parse_args()


    app = QApplication(sys.argv)
    window = PyQtDemo()
    window.ui.vtkWidget.GetRenderWindow().SetSize(1024, 768)
    window.ui.log.insertPlainText('Set render window resolution to {}\n'.format([1024,768]))
    window.show()
    window.setWindowState(Qt.WindowMaximized)  # Maximize the window
    window.iren.Initialize() # Need this line to actually show
                             # the render inside Qt

     #camera settings 
    window.iren.AddObserver("KeyPressEvent", key_pressed_callback)

    window.ui.slider_year.valueChanged.connect(window.year_callback)
    window.ui.comboBox.activated.connect(window.combo_callback)
    # window.ui.slider_year.valueChanged.connect(window.radius_callback)
    window.ui.toggle_button.clicked.connect(window.toggle_callback_iso)
    window.ui.toggle_button2.clicked.connect(window.toggle_callback_ele)
    print(window.ui.toggle_button.isChecked())
    sys.exit(app.exec_())