import vtk
import tkinter as tk
from tkinter import filedialog

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory()  # Show a directory selection dialog
    return directory

def load_dicom_directory(directory):
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(directory)
    reader.Update()
    return reader

def add_roi_widget(renderer, interactor, volumeMapper, renWin):
    # Create the box widget for ROI selection
    roi_widget = vtk.vtkBoxWidget()
    roi_widget.SetInteractor(interactor)
    roi_widget.SetPlaceFactor(1.0)  # Set initial size of the box

    # Lấy bounds của volume (ảnh render)
    volume_bounds = [0] * 6
    volume.GetBounds(volume_bounds)

    # Đặt ROI Box bao quanh volume
    roi_widget.SetPlaceFactor(1.0)  # Đặt hệ số phóng đại vùng ROI bằng 1.0 để không mở rộng thêm
    roi_widget.PlaceWidget(volume_bounds)  # Đặt widget theo bounds của volume
    roi_widget.On()  # Bật ROI Box để hiển thị

    # Đảm bảo rằng khi ROI Box thay đổi, nó sẽ cập nhật đúng các giới hạn cho Volume
    def on_roi_changed(widget, event):
        # Create a vtkPolyData object to store the ROI box
        box_polydata = vtk.vtkPolyData()
        widget.GetPolyData(box_polydata)  # Get the PolyData from the widget

        # Compute the bounds of the PolyData
        box_bounds = [0] * 6
        box_polydata.GetBounds(box_bounds)  # Compute the bounds of the PolyData

        # Update Volume Mapper to only show data within the ROI
        volumeMapper.SetCroppingRegionPlanes(box_bounds)
        volumeMapper.CroppingOn()  # Enable cropping based on the ROI
        renWin.Render()

    # Gắn callback cho sự kiện thay đổi của ROI Box
    roi_widget.AddObserver(vtk.vtkCommand.InteractionEvent, on_roi_changed)

    return roi_widget

# Create the renderer, the render window, and the interactor.
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Use vtkDICOMImageReader to read DICOM files
dicom_directory = select_directory()
reader = load_dicom_directory(dicom_directory)
reader.Update()

# The volume mapper for ray-cast alpha compositing
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Color transfer function for mapping voxel intensities to colors
volumeColor = vtk.vtkColorTransferFunction()
volumeColor.AddRGBPoint(0, 0.0, 0.0, 0.0)
volumeColor.AddRGBPoint(500, 1.0, 0.5, 0.3)
volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)

# Scalar opacity transfer function for controlling the opacity of tissue types
volumeScalarOpacity = vtk.vtkPiecewiseFunction()
volumeScalarOpacity.AddPoint(0, 0.0)
volumeScalarOpacity.AddPoint(500, 0.15)
volumeScalarOpacity.AddPoint(1000, 0.15)
volumeScalarOpacity.AddPoint(1150, 0.85)

# Gradient opacity function for enhancing volume boundaries
volumeGradientOpacity = vtk.vtkPiecewiseFunction()
volumeGradientOpacity.AddPoint(0, 0.0)
volumeGradientOpacity.AddPoint(90, 0.5)
volumeGradientOpacity.AddPoint(100, 1.0)

# Volume property to set color and opacity functions
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(volumeColor)
volumeProperty.SetScalarOpacity(volumeScalarOpacity)
volumeProperty.SetGradientOpacity(volumeGradientOpacity)
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.ShadeOn()
volumeProperty.SetAmbient(0.4)
volumeProperty.SetDiffuse(0.6)
volumeProperty.SetSpecular(0.2)

# Volume object to control position and orientation
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# Add volume to renderer
ren.AddViewProp(volume)

# Set initial view of the volume
camera = ren.GetActiveCamera()
c = volume.GetCenter()
camera.SetFocalPoint(c[0], c[1], c[2])
camera.SetPosition(c[0] + 400, c[1], c[2])
camera.SetViewUp(0, 0, -1)

# Increase the size of the render window
renWin.SetSize(1000, 1000)

