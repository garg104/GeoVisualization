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


frame_counter = 0

def convert(arr, r):
    
    a = []
    for temp in arr:
        # print(temp)
        # x - long, theta = long x, phi-lat y
        x = temp[0]+180 # long
        y = temp[1] # lat
        # x_new = r * np.sin(x * np.pi/180) * np.cos(y * np.pi/180)
        # y_new = r * np.sin(x * np.pi/180) * np.sin(y * np.pi/180)
        # z_new = r * np.cos(x * np.pi/180)
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



class Ui_MainWindow(object):
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
        # self.slider_radius = QSlider()
        # self.slider_phi = QSlider()
        # self.slider_radius = QSlider()
        # Push buttons
        # self.push_screenshot = QPushButton()
        # self.push_screenshot.setText('Save screenshot')
        # self.push_camera = QPushButton()
        # self.push_camera.setText('Update camera info')
        # self.push_quit = QPushButton()
        # self.push_quit.setText('Quit')
        # Text windows
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
        self.gridlayout.addWidget(QLabel("Year Value"), 4, 0, 1, 1)
        self.gridlayout.addWidget(self.slider_year, 4, 1, 1, 1)

    
        self.gridlayout.addWidget(QLabel("Year Value Selected : "), 5, 0, 1, 1)
        self.gridlayout.addWidget(self.year_label, 5, 1, 1, 1)
        self.year_label.setText("test")

        self.comboBox = QComboBox()
        self.comboBox.addItem("Vegetation")
        self.comboBox.addItem("Surface Temperature")

        self.gridlayout.addWidget(QLabel("Data to display : "), 6, 0, 1, 1)
        self.gridlayout.addWidget(self.comboBox, 6, 1, 1, 1)

    
        # self.gridlayout.addWidget(QLabel("Radius Value"), 7, 0, 1, 1)
        # self.gridlayout.addWidget(self.slider_radius, 7, 1, 1, 1)

        
        # self.label = self.slider_year
        # self.gridlayout.addWidget(QLabel("Year Value Selected"), 5, 2, 1, 1)
        # self.gridlayout.addWidget(self.label, 5, 3, 1, 1)




        # self.gridlayout.addWidget(QLabel("Phi resolution"), 5, 0, 1, 1)
        # self.gridlayout.addWidget(self.slider_phi, 5, 1, 1, 1)
        # self.gridlayout.addWidget(QLabel("Edge radius"), 4, 2, 1, 1)
        # self.gridlayout.addWidget(self.slider_radius, 4, 3, 1, 1)
        # self.gridlayout.addWidget(self.push_screenshot, 0, 5, 1, 1)
        # self.gridlayout.addWidget(self.push_camera, 1, 5, 1, 1)
        # self.gridlayout.addWidget(self.camera_info, 2, 4, 1, 2)
        # self.gridlayout.addWidget(self.log, 3, 4, 1, 2)
        # self.gridlayout.addWidget(self.push_quit, 5, 5, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)




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
    radius = 6368000
    # self.radius = radius
    coor_sphere = convert(arr=arrnp, r=radius)
    
    curves.GetPoints().SetData(coor_sphere)

    return curves


