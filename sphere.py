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
rgb255 = [
            [13, 8, 135],
            [38, 5, 145],
            [58, 4, 154],
            [76, 2, 161],
            [92, 1, 166],
            [110, 0, 168],
            [126, 3, 168],
            [141, 11, 165],
            [156, 23, 158],
            [170, 35, 149],
            [181, 47, 140],
            [193, 59, 131],
            [204, 71, 120],
            [213, 83, 111],
            [222, 95, 101],
            [230, 108, 92],
            [237, 121, 83],
            [243, 135, 74],
            [248, 149, 64],
            [252, 163, 56],
            [253, 180, 47],
            [253, 197, 39],
            [251, 213, 36],
            [246, 232, 38],
            [240, 249, 33],
        ]


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
    radius = 6368000
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
        self.gridlayout.addWidget(QLabel("Year Value"), 4, 0, 1, 1)
        self.gridlayout.addWidget(self.slider_year, 4, 1, 1, 1)

    
        self.gridlayout.addWidget(QLabel("Year Value Selected : "), 5, 0, 1, 1)
        self.gridlayout.addWidget(self.year_label, 5, 1, 1, 1)
        self.year_label.setText("2023")

        self.comboBox = QComboBox()
        self.comboBox.addItem("Vegetation")
        self.comboBox.addItem("Surface Temperature")

        self.gridlayout.addWidget(QLabel("Data to display : "), 6, 0, 1, 1)
        self.gridlayout.addWidget(self.comboBox, 6, 1, 1, 1)

        self.gridlayout.addWidget(QLabel( "Disable Rainfall "), 7, 0, 1, 1)
        self.gridlayout.addWidget(self.toggle_button, 7, 1, 1, 1)

    
        MainWindow.setCentralWidget(self.centralWidget)



class PyQtDemo(QMainWindow):
    global renderer
    
    def addActors(self):
        if not self.ui.toggle_button.isChecked():
            self.ren.AddActor(self.cactor)
            self.ren.AddActor(self.colorbar_actor)

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
        

        ctf = make_color_table()
        colorbarparam = colorbar_param(title = "Rainfall")
        colorbar_actor = colorbar(ctf,colorbarparam).get()


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
        
        self.ren.AddActor(self.iactor)
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

        
        slider_setup(self.ui.slider_year, self.year, [2000, 2023], 1)

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
        window.ui.year_label.setText(str(self.year))

        # self.ui.vtkWidget.GetRenderWindow().Render()
        # yr = int(self.year)-2000
        # if window.ui.toggle_button.isChecked():
        print("File updated : "+"data/rainVTI/rain_"+str(self.year)+".vti")
        file = "data/rainVTI/rain_"+str(self.year)+".vti"
        curves = isoContoursGen(fileName=file)
        self.cmapper.SetInputData(curves)

        self.ui.vtkWidget.GetRenderWindow().Render()


    def camera_callback(self):
        print_camera_settings(self.ren.GetActiveCamera(), self.ui.camera_info, self.ui.log)


    def toggle_callback(self):
        print("Toggle Called")
        
        self.addActors()
        if not window.ui.toggle_button.isChecked():
            print("Added")
            self.ren.AddActor(self.cactor)
            self.ren.AddActor(self.colorbar_actor)
            window.ui.toggle_button.setText("Disable Rainfall ")
        else:
            # self.cactor.SetVisibility(False)
            # self.colorbar_actor.SetVisibility(False)
            self.ren.RemoveActor(self.cactor)
            self.ren.RemoveActor(self.colorbar_actor)
            window.ui.toggle_button.setText("Enable Rainfall ")
            print("Removed")


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
    window.ui.toggle_button.clicked.connect(window.toggle_callback)
    print(window.ui.toggle_button.isChecked())
    sys.exit(app.exec_())