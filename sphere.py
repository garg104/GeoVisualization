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

frame_counter = 0

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

class PyQtDemo(QMainWindow):

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #self.scale = args.scale
        self.scale = 10
        self.year = 2023
        

        # Source
        ireader=vtk.vtkXMLPolyDataReader()
        # ireader.SetFileName(args.geometry)
        # ireader.SetFileName("elevation_large.vti")
        
        ireader.SetFileName("data/elevation_sphere_large.vtp")
        ireader.Update()



        output=ireader.GetOutput()
        print(f'our output is \n{output}')
        scalars=output.GetPointData().GetScalars()
        print('scalars is \n{scalars}')

        sreader=vtk.vtkJPEGReader()
        # sreader.SetFileName(args.image)
        file_name = "data/vegetation_"+str(self.year)+".jpg"
        sreader.SetFileName(file_name)
        self.file = "vegetation_"
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
        [self.sphere, self.edges] = make_sphere(20, 20, 0.001)
        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputConnection(self.sphere.GetOutputPort())
        sphere_actor = vtk.vtkActor()
        sphere_actor.SetMapper(sphere_mapper)
        sphere_actor.GetProperty().SetColor(1, 1, 0)

        #contour
        cfilter = vtk.vtkContourFilter()
        cfilter.SetInputConnection(warp.GetOutputPort())
        cfilter.GenerateValues(19, -10000, 8000)

        #tubefilter
        tubeFilter = vtk.vtkTubeFilter()
        tubeFilter.SetInputConnection(cfilter.GetOutputPort())
        tubeFilter.SetRadius(5000)
        # tubeFilter.SetNumberOfSides(5)
        tubeFilter.Update()

        #color tubes
        ctf =  vtk.vtkColorTransferFunction()
        ctf.SetColorSpaceToRGB()
        ctf.AddRGBPoint(-11000, 1, 1, 1) # white color for negative elevations
        ctf.AddRGBPoint(-1000, 1, 1, 1) # same color at -1000 to force all the values in between to be white as well
        ctf.AddRGBPoint(0, 1, 0, 0) # sea level is red 
        ctf.AddRGBPoint(1000, 0, 0, 1) # positive elevations are blue 
        ctf.AddRGBPoint(8000, 0, 0, 1) # same color from 1000 to 8000 m elevations

        cmapper=vtk.vtkPolyDataMapper() 
        cmapper.SetInputConnection(cfilter.GetOutputPort())
        cmapper.SetLookupTable(ctf)
        # cmapper.ScalarVisibilityOff()
        cmapper.Update()


        cactor=vtk.vtkActor()
        # cactor.SetMapper(cmapper)

        # Create the Renderer
        self.ren = vtk.vtkRenderer()
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

        slider_setup(self.ui.slider_year, self.scale, [2000, 2023], 5)
        # slider_setup(self.ui.slider_phi, self.phi, [3, 200], 10)
        # slider_setup(self.ui.slider_radius, self.radius*100, [1, 10], 2)

    def scale_callback(self, val):
        # print("Year selected :" , val)
        self.scale = val
        self.warp.SetScaleFactor(self.scale)
        self.ui.log.insertPlainText('Theta resolution set to {}\n'.format(self.scale))
        self.ui.vtkWidget.GetRenderWindow().Render()

    def combo_callback(self, val):
        print("Combo selected :" , val)
        if val == 0 : self.file="vegetation_" 
        else : self.file = "surface_temp_"  
        file_name = "data/"+self.file+str(self.year)+".jpg"
        self.sreader.SetFileName(file_name)
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
        self.ui.log.insertPlainText("File Updated to {}".format(file_name))

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

    # def camera_callback(self):
    #     print_camera_settings(self.ren.GetActiveCamera(), self.ui.camera_info, self.ui.log)

    # def quit_callback(self):
    #     sys.exit()

if __name__=="__main__":
    global args

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

    window.ui.slider_year.valueChanged.connect(window.year_callback)
    window.ui.comboBox.activated.connect(window.combo_callback)
    sys.exit(app.exec_())