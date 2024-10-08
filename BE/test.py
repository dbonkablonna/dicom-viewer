import vtk
import math
import numpy
import slicer
from vtkmodules.util.misc import vtkGetDataRoot

VTK_DATA_ROOT = vtkGetDataRoot()
DEBUG_MODE = 0

def findDistanceBetweenTwoPoints(startPoint, endPoint):
    dist = 0.0
    for i in range(0, 3):
        dist += math.pow((endPoint[i] - startPoint[i]), 2)
    return math.sqrt(dist)

def findAngleBetweenTwoPoints(startPoint, endPoint):
    delY = endPoint[1] - startPoint[1]
    delX = endPoint[0] - startPoint[0]
    if delX == 0 and delY >= 0:
        return math.degrees(numpy.arctan(-float('inf')))
    elif delX == 0 and delY < 0:
        return math.degrees(numpy.arctan(float('inf')))
    else:
        return math.degrees(numpy.arctan(delY / delX))

def computeMPR(endPoints, plane, planeAngle):
    numberOfSlices = len(endPoints) - 1
    points = [[0 for x in range(3)] for x in range(len(endPoints) - 1)]
    angle = [0] * numberOfSlices
    extentLength = [[0 for x in range(len(endPoints))] for x in range(len(endPoints))]
    setLocation = [0] * numberOfSlices
    distance = [0] * numberOfSlices

    print("-", planeAngle)

    for i in range(0, numberOfSlices):
        for j in range(0, 3):
            points[i][j] = (endPoints[i][j] + endPoints[i + 1][j]) * 0.5

            if DEBUG_MODE:
                print("Mid Point:: [", i, ",],[", j, "] :: ", points[i][j])

    for i in range(0, numberOfSlices):
        distance[i] = findDistanceBetweenTwoPoints(endPoints[i], endPoints[i + 1])
        angle[i] = findAngleBetweenTwoPoints(endPoints[i], endPoints[i + 1])

        if DEBUG_MODE:
            print("For the points:: ", endPoints[i], " and ", endPoints[i + 1])
            print("Distance: ", distance[i], "Angle: ", angle[i])

    temp = -40

    for i in range(0, numberOfSlices):
        extentLength[i][0] = distance[i]
        extentLength[i][1] = 94
        temp += distance[i]
        setLocation[i] = temp

    actor = [None] * numberOfSlices  # Initialize actor list

    for i in range(0, numberOfSlices):
        aslice = vtk.vtkImageReslice()
        aslice.SetInputConnection(reader.GetOutputPort())
        aslice.SetOutputDimensionality(2)
        aslice.SetResliceAxesOrigin(
            points[i][0] * aslice.GetOutput().GetSpacing()[0],
            points[i][1] * aslice.GetOutput().GetSpacing()[1],
            points[i][2] * aslice.GetOutput().GetSpacing()[2])

        aslice.SetResliceAxesDirectionCosines(1, 0, 0,
                                              0, math.cos(math.radians(float(planeAngle))),
                                              -math.sin(math.radians(float(planeAngle))),
                                              0, math.sin(math.radians(float(planeAngle))),
                                              math.cos(math.radians(float(planeAngle))))
        aslice.SetInterpolationModeToLinear()

        transform = vtk.vtkTransform()
        transform.Translate(center[0], center[1], center[2])
        transform.RotateZ(angle[i])
        transform.Translate(-center[0], -center[1], -center[2])

        transform.Translate(center[0] - points[i][0], center[1] - points[i][1], center[2] - points[i][2])

        aslice.SetResliceTransform(transform)
        aslice.SetOutputExtent(0, int(extentLength[i][0]), 0, int(extentLength[i][1]), 0, 0)

        color = vtk.vtkImageMapToColors()
        color.SetLookupTable(table)
        color.SetInputConnection(aslice.GetOutputPort())

        # Create a vtkImageMapper3D object
        mapper = vtk.vtkOpenGLImageSliceMapper()
        mapper.SetInputConnection(color.GetOutputPort())

        # Set the mapper for the actor
        actor[i] = vtk.vtkImageActor()
        actor[i].SetMapper(mapper)
        actor[i].SetPosition(setLocation[i], 0, 0)

    return actor

# Initialization
worldPicker = vtk.vtkWorldPointPicker()
clickPointsList = []
renderer = vtk.vtkRenderer()
mpv_renderer = range(4)

# Start by loading some data
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(slicer.dicom_directory)

# Không cần thiết lập DataExtent và DataSpacing vì DICOM tự động xác định các thông số này từ các files.
reader.Update()

reader.SetDataScalarTypeToUnsignedShort()
reader.UpdateWholeExtent()

# Calculate the center of the volume
(xSpacing, ySpacing, zSpacing) = reader.GetOutput().GetSpacing()
(x0, y0, z0) = reader.GetOutput().GetOrigin()
(xMin, xMax, yMin, yMax, zMin, zMax) = reader.GetOutput().GetExtent()

center = [x0 + xSpacing * 0.5 * (xMin + xMax),
          y0 + ySpacing * 0.5 * (yMin + yMax),
          z0 + zSpacing * 0.5 * (zMin + zMax)]

