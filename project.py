#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk
from typing import List

"""
Visualization Assignment #3

Write a program to visualize a uniform grid. Specify a dimension of 26x26x26 and an xyzv 
ranges of [0.0,1.0][0.0,1.0][0.0,1.0][0.0,1.0]. Use your favorite math functions 
to generate a scalar field. Design your own color table. Your window should have four 
views displaying the following:

1. Isosurfaces
2. Cutting planes
3. Contour lines
4. In the display, briefly document what techniques and parameters that you have used to 
   create the visualization.

Take a screen shot of your display.
"""


def create_text(text: str, color: vtk.vtkColor3d) -> vtk.vtkActor:
    """
    Creates a text actor with the given text in the given color.
    Adapted from 
    https://lorensen.github.io/VTKExamples/site/Python/Visualization/VectorText/

    :param text: The text to display
    :param color: The color the text should be.
    :return: a vtk actor with the given text.
    """
    text_source = vtk.vtkVectorText()
    text_source.SetText(text)
    text_source.Update()

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(text_source.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)

    return actor


def create_isosurface(func: vtk.vtkSampleFunction,
                      lut: vtk.vtkLookupTable,
                      number_of_contours=5) -> vtk.vtkActor:
    """
    Creates an Isosurface using the given function and applies it to the given actor
    with the given number of contours.
    Adapted from
    https://lorensen.github.io/VTKExamples/site/Python/Visualization/QuadricVisualization/

    :param func: a vtkSampleFunction
    :param number_of_contours: [default: 5] The number of contours to draw
    :return: the actor into which the function will be applied.

    """
    actor = vtk.vtkActor()
    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(func.GetOutputPort())
    ranges = [1.0, 6.0]
    contour.GenerateValues(number_of_contours, ranges)

    contour_mapper = vtk.vtkPolyDataMapper()
    contour_mapper.SetInputConnection(contour.GetOutputPort())
    contour_mapper.SetScalarRange(0, 7)
    contour_mapper.SetLookupTable(lut)

    actor.SetMapper(contour_mapper)

    return actor


def create_planes(func: vtk.vtkSampleFunction,
                  number_of_planes: int) -> vtk.vtkActor:
    """
    Creates a number of planes that show a slice of the data at that slice.
    Adapted from
    https://lorensen.github.io/VTKExamples/site/Python/Visualization/QuadricVisualization/
    
    :param func: a vtkSampleFunction
    :param number_of_planes: the number of planes to add to the actor.
    :return: the actor to which the planes will be added.
    """
    actor = vtk.vtkActor()
    append = vtk.vtkAppendFilter()

    dimensions = func.GetSampleDimensions()
    slice_increment = (dimensions[2] - 1) // (number_of_planes + 1)
    slice_num = -4
    for i in range(0, number_of_planes):
        extract = vtk.vtkExtractVOI()
        extract.SetInputConnection(func.GetOutputPort())
        extract.SetVOI(0, dimensions[0] - 1,
                       0, dimensions[1] - 1,
                       slice_num + slice_increment,
                       slice_num + slice_increment)
        append.AddInputConnection(extract.GetOutputPort())
        slice_num += slice_increment
    append.Update()

    planes_mapper = vtk.vtkDataSetMapper()
    planes_mapper.SetInputConnection(append.GetOutputPort())
    planes_mapper.SetScalarRange(0, 7)

    actor.SetMapper(planes_mapper)
    actor.GetProperty().SetAmbient(1.)

    return actor


def create_contours(func: vtk.vtkSampleFunction,
                    number_of_planes: int, number_of_contours: int) -> vtk.vtkActor:
    """
    Create a number of planes that show the contours at the slices those planes
    intersect
    Adapted from
    https://lorensen.github.io/VTKExamples/site/Python/Visualization/QuadricVisualization/

    :param func: a vtkSampleFunction
    :param number_of_planes: the number of planes to add to the actor.
    :param number_of_contours: the number of to generate values for.
    :return: the actor to which the planes will be added.
    """
    actor = vtk.vtkActor()
    append = vtk.vtkAppendFilter()

    dimensions = func.GetSampleDimensions()
    slice_increment = (dimensions[2] - 1) // (number_of_planes + 1)

    slice_num = -4
    for i in range(0, number_of_planes):
        extract = vtk.vtkExtractVOI()
        extract.SetInputConnection(func.GetOutputPort())
        extract.SetVOI(0, dimensions[0] - 1,
                       0, dimensions[1] - 1,
                       slice_num + slice_increment,
                       slice_num + slice_increment)
        ranges = [1.0, 6.0]
        contour = vtk.vtkContourFilter()
        contour.SetInputConnection(extract.GetOutputPort())
        contour.GenerateValues(number_of_contours, ranges)
        append.AddInputConnection(contour.GetOutputPort())
        slice_num += slice_increment
    append.Update()

    planes_mapper = vtk.vtkDataSetMapper()
    planes_mapper.SetInputConnection(append.GetOutputPort())
    planes_mapper.SetScalarRange(0, 7)

    actor.SetMapper(planes_mapper)
    actor.GetProperty().SetAmbient(1.)

    return actor


def create_outline(source: vtk.vtkSampleFunction) -> vtk.vtkActor:
    """
    Create an outline around the viewed actor
    Adapted from
    https://lorensen.github.io/VTKExamples/site/Python/Visualization/QuadricVisualization/

    :param source: The sample function
    :return: The actor to which the outline is to be applied
    """
    actor = vtk.vtkActor()
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(source.GetOutputPort())
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(outline.GetOutputPort())
    actor.SetMapper(mapper)

    return actor