# Add ROI Widget to the scene
roi_widget = add_roi_widget(ren, iren, volumeMapper, renWin)
roi_widget.On()

# Create a vtkSliderWidget for opacity control
opacityWidget = vtk.vtkSliderWidget()
opacityWidget.SetInteractor(iren)
sliderRepOpacity = vtk.vtkSliderRepresentation2D()

# Set opacity slider properties
sliderRepOpacity.SetValue(volumeScalarOpacity.GetValue(500))  # Initialize slider with default opacity value
sliderRepOpacity.SetTitleText("Opacity")
sliderRepOpacity.SetMinimumValue(0.0)
sliderRepOpacity.SetMaximumValue(1.0)
sliderRepOpacity.GetSliderProperty().SetColor(1, 0, 0)  # Slider color
sliderRepOpacity.GetTubeProperty().SetColor(1, 1, 1)   # Tube color

# Set title text properties
titleTextPropertyOpacity = sliderRepOpacity.GetTitleProperty()
titleTextPropertyOpacity.SetColor(1, 0, 0)  # Title color

# Set slider position to top-left corner
sliderRepOpacity.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepOpacity.GetPoint1Coordinate().SetValue(0.05, 0.85)
sliderRepOpacity.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepOpacity.GetPoint2Coordinate().SetValue(0.3, 0.85)

opacityWidget.SetRepresentation(sliderRepOpacity)

# Callback function for opacity slider interaction
def onOpacityChanged(widget, event):
    value = widget.GetRepresentation().GetValue()
    volumeScalarOpacity.RemoveAllPoints()
    volumeScalarOpacity.AddPoint(0, 0.0)
    volumeScalarOpacity.AddPoint(500, value)
    volumeScalarOpacity.AddPoint(1000, value)
    volumeScalarOpacity.AddPoint(1150, 0.85)
    renWin.Render()

opacityWidget.AddObserver(vtk.vtkCommand.InteractionEvent, onOpacityChanged)

# Create vtkSliderWidgets for RGB color control
sliderRepRed = vtk.vtkSliderRepresentation2D()
sliderRepRed.SetMinimumValue(0.0)
sliderRepRed.SetMaximumValue(1.0)
sliderRepRed.SetValue(volumeColor.GetRedValue(500))  # Initialize slider with default color value for red channel
sliderRepRed.SetTitleText("Red")
sliderRepRed.GetSliderProperty().SetColor(1, 0, 0)  # Slider color
sliderRepRed.GetTubeProperty().SetColor(1, 1, 1)   # Tube color

# Set title text properties
titleTextPropertyRed = sliderRepRed.GetTitleProperty()
titleTextPropertyRed.SetColor(1, 0, 0)  # Title color

# Set slider position to bottom-left corner
sliderRepRed.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepRed.GetPoint1Coordinate().SetValue(0.7, 0.1)
sliderRepRed.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepRed.GetPoint2Coordinate().SetValue(0.95, 0.1)

# Callback function for red channel slider interaction
def onRedChanged(widget, event):
    value = widget.GetRepresentation().GetValue()
    updateColorFunction(value, sliderRepGreen.GetValue(), sliderRepBlue.GetValue())  # Update red channel (index 0)

def updateColorFunction(red, green, blue):
    # Update color transfer function based on slider values
    volumeColor.RemoveAllPoints()
    volumeColor.AddRGBPoint(0, 0.0, 0.0, 0.0)
    volumeColor.AddRGBPoint(500, red, green, blue)
    volumeColor.AddRGBPoint(1000, red, green, blue)
    volumeColor.AddRGBPoint(1150, red, green, blue)
    renWin.Render()

sliderRepGreen = vtk.vtkSliderRepresentation2D()
sliderRepGreen.SetMinimumValue(0.0)
sliderRepGreen.SetMaximumValue(1.0)
sliderRepGreen.SetValue(volumeColor.GetGreenValue(500))  # Initialize slider with default color value for green channel
sliderRepGreen.SetTitleText("Green")
sliderRepGreen.GetSliderProperty().SetColor(0, 1, 0)  # Slider color
sliderRepGreen.GetTubeProperty().SetColor(1, 1, 1)   # Tube color