# Basic Planes
axial = vtk.vtkMatrix4x4()
axial.DeepCopy((1, 0, 0, center[0],
                0, 1, 0, center[1],
                0, 0, 1, center[2],
                0, 0, 0, 1))

coronal = vtk.vtkMatrix4x4()
coronal.DeepCopy((1, 0, 0, center[0],
                  0, 0, 1, center[1],
                  0, -1, 0, center[2],
                  0, 0, 0, 1))

sagittal = vtk.vtkMatrix4x4()
sagittal.DeepCopy((0, 0, -1, center[0],
                   1, 0, 0, center[1],
                   0, -1, 0, center[2],
                   0, 0, 0, 1))

# Oblique slice
obliqueSlice = vtk.vtkImageReslice()
obliqueSlice.SetInputConnection(reader.GetOutputPort())
obliqueSlice.SetOutputDimensionality(2)

# Extract a slice in the desired orientation (axial)
reslice_axial = vtk.vtkImageReslice()
reslice_axial.SetInputConnection(reader.GetOutputPort())
reslice_axial.SetOutputDimensionality(2)
reslice_axial.SetResliceAxes(axial)
reslice_axial.SetInterpolationModeToLinear()

# Extract a slice in the desired orientation (coronal)
reslice_coronal = vtk.vtkImageReslice()
reslice_coronal.SetInputConnection(reader.GetOutputPort())
reslice_coronal.SetOutputDimensionality(2)
reslice_coronal.SetResliceAxes(coronal)
reslice_coronal.SetInterpolationModeToLinear()

# Extract a slice in the desired orientation (sagittal)
reslice_sagittal = vtk.vtkImageReslice()
reslice_sagittal.SetInputConnection(reader.GetOutputPort())
reslice_sagittal.SetOutputDimensionality(2)
reslice_sagittal.SetResliceAxes(sagittal)
reslice_sagittal.SetInterpolationModeToLinear()

# Create a greyscale lookup table
table = vtk.vtkLookupTable()
table.SetRange(0, 2000)  # image intensity range
table.SetValueRange(0.0, 1.0)  # from black to white
table.SetSaturationRange(0.0, 0)
table.SetRampToLinear()
table.Build()

# Map the image through the lookup table (axial)
color_axial = vtk.vtkImageMapToColors()
color_axial.SetLookupTable(table)
color_axial.SetInputConnection(reslice_axial.GetOutputPort())

# Display the image (axial)
actor_axial = vtk.vtkImageActor()
actor_axial.GetMapper().SetInputConnection(color_axial.GetOutputPort())

# Map the image through the lookup table (coronal)
color_coronal = vtk.vtkImageMapToColors()
color_coronal.SetLookupTable(table)
color_coronal.SetInputConnection(reslice_coronal.GetOutputPort())

# Display the image (coronal)
actor_coronal = vtk.vtkImageActor()
actor_coronal.GetMapper().SetInputConnection(color_coronal.GetOutputPort())

# Map the image through the lookup table (sagittal)
color_sagittal = vtk.vtkImageMapToColors()
color_sagittal.SetLookupTable(table)
color_sagittal.SetInputConnection(reslice_sagittal.GetOutputPort())

# Display the image (sagittal)
actor_sagittal = vtk.vtkImageActor()
actor_sagittal.GetMapper().SetInputConnection(color_sagittal.GetOutputPort())

# Oblique Slice
obliqueSlice.SetResliceAxesOrigin(center[0], center[1], center[2])
obliqueSlice.SetResliceAxesDirectionCosines(1, 0, 0,
                                             0, math.cos(math.radians(45)), -math.sin(math.radians(45)),
                                             0, math.sin(math.radians(45)), math.cos(math.radians(45)))
obliqueSlice.SetInterpolationModeToLinear()

color_oblique = vtk.vtkImageMapToColors()
color_oblique.SetLookupTable(table)
color_oblique.SetInputConnection(obliqueSlice.GetOutputPort())

actor_oblique = vtk.vtkImageActor()
actor_oblique.GetMapper().SetInputConnection(color_oblique.GetOutputPort())

# Create a renderer for multi-view
rw = vtk.vtkRenderWindow()
interactorStyle = vtk.vtkInteractorStyleImage()
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(interactorStyle)
rw.SetInteractor(interactor)

# Callbacks
actions = {}
actions["Slicing"] = 0
mode = 4

def ButtonCallback(obj, event):
    if event == "LeftButtonPressEvent":
        actions["Slicing"] = 1
    else:
        actions["Slicing"] = 0
    x, y = obj.GetInteractor().GetEventPosition()

    global mode
    if x < 300 and y < 300:
        mode = 0  # "SAGITTAL"
    elif x < 600 and y < 300:
        mode = 1  # "AXIAL"
    elif x > 300 and y > 300:
        mode = 3  # "CORONAL"
    else:
        mode = 4