def create_color_table(num_values: int) -> vtk.vtkLookupTable:
    """
    Create a CTF LUT
    Adapted from
    https://vtk.org/Wiki/VTK/Examples/Python/Visualization/AssignColorsCellFromLUT
    :param num_values: number of values
    :return: a lookup table
    """
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToDiverging()

    ctf.AddRGBPoint(0.0, 0, 117, 173)
    ctf.AddRGBPoint(0.5, 173, 0, 32)
    ctf.AddRGBPoint(1.0, 173, 142, 0)

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(num_values)
    lut.Build()

    for i in range(0, num_values):
        rgb = list(ctf.GetColor(float(i)/num_values)) + [1]
        lut.SetTableValue(i, rgb)

    return lut


def make_cell_data(num_values: int, lut: vtk.vtkLookupTable,
                   colors: vtk.vtkUnsignedCharArray):
    """

    :param num_values:
    :param lut:
    :param colors:
    :return:
    """
    for i in range(1, num_values):
        rgb = [0.0, 0.0, 0.0]
        lut.GetColor(float(i) / (num_values - 1), rgb)
        ucrgb = list(map(int, [x * 255 for x in rgb]))
        colors.InsertNextTuple3(ucrgb[0], ucrgb[1], ucrgb[2])


def create_viewport(x_min: float, x_max: float, y_min: float, y_max: float,
                    background_color: vtk.vtkColor3d, actors: List[vtk.vtkActor],
                    render_window: vtk.vtkRenderWindow, is_text=False):
    """
    Create a viewport with the given dimensions, background color, and actor
    Adapted from
    https://lorensen.github.io/VTKExamples/site/Python/Visualization/MultipleViewports/

    :type actors: list[vtk.vtkActor]
    :param x_min: The point on the x-axis to start the viewport
    :param x_max: The point on the x-axis to stop the viewport
    :param y_min: The point on the y-axis to start the viewport
    :param y_max: The point on the y-axis to stop the viewport
    :param background_color: The color the background in this viewport should be
    :param actors: The actors to display
    :param render_window: The render window that will get the new viewport
    :param is_text: should this be rendered as text?
    """
    renderer = vtk.vtkRenderer()
    renderer.SetViewport(x_min, y_min, x_max, y_max)

    for actor in actors:
        renderer.AddActor(actor)

    if not is_text:
        renderer.TwoSidedLightingOn()

        renderer.SetBackground(background_color)
        renderer.GetActiveCamera().SetPosition(0, -1, 0)
        renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
        renderer.GetActiveCamera().SetViewUp(0, 0, -1)
        renderer.ResetCamera()
        renderer.GetActiveCamera().Elevation(20)
        renderer.GetActiveCamera().Azimuth(10)
        renderer.GetActiveCamera().Dolly(1.2)
        renderer.ResetCameraClippingRange()
    else:
        renderer.ResetCamera()

    render_window.AddRenderer(renderer)


def main():
    """
    The entry-point to the program.
    Adapted from
    https://lorensen.github.io/VTKExamples/site/Python/Visualization/QuadricVisualization/
    """

    table_size = 7
    lut = create_color_table(table_size)

    render_window = vtk.vtkRenderWindow()
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    render_window.SetSize(1700, 900)

    # Text in the first viewport
    text = '''Edwin Sarver
Assignment #3
Visualization
    
    The following visualizations were created using VTK for Python.
    A quadric is generated with multiple layers. This is then sampled in a 
    50x50x50-cell cube. Then, the following visualizations are created:
    
        1) Isosurfaces
        2) Cutting Planes
        3) Contour Lines 
    
    A custom color-table was used to get the coloring at each isosurface value.
    An interactor was added because it is fun to watch the objects (and text) spin.
    '''
    text_color = vtk.vtkNamedColors().GetColor3d('White')
    text_actor = create_text(text, text_color)
    background_color = vtk.vtkNamedColors().GetColor3d('SlateGray')

    create_viewport(0.0, 0.5, 0.5, 1.0, background_color, [text_actor],
                    render_window, True)

    # Generate the function
    quadric = vtk.vtkQuadric()
    quadric.SetCoefficients(1, 2, 3, 0, 1, 0, 0, 0, 0, 0)

    sample = vtk.vtkSampleFunction()
    sample.SetSampleDimensions(50, 50, 50)
    sample.SetImplicitFunction(quadric)

    color_data = vtk.vtkUnsignedCharArray()
    color_data.SetName('colors')
    color_data.SetNumberOfComponents(3)
    make_cell_data(table_size, lut, color_data);

    sample.GetOutput().GetCellData().SetScalars(color_data)

    # Get the isosurface actors
    iso_actor = create_isosurface(sample, lut)
    iso_outline = create_outline(sample)

    create_viewport(0.5, 1.0, 0.5, 1.0, background_color,
                    [iso_actor, iso_outline], render_window)

    # Get the cutting plane actors
    planes_actor = create_planes(sample, 5)
    planes_outline = create_outline(sample)

    create_viewport(0.0, 0.5, 0.0, 0.5, background_color,
                    [planes_actor, planes_outline], render_window)

    # Get the contour actors
    contours_actor = create_contours(sample, 5, 15)
    contours_outline = create_outline(sample)

    create_viewport(0.5, 1.0, 0.0, 0.5, background_color,
                    [contours_actor, contours_outline], render_window)

    # Render everything
    render_window.Render()
    render_window.SetWindowName("Visualization Project #3")
    interactor.Start()


if __name__ == "__main__":
    main()
