# app.py (backend)
from pathlib import Path

from flask import Flask, request, send_file
import vtk
import os
from io import BytesIO

app = Flask(__name__)


# Function to load DICOM directory
def load_dicom_directory(directory):
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(directory)
    reader.Update()
    return reader


# Global variables for storing VTK objects
volume = None
volumeProperty = None
renWin = None


@app.route('/render', methods=['POST'])
def render_image():
    global volume, volumeProperty, renWin

    # # Get the folder path
    # directory = request.files['folder'].filename
    # folder = request.form['folder']
    # print(f"Received folder: {folder}")
    #
    # folder_path = Path(folder).resolve()  # Chuyển thành đường dẫn tuyệt đối
    #
    # # In ra đường dẫn tuyệt đối để kiểm tra
    # print(f"Using absolute path: {folder_path}")


    # # Load the DICOM data
    # reader = vtk.vtkDICOMImageReader()
    # reader.SetDirectoryName(str(folder_path))  # Sử dụng đường dẫn tuyệt đối
    # reader.Update()

    # Get the folder path
    directory = request.files['folder'].filename

    # Load the DICOM data
    reader = load_dicom_directory(directory)
    reader.Update()



    # Create the volume mapper and other VTK objects if not already created
    if not volume:
        volumeMapper = vtk.vtkSmartVolumeMapper()
        volumeMapper.SetInputConnection(reader.GetOutputPort())

        volumeColor = vtk.vtkColorTransferFunction()
        volumeColor.AddRGBPoint(0, 0.0, 0.0, 0.0)
        volumeColor.AddRGBPoint(500, 1.0, 0.5, 0.3)
        volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
        volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)

        volumeScalarOpacity = vtk.vtkPiecewiseFunction()
        volumeScalarOpacity.AddPoint(0, 0.0)
        volumeScalarOpacity.AddPoint(500, 0.15)
        volumeScalarOpacity.AddPoint(1000, 0.15)
        volumeScalarOpacity.AddPoint(1150, 0.85)

        volumeGradientOpacity = vtk.vtkPiecewiseFunction()
        volumeGradientOpacity.AddPoint(0, 0.0)
        volumeGradientOpacity.AddPoint(90, 0.5)
        volumeGradientOpacity.AddPoint(100, 1.0)

        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(volumeColor)
        volumeProperty.SetScalarOpacity(volumeScalarOpacity)
        volumeProperty.SetGradientOpacity(volumeGradientOpacity)
        volumeProperty.SetInterpolationTypeToLinear()
        volumeProperty.ShadeOn()
        volumeProperty.SetAmbient(0.4)
        volumeProperty.SetDiffuse(0.6)
        volumeProperty.SetSpecular(0.2)

        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volumeProperty)

        ren = vtk.vtkRenderer()
        ren.AddViewProp(volume)

        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)
        renWin.SetSize(1000, 1000)

        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

    # Capture the image
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renWin)
    w2if.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetInputConnection(w2if.GetOutputPort())

    buffer = BytesIO()
    writer.SetWriteToMemory(True)
    writer.WriteToBuffer(buffer)
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')


@app.route('/update-sliders', methods=['POST'])
def update_sliders():
    global volumeProperty

    data = request.json
    opacity = data.get('opacity', 100) / 100.0
    red = data.get('red', 1.0)
    green = data.get('green', 1.0)
    blue = data.get('blue', 1.0)
    density = data.get('density', 1.0)

    # Update volume properties based on sliders
    volumeProperty.GetScalarOpacity().RemoveAllPoints()
    volumeProperty.GetScalarOpacity().AddPoint(0, 0.0)
    volumeProperty.GetScalarOpacity().AddPoint(500, opacity)
    volumeProperty.GetScalarOpacity().AddPoint(1000, opacity)
    volumeProperty.GetScalarOpacity().AddPoint(1150, 0.85)

    volumeProperty.GetColor().RemoveAllPoints()
    volumeProperty.GetColor().AddRGBPoint(0, 0.0, 0.0, 0.0)
    volumeProperty.GetColor().AddRGBPoint(500, red, green, blue)
    volumeProperty.GetColor().AddRGBPoint(1000, red, green, blue)
    volumeProperty.GetColor().AddRGBPoint(1150, red, green, blue)

    volumeProperty.GetGradientOpacity().RemoveAllPoints()
    volumeProperty.GetGradientOpacity().AddPoint(0, 0.0)
    volumeProperty.GetGradientOpacity().AddPoint(90, density)
    volumeProperty.GetGradientOpacity().AddPoint(100, density)

    renWin.Render()

    return "Updated", 200


if __name__ == '__main__':
    app.run(debug=True)