def MouseMoveCallback(obj, event):
    (lastX, lastY) = interactor.GetLastEventPosition()
    (mouseX, mouseY) = interactor.GetEventPosition()
    if actions["Slicing"] == 1:
        deltaY = mouseY - lastY

        if deltaY > 0:
            deltaY = 5
        else:
            deltaY = -5

        if mode == 3:  # "CORONAL":
            reslice_coronal.Update()
            sliceSpacing = reslice_coronal.GetOutput().GetSpacing()[2]
            matrix = reslice_coronal.GetResliceAxes()
        elif mode == 1:  # "AXIAL":
            reslice_axial.Update()
            sliceSpacing = reslice_axial.GetOutput().GetSpacing()[2]
            matrix = reslice_axial.GetResliceAxes()
        elif mode == 0:  # "SAGITTAL":
            reslice_sagittal.Update()
            sliceSpacing = reslice_sagittal.GetOutput().GetSpacing()[2]
            matrix = reslice_sagittal.GetResliceAxes()
        else:
            return

        center = matrix.MultiplyPoint((0, 0, sliceSpacing * deltaY, 1))
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])
        rw.Render()
        rw.Render()
    else:
        interactorStyle.OnMouseMove()

def LeftButtonPressEvent(obj, event):
    x, y = obj.GetInteractor().GetEventPosition()
    worldPicker.Pick(x, y, 0, mpv_renderer[1])
    worldPos = worldPicker.GetPickPosition()
    singleClickedPoint = [worldPos[0] + center[0], worldPos[1] + center[1], worldPos[2] + center[2]]

    clickPointsList.append(singleClickedPoint)

    displayClickPoints(clickPointsList)

    return

def displayClickPoints(clickPoints):
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()
    polygon = vtk.vtkPolyData()
    polygonMapper = vtk.vtkPolyDataMapper()
    polygonActor = vtk.vtkActor()

    points.SetNumberOfPoints(4)
    points.SetPoint(0, 0.0, -1.0, 0.0)
    points.SetPoint(1, -0.7, -0.5, 0.0)
    points.SetPoint(2, 0.7, 0.5, 0.0)
    points.SetPoint(3, 0.0, -1.0, 0.0)

    lines.InsertNextCell(4)
    lines.InsertCellPoint(0)
    lines.InsertCellPoint(1)
    lines.InsertCellPoint(2)
    lines.InsertCellPoint(3)

    polygon.SetPoints(points)
    polygon.SetLines(lines)

    polygonMapper.SetInputData(polygon)
    polygonActor.SetMapper(polygonMapper)

    mpv_renderer[1].ResetCamera()
    mpv_renderer[1].AddActor(polygonActor)
    rw.Render()

def KeyPressEvent(obj, event):
    global clickPointsList, mode

    keyCode = obj.GetKeyCode()

    if keyCode in ['r', 'R']:  # Render_Mode

        print("r pressed")
        actors = computeMPR(clickPointsList, "Axial", 90)
        renderer.ResetCamera()

        for i in range(len(actors)):
            renderer.AddActor2D(actors[i])

        rw.AddRenderer(renderer)
        rw.Render()


    if keyCode in ['c', 'C']:  # ViewPort Clear Mode & Reset
        print("c pressed")
        for i in range(len(clickPointsList) - 1):
            renderer.RemoveActor2D(actors[i])

        rw.AddRenderer(renderer)
        rw.Render()

        del clickPointsList[:]

# Call back registration
interactorStyle.AddObserver("MouseMoveEvent", MouseMoveCallback)
interactorStyle.AddObserver("LeftButtonPressEvent", ButtonCallback)
interactorStyle.AddObserver("LeftButtonReleaseEvent", ButtonCallback)
interactorStyle.AddObserver("LeftButtonPressEvent", LeftButtonPressEvent)
interactor.AddObserver("KeyPressEvent", KeyPressEvent)

# Define viewport ranges
xmins = [0, .5, 0, .5]
xmaxs = [0.5, 1, 0.5, 1]
ymins = [0, 0, .5, .5]
ymaxs = [0.5, 0.5, 1, 1]

# Create a list of vtkRenderer objects
mpv_renderer = [vtk.vtkRenderer() for _ in range(4)]
for i in range(len(mpv_renderer)):
    mpv_renderer[i].SetViewport(xmins[i], ymins[i], xmaxs[i], ymaxs[i])

mpv_renderer[1].SetUseDepthPeeling(1)
mpv_renderer[1].SetOcclusionRatio(0.5)

mpv_renderer[2].AddViewProp(slicer.volume)
camera = mpv_renderer[2].GetActiveCamera()
c = slicer.volume.GetCenter()
camera.SetFocalPoint(c[0], c[1], c[2])
camera.SetPosition(c[0] + 400, c[1], c[2])
camera.SetViewUp(0, 0, -1)

displayClickPoints(clickPointsList)
mpv_renderer[1].AddActor2D(actor_axial)
mpv_renderer[3].AddActor2D(actor_coronal)
mpv_renderer[0].AddActor2D(actor_sagittal)

for i in range(0, 4):
    rw.AddRenderer(mpv_renderer[i])


rw.SetWindowName("Multi Planar Viewer Window")
rw.SetSize(1200, 1200)
rw.Render()

interactor.Start()