class PyQtDemo(QMainWindow):
    global renderer

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        global renderer
        global window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #self.scale = args.scale
        self.scale = 10
        self.year = 2023
        

        # Source
        ireader=vtk.vtkXMLPolyDataReader()
        # ireader.SetFileName(args.geometry)
        # ireader.SetFileName("elevation_large.vti")
        
        ireader.SetFileName("data/elevation/elevation_sphere_large.vtp")
        ireader.Update()



        output=ireader.GetOutput()
        print(f'our output is \n{output}')
        scalars=output.GetPointData().GetScalars()
        print('scalars is \n{scalars}')

        sreader=vtk.vtkJPEGReader()
        # sreader.SetFileName(args.image)
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
        # if args.scale is None:
        #     warp.SetScaleFactor(10)
        # else:
        #     warp.SetScaleFactor(args.scale)
        #     warp.Update()

        imapper=vtk.vtkDataSetMapper() 
        imapper.SetInputConnection(warp.GetOutputPort())
        imapper.ScalarVisibilityOff()

        iactor=vtk.vtkActor()
        iactor.SetMapper(imapper)
        iactor.SetTexture(texture)




        # renderer=vtk.vtkRenderer()
        # renderer.AddActor(iactor)

        # window=vtk.vtkRenderWindow()
        # window.AddRenderer(renderer)
        # window.SetSize(1024,1024)

        # interactor=vtk.vtkRenderWindowInteractor()
        # interactor.SetRenderWindow(window)
        # interactor.Initialize()

        #source
        # [self.sphere, self.edges] = make_sphere(20, 20, 0.001)
        # mapToSphere = vtk.vtkTextureMapToSphere()
        # mapToSphere.SetInputConnection(self.sphere.GetOutputPort())
        # sphere_mapper = vtk.vtkPolyDataMapper()
        # sphere_mapper.SetInputConnection(mapToSphere.GetOutputPort())
    
        curves = isoContoursGen(fileName="data/rainVTI/rain_2021.vti")


        #tubefilter
        # tubeFilter = vtk.vtkTubeFilter()
        # tubeFilter.SetInputConnection(cfilter.GetOutputPort())
        # tubeFilter.SetRadius(5000)
        # # tubeFilter.SetNumberOfSides(5)
        # tubeFilter.Update()

        #color tubes
        ctf =  vtk.vtkColorTransferFunction()
        ctf.SetColorSpaceToRGB()
        ctf.AddRGBPoint(0, 1, 0, 0)
        ctf.AddRGBPoint(10, 1, 1, 1)
        ctf.AddRGBPoint(25,1,1,1)
        ctf.AddRGBPoint(50,1,1,1)
        ctf.AddRGBPoint(75,1,1,1)
        ctf.AddRGBPoint(100, 0.1, 0.1, 1)
        ctf.AddRGBPoint(110, 1, 1, 1)
        ctf.AddRGBPoint(125,1,1,1)
        ctf.AddRGBPoint(150,1,1,1)
        ctf.AddRGBPoint(175,1,1,1)
        ctf.AddRGBPoint(200, 0.6, 0.6, 0.6)
        ctf.AddRGBPoint(300, 0.1, 0.9, 0.3)
        ctf.AddRGBPoint(500, 1, 0.6, .1)
        ctf.AddRGBPoint(700, 1, 0.6, 0.8)
        ctf.AddRGBPoint(900, 1, 0, 0.89)
        ctf.AddRGBPoint(1200, 0, 1, 0.89)
        ctf.AddRGBPoint(1500, 1, 1, 0) #same color from 1000 to 8000 m elevations
        ctf.AddRGBPoint(1700, 1, 0, 0.5)
        ctf.AddRGBPoint(1800, 1, 1, 0.5)
        ctf.AddRGBPoint(1900, 1, 0.5, 0)
        ctf.AddRGBPoint(2000, 1, 0, 0)

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

        #         Camera settings:
        #   * position:        (-6016408.402472742, -21485231.33252782, 8849218.06925976)
        #   * focal point:     (4050.0, 6022.75, -15222.5)
        #   * up vector:       (-0.28714312753228705, 0.43288884593951726, 0.8544917035127549)
        #   * clipping range:  (4602250.824907519, 48508541.6215622)

        #camera
        camera = self.ren.GetActiveCamera()
        camera.SetPosition(-6016408.402472742, -21485231.33252782, 8849218.06925976)
        camera.SetFocalPoint(4050.0, 6022.75, -15222.5)
        camera.SetViewUp(-0.28714312753228705, 0.43288884593951726, 0.8544917035127549)
        camera.SetClippingRange(4602250.824907519, 48508541.6215622)
        

        iactor.GetProperty().SetOpacity(1)
        self.ren.AddActor(iactor)
        self.ren.AddActor(cactor)
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

        
        slider_setup(self.ui.slider_year, self.year, [2000, 2023], 1)
        # slider_setup(self.ui.slider_radius, self.radius, [2000, 2020], 5)
        # slider_setup(self.ui.slider_phi, self.phi, [3, 200], 10)
        # slider_setup(self.ui.slider_radius, self.radius*100, [1, 10], 2)

    def scale_callback(self, val):
        # print("Year selected :" , val)
        self.scale = val
        self.warp.SetScaleFactor(self.scale)
        self.ui.log.insertPlainText('Theta resolution set to {}\n'.format(self.scale))
        self.ui.vtkWidget.GetRenderWindow().Render()

    def radius_callback(self, val):
        # print("Year selected :" , val)
        self.radius = val
        
        
        # self.ui.log.insertPlainText('Theta resolution set to {}\n'.format(self.scale))
        self.ui.vtkWidget.GetRenderWindow().Render()

    def combo_callback(self, val):
        print("Combo selected :" , val)
        if val == 0 : self.file="vegetation/vegetation_" 
        else : self.file = "temp/surface_temp_"  
        file_name = "data/"+self.file+str(self.year)+".jpg"
        self.sreader.SetFileName(file_name)
        self.sreader.Update()
        self.ui.log.insertPlainText("File Updated to {}".format(file_name))
        # self.year = val
        # file_name = "data/surface_temp_"+str(self.year)+".jpg"
        # self.sreader.SetFileName(file_name)
        # self.ui.log.insertPlainText("File Updated to {}".format(file_name))

        self.ui.vtkWidget.GetRenderWindow().Render()


    def year_callback(self, val):
        print("Year selected :" , val)
        self.year = val
        file_name = "data/"+self.file+str(self.year)+".jpg"
        self.sreader.SetFileName(file_name)
        self.sreader.Update()
        self.ui.log.insertPlainText("File Updated to {}".format(file_name))

        # self.ui.vtkWidget.GetRenderWindow().Render()
        # yr = int(self.year)-2000
        print("File updated : "+"data/rainVTI/rain_"+str(self.year)+".vti")
        file = "data/rainVTI/rain_"+str(self.year)+".vti"
        curves = isoContoursGen(fileName=file)
        self.cmapper.SetInputData(curves)
        # self.rainReader.SetFileName("data/rainVTI/rain_"+str(self.year)+".vti")
        # self.rainReader.Update()
        # self.cfilter.SetInputConnection(self.rainReader.GetOutputPort())

        

        self.ui.vtkWidget.GetRenderWindow().Render()
        # self.scale = val
        # self.warp.SetScaleFactor(self.scale)
        # self.ui.log.insertPlainText('Theta resolution set to {}\n'.format(self.scale))
        # self.ui.vtkWidget.GetRenderWindow().Render()
    # def phi_callback(self, val):
    #     self.phi = val
    #     self.sphere.SetPhiResolution(self.phi)
    #     self.ui.log.insertPlainText('Phi resolution set to {}\n'.format(self.phi))
    #     self.ui.vtkWidget.GetRenderWindow().Render()

    # def radius_callback(self, val):
    #     self.radius = val/1000.
    #     self.edges.SetRadius(self.radius)
    #     self.ui.log.insertPlainText('Edge radius set to {}\n'.format(self.radius))
    #     self.ui.vtkWidget.GetRenderWindow().Render()

    # def screenshot_callback(self):
    #     save_frame(self.ui.vtkWidget.GetRenderWindow(), self.ui.log)

    def camera_callback(self):
        print_camera_settings(self.ren.GetActiveCamera(), self.ui.camera_info, self.ui.log)

    

    # def quit_callback(self):
    #     sys.exit()
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

if __name__=="__main__":
    global args
    # global renderer

    parser= argparse.ArgumentParser(description='Assignment 1 Task 1')
    # parser.add_argument('-g','--geometry',type=str,help='Filename for heightfield')
    # parser.add_argument('-i','--image',type=str,required=True,help='Filename for satellite imagery')

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
    window.ui.slider_year.valueChanged.connect(window.radius_callback)
    sys.exit(app.exec_())