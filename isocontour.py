#!/usr/bin/env python

# Purdue CS530 - Introduction to Scientific Visualization
# Spring 2023

# PyQt6 version of pyqt5_demo.py
import numpy as np

from vtk.util import numpy_support
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QSlider, QGridLayout, QLabel, QPushButton, QTextEdit
import PyQt6.QtCore as QtCore
from PyQt6.QtCore import Qt
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import argparse
import sys

frame_counter = 0

def convert(arr, r):
    
    a = []
    for temp in arr:
        # print(temp)
        x = temp[0] + 180
        y = temp[1] + 90
        x_new = r * np.sin(x * np.pi/180) * np.cos(y * np.pi/180)
        y_new = r * np.sin(x * np.pi/180) * np.sin(y * np.pi/180)
        z_new = r * np.cos(x * np.pi/180)
        temp2 = np.array([x_new, y_new, z_new], dtype=np.float32)
        a.append(temp2)
       
    aa = np.asarray(a)
    aaa = numpy_support.numpy_to_vtk(aa) 

    return aaa



def make_sphere(radius, resolution_theta, resolution_phi, edge_radius):
    # create and visualize sphere
    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetRadius(radius)
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



def make_map(elevation, image):
    # elevation is the file that has elevation data points
    # image is the point that sets the texture of the map
    

    # read the elevation data
    rainReader=vtk.vtkXMLImageDataReader()
    rainReader.SetFileName(args.g)
    rainReader.Update()
    # print(rainReader.GetOutput().GetScalarRange())
    # print(rainReader.GetOutput().GetPointData().GetScalars())
    

    arrele = rainReader.GetOutput().GetPointData().GetArray(0)
    
    # values = numpy_support.vtk_to_numpy(arrele)
    # sorted = np.sort(np.unique(values))
    # print(sorted)
    
    # rng = arrele.GetNumberOfTuples()
    # f = open("tiffData.txt","w")
    # for ind in range(rng):
    #     f.write(str(arrele.GetTuple(ind)) + "\n")
    # f.close()
    # exit()
    # exit()
    # map the elevation
    elevationMapper = vtk.vtkDataSetMapper()
    elevationMapper.SetInputData(rainReader.GetOutput())
    elevationMapper.SetScalarRange(0, 255)
    elevationMapper.ScalarVisibilityOff()
    
    
    # read the image data to set the texture of the map
    textureReader=vtk.vtkJPEGReader()
    textureReader.SetFileName(args.i)
    textureReader.Update()

    # connect the texture data to vtkTexture
    texture=vtk.vtkTexture()
    texture.SetInputConnection(textureReader.GetOutputPort())
  
    # link the elevationMapper with elevationActor and set the texture
    elevationActor=vtk.vtkActor()
    # elevationActor.SetMapper(elevationMapper)
    # elevationActor.SetTexture(texture)
    
    
    # compute the iso-contours
    isoContour = vtk.vtkContourFilter()
    isoContour.GenerateValues(10, 0, 1500)
    isoContour.SetInputConnection(rainReader.GetOutputPort())
    isoContour.Update()
    curves = isoContour.GetOutput()
    arr = curves.GetPoints().GetData()
    arrnp = numpy_support.vtk_to_numpy(arr)
    
    
    radius = 1.0
    coor_sphere = convert(arr=arrnp, r=radius)
    
    curves.GetPoints().SetData(coor_sphere)
    
    
    [sphere, edges] = make_sphere(radius, 20, 20, 0.001)
    sphere_mapper = vtk.vtkPolyDataMapper()
    sphere_mapper.SetInputConnection(sphere.GetOutputPort())
    sphere_actor = vtk.vtkActor()
    sphere_actor.SetMapper(sphere_mapper)
    # sphere_actor.GetProperty().SetColor(1, 1, 0)
    sphere_actor.SetTexture(texture)

    # sphere_source.SetThetaResolution(resolution_theta)
    # sphere_source.SetPhiResolution(resolution_phi)
    
    
    
    # import pdb
    # pdb.set_trace()
    
    # wrap the iso-contours in tubes
    tubes = vtk.vtkTubeFilter()
    tubes.SetInputConnection(isoContour.GetOutputPort())
    tubes.SetRadius(4000)
    
    # color the tubes
    colorTable = vtk.vtkColorTransferFunction()
    colorTable.SetColorSpaceToRGB()
    colorTable.AddRGBPoint(0, 1, 0, 0)
    colorTable.AddRGBPoint(100, 0.1, 0.1, 1)
    colorTable.AddRGBPoint(200, 0.6, 0.6, 0.6)
    colorTable.AddRGBPoint(300, 0.1, 0.9, 0.3)
    colorTable.AddRGBPoint(500, 1, 0.6, .1)
    colorTable.AddRGBPoint(700, 1, 0.6, 0.8)
    colorTable.AddRGBPoint(900, 1, 0, 0.89)
    colorTable.AddRGBPoint(1200, 0, 1, 0.89)
    colorTable.AddRGBPoint(1500, 1, 1, 0)
    
    
    colorMapper = vtk.vtkDataSetMapper()
    # colorMapper.SetInputConnection(isoContour.GetOutputPort())
    colorMapper.SetInputData(curves)
    colorMapper.SetLookupTable(colorTable)
    
    tubesActor = vtk.vtkActor()
    tubesActor.SetMapper(colorMapper)
    
    
    return [tubes, elevationActor, tubesActor, sphere_actor]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('The Main Window')
        MainWindow.setWindowTitle('Assignment 1 Task 1')
        
        self.centralWidget = QWidget(MainWindow)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        
        # Sliders
        self.slider_tube_radius = QSlider()
        
        # Push buttons
        self.push_screenshot = QPushButton()
        self.push_quit = QPushButton()
        self.push_quit.setText('Quit')
        
        # We are now going to position our widgets inside our
        # grid layout. The top left corner is (0,0)
        # Here we specify that our vtkWidget is anchored to the top
        # left corner and spans 3 rows and 4 columns.
        self.gridLayout.addWidget(self.vtkWidget, 0, 0, 4, 4)
        self.gridLayout.addWidget(QLabel("Tube Radius"), 4, 0, 1, 1)
        self.gridLayout.addWidget(self.slider_tube_radius, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.push_quit, 5, 5, 1, 1)
        
        MainWindow.setCentralWidget(self.centralWidget)


class PyQtDemo(QMainWindow):

    def __init__(self, args, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.rad = 30000
        
        elevation = args.g
        image = args.i
        # print("Elevation: " + elevation)
        # print("Image: " + image)

        # Source
        [self.tubes, self.elevationActor, self.tubesActor, self.sphere] = make_map(elevation, image)
    
        # Create the Renderer
        self.ren = vtk.vtkRenderer()
        # self.ren.AddActor(self.elevationActor)
        self.ren.AddActor(self.tubesActor)
        self.ren.AddActor(self.sphere)
        
        # Set gradient for background
        self.ren.GradientBackgroundOn()
        
        # Set background to silver
        self.ren.SetBackground(0.75, 0.75, 0.75)
        
        # set the initial camera view
        self.ren.ResetCamera()
        self.ren.GetActiveCamera().Azimuth(180)
        self.ren.GetActiveCamera().Roll(180)
        self.ren.GetActiveCamera().Elevation(-40)
        self.ren.GetActiveCamera().Zoom(2.5)
        
        # Set up the render window
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()


        # Setting up widgets
        def slider_setup(slider, val, bounds, interv):
            slider.setOrientation(Qt.Orientation.Horizontal)
            slider.setValue(int(val))
            slider.setTracking(False)
            slider.setTickInterval(interv)
            slider.setTickPosition(QSlider.TickPosition.TicksAbove)
            slider.setRange(bounds[0], bounds[1])
 
        slider_setup(self.ui.slider_tube_radius, self.rad, [30000, 100000], 1000)


    def radius_callback(self, val):
        self.rad = (val)
        self.tubes.SetRadius(self.rad)
        self.ui.vtkWidget.GetRenderWindow().Render()

    # def screenshot_callback(self):
    #     save_frame(self.ui.vtkWidget.GetRenderWindow(), self.ui.log)

    # def camera_callback(self):
    #     print_camera_settings(self.ren.GetActiveCamera(), self.ui.camera_info, self.ui.log)

    def quit_callback(self):
        sys.exit()


if __name__=="__main__":
    global args

    # use argparse to get the filenames
    parser=argparse.ArgumentParser(description='Assignment 1 Task 1')
    parser.add_argument('-g', '-—geometry', type=str, required=True, help='Filename for height field')
    parser.add_argument('-i', '-—image', type=str, required=True, help='Filename for satellite imagery')
    # parser.add_argument('-s', '-—scale', type=float, required=True, help='Scale factor')
    
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    
    
    window = PyQtDemo(args=args)
    window.ui.vtkWidget.GetRenderWindow().SetSize(1024, 1024)
    # window.ui.log.insertPlainText('Set render window resolution to {}\n'.format(args.resolution))
    window.show()
    window.setWindowState(Qt.WindowState.WindowMaximized)  # Maximize the window
    window.iren.Initialize() # Need this line to actually show the render inside Qt

    window.ui.slider_tube_radius.valueChanged.connect(window.radius_callback)
    window.ui.push_quit.clicked.connect(window.quit_callback)
    
    sys.exit(app.exec())
