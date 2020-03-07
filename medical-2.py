#!/usr/bin/env python

"""
"""

import vtk


def main():
    colors = vtk.vtkNamedColors()

    filename = get_program_parameters()

    colors.SetColor("SkinColor", [255, 125, 64, 255])
    colors.SetColor("BkgColor", [51, 77, 102, 255])

    # Create the renderer, the render window, and the interactor. The renderer
    # draws into the render window, the interactor enables mouse- and
    # keyboard-based interaction with the data within the render window.
    #
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    # The following reader is used to read a series of 2D slices (images)
    # that compose the volume. The slice dimensions are set, and the
    # pixel spacing. The data Endianness must also be specified. The reader
    # uses the FilePrefix in combination with the slice number to construct
    # filenames using the format FilePrefix.%d. (In this case the FilePrefix
    # is the root name of the file: quarter.)
    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(filename)

    # An isosurface, or contour value of 500 is known to correspond to the
    # skin of the patient.
    # The triangle stripper is used to create triangle strips from the
    # isosurface these render much faster on many systems.
    skin_extractor = vtk.vtkMarchingCubes()
    skin_extractor.SetInputConnection(reader.GetOutputPort())
    skin_extractor.SetValue(0, 500)

    skin_stripper = vtk.vtkStripper()
    skin_stripper.SetInputConnection(skin_extractor.GetOutputPort())

    skin_mapper = vtk.vtkPolyDataMapper()
    skin_mapper.SetInputConnection(skin_stripper.GetOutputPort())
    skin_mapper.ScalarVisibilityOff()

    skin = vtk.vtkActor()
    skin.SetMapper(skin_mapper)
    skin.GetProperty().SetDiffuseColor(colors.GetColor3d("SkinColor"))
    skin.GetProperty().SetSpecular(.3)
    skin.GetProperty().SetSpecularPower(20)
    skin.GetProperty().SetOpacity(.5)

    # An isosurface, or contour value of 1150 is known to correspond to the
    # bone of the patient.
    # The triangle stripper is used to create triangle strips from the
    # isosurface these render much faster on may systems.
    bone_extractor = vtk.vtkMarchingCubes()
    bone_extractor.SetInputConnection(reader.GetOutputPort())
    bone_extractor.SetValue(0, 1150)

    bone_stripper = vtk.vtkStripper()
    bone_stripper.SetInputConnection(bone_extractor.GetOutputPort())

    bone_mapper = vtk.vtkPolyDataMapper()
    bone_mapper.SetInputConnection(bone_stripper.GetOutputPort())
    bone_mapper.ScalarVisibilityOff()

    bone = vtk.vtkActor()
    bone.SetMapper(bone_mapper)
    bone.GetProperty().SetDiffuseColor(colors.GetColor3d("Ivory"))

    # An outline provides context around the data.
    #
    outline_data = vtk.vtkOutlineFilter()
    outline_data.SetInputConnection(reader.GetOutputPort())

    map_outline = vtk.vtkPolyDataMapper()
    map_outline.SetInputConnection(outline_data.GetOutputPort())

    outline = vtk.vtkActor()
    outline.SetMapper(map_outline)
    outline.GetProperty().SetColor(colors.GetColor3d("Black"))

    # It is convenient to create an initial view of the data. The FocalPoint
    # and Position form a vector direction. Later on (ResetCamera() method)
    # this vector is used to position the camera to look at the data in
    # this direction.
    camera = vtk.vtkCamera()
    camera.SetViewUp(0, 0, -1)
    camera.SetPosition(0, -1, 0)
    camera.SetFocalPoint(0, 0, 0)
    camera.ComputeViewPlaneNormal()
    camera.Azimuth(30.0)
    camera.Elevation(30.0)

    # Actors are added to the renderer. An initial camera view is created.
    # The Dolly() method moves the camera towards the FocalPoint,
    # thereby enlarging the image.
    renderer.AddActor(outline)
    renderer.AddActor(skin)
    renderer.AddActor(bone)
    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()
    camera.Dolly(1.5)

    # Set a background color for the renderer and set the size of the
    # render window (expressed in pixels).
    renderer.SetBackground(colors.GetColor3d("BkgColor"))
    render_window.SetSize(640, 480)

    # Note that when camera movement occurs (as it does in the Dolly()
    # method), the clipping planes often need adjusting. Clipping planes
    # consist of two planes: near and far along the view direction. The
    # near plane clips out objects in front of the plane the far plane
    # clips out objects behind the plane. This way only what is drawn
    # between the planes is actually rendered.
    renderer.ResetCameraClippingRange()

    # Initialize the event loop and then start it.
    render_interactor.Initialize()
    render_interactor.Start()


def get_program_parameters():
    import argparse
    description = 'The skin and bone is extracted from a CT dataset of the head.'
    epilogue = '''
    Derived from VTK/Examples/Cxx/Medical2.cxx
    This example reads a volume dataset, extracts two isosurfaces that
     represent the skin and bone, and then displays it.
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='FullHead.mhd.')
    args = parser.parse_args()
    return args.filename


if __name__ == '__main__':
    main()