# Set title text properties
titleTextPropertyGreen = sliderRepGreen.GetTitleProperty()
titleTextPropertyGreen.SetColor(0, 1, 0)  # Title color

# Set slider position to bottom-left corner
sliderRepGreen.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepGreen.GetPoint1Coordinate().SetValue(0.4, 0.1)
sliderRepGreen.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepGreen.GetPoint2Coordinate().SetValue(0.65, 0.1)

# Callback function for green channel slider interaction
def onGreenChanged(widget, event):
    value = widget.GetRepresentation().GetValue()
    updateColorFunction(sliderRepRed.GetValue(), value, sliderRepBlue.GetValue())  # Update green channel (index 1)

sliderRepBlue = vtk.vtkSliderRepresentation2D()
sliderRepBlue.SetMinimumValue(0.0)
sliderRepBlue.SetMaximumValue(1.0)
sliderRepBlue.SetValue(volumeColor.GetBlueValue(500))  # Initialize slider with default color value for blue channel
sliderRepBlue.SetTitleText("Blue")
sliderRepBlue.GetSliderProperty().SetColor(0, 0, 1)  # Slider color
sliderRepBlue.GetTubeProperty().SetColor(1, 1, 1)   # Tube color

# Set title text properties
titleTextPropertyBlue = sliderRepBlue.GetTitleProperty()
titleTextPropertyBlue.SetColor(0, 0, 1)  # Title color

# Set slider position to bottom-left corner
sliderRepBlue.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepBlue.GetPoint1Coordinate().SetValue(0.05, 0.1)
sliderRepBlue.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepBlue.GetPoint2Coordinate().SetValue(0.3, 0.1)

# Callback function for blue channel slider interaction
def onBlueChanged(widget, event):
    value = widget.GetRepresentation().GetValue()
    updateColorFunction(sliderRepRed.GetValue(), sliderRepGreen.GetValue(), value)  # Update blue channel (index 2)

# Callback function for opacity slider interaction
def onDensityChanged(widget, event):
    value = widget.GetRepresentation().GetValue()
    volumeScalarOpacity.RemoveAllPoints()
    volumeScalarOpacity.AddPoint(0, 0.0)
    volumeScalarOpacity.AddPoint(500, value)
    volumeScalarOpacity.AddPoint(1000, value)
    volumeScalarOpacity.AddPoint(1150, 0.85)
    renWin.Render()

opacityWidget.AddObserver(vtk.vtkCommand.InteractionEvent, onOpacityChanged)
sliderRedWidget = vtk.vtkSliderWidget()
sliderRedWidget.SetInteractor(iren)
sliderRedWidget.SetRepresentation(sliderRepRed)
sliderRedWidget.AddObserver(vtk.vtkCommand.InteractionEvent, onRedChanged)

sliderGreenWidget = vtk.vtkSliderWidget()
sliderGreenWidget.SetInteractor(iren)
sliderGreenWidget.SetRepresentation(sliderRepGreen)
sliderGreenWidget.AddObserver(vtk.vtkCommand.InteractionEvent, onGreenChanged)

sliderBlueWidget = vtk.vtkSliderWidget()
sliderBlueWidget.SetInteractor(iren)
sliderBlueWidget.SetRepresentation(sliderRepBlue)
sliderBlueWidget.AddObserver(vtk.vtkCommand.InteractionEvent, onBlueChanged)

densityWidget = vtk.vtkSliderWidget()
densityWidget.SetInteractor(iren)
densityWidget.AddObserver(vtk.vtkCommand.InteractionEvent, onDensityChanged)

# Start interaction
iren.Initialize()
renWin.Render()
opacityWidget.On()
sliderRedWidget.On()
sliderGreenWidget.On()
sliderBlueWidget.On()
densityWidget.On()
iren.Start()
