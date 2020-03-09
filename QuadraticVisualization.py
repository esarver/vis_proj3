#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk

"""
Quadratic Visualization Demo from https://lorensen.github.io/VTKExamples/site/Python/Visualization/QuadricVisualization/
"""

def main():
    colors = vtk.vtkNamedColors()

    renderer = vtk.vtkRenderer()

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    render_window.SetSize(640, 480)

    #
    # Create surface of implicit function.
    #

    # Sample quadric function.
    quadric = vtk.vtkQuadric()
    quadric.SetCoefficients(1, 2, 3, 0, 1, 0, 0, 0, 0, 0)

    sample = vtk.vtkSampleFunction()
    sample.SetSampleDimensions(25, 25, 25)
    sample.SetImplicitFunction(quadric)

    iso_actor = vtk.vtkActor()
    create_isosurface(sample, iso_actor)
    outline_iso_actor = vtk.vtkActor()
    create_outline(sample, outline_iso_actor)

    planes_actor = vtk.vtkActor()
    create_planes(sample, planes_actor, 3)
    outline_planes_actor = vtk.vtkActor()
    create_outline(sample, outline_planes_actor)
    planes_actor.AddPosition(iso_actor.GetBounds()[0] * 2.0, 0, 0)
    outline_planes_actor.AddPosition(iso_actor.GetBounds()[0] * 2.0, 0, 0)

    contour_actor = vtk.vtkActor()
    create_contours(sample, contour_actor, 3, 15)
    outline_contour_actor = vtk.vtkActor()
    create_outline(sample, outline_contour_actor)
    contour_actor.AddPosition(iso_actor.GetBounds()[0] * 4.0, 0, 0)
    outline_contour_actor.AddPosition(iso_actor.GetBounds()[0] * 4.0, 0, 0)

    renderer.AddActor(planes_actor)
    renderer.AddActor(outline_planes_actor)
    renderer.AddActor(contour_actor)
    renderer.AddActor(outline_contour_actor)
    renderer.AddActor(iso_actor)
    renderer.AddActor(outline_iso_actor)

    renderer.TwoSidedLightingOn()

    renderer.SetBackground(colors.GetColor3d("SlateGray"))

    # Try to set camera to match figure on book
    renderer.GetActiveCamera().SetPosition(0, -1, 0)
    renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
    renderer.GetActiveCamera().SetViewUp(0, 0, -1)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Elevation(20)
    renderer.GetActiveCamera().Azimuth(10)
    renderer.GetActiveCamera().Dolly(1.2)
    renderer.ResetCameraClippingRange()

    render_window.SetSize(640, 480)
    render_window.Render()

    # interact with data
    interactor.Start()


def create_isosurface(func, actor, number_of_contours=5):
    # Generate implicit surface.
    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(func.GetOutputPort())
    ranges = [1.0, 6.0]
    contour.GenerateValues(number_of_contours, ranges)

    # Map contour
    contour_mapper = vtk.vtkPolyDataMapper()
    contour_mapper.SetInputConnection(contour.GetOutputPort())
    contour_mapper.SetScalarRange(0, 7)

    actor.SetMapper(contour_mapper)
    return


def create_planes(func, actor, number_of_planes):
    #
    # Extract planes from implicit function.
    #

    append = vtk.vtkAppendFilter()

    dims = func.GetSampleDimensions()
    slice_increment = (dims[2] - 1) // (number_of_planes + 1)
    slice_num = -4
    for i in range(0, number_of_planes):
        extract = vtk.vtkExtractVOI()
        extract.SetInputConnection(func.GetOutputPort())
        extract.SetVOI(0, dims[0] - 1,
                       0, dims[1] - 1,
                       slice_num + slice_increment, slice_num + slice_increment)
        append.AddInputConnection(extract.GetOutputPort())
        slice_num += slice_increment
    append.Update()

    # Map planes
    planes_mapper = vtk.vtkDataSetMapper()
    planes_mapper.SetInputConnection(append.GetOutputPort())
    planes_mapper.SetScalarRange(0, 7)

    actor.SetMapper(planes_mapper)
    actor.GetProperty().SetAmbient(1.)
    return


def create_contours(func, actor, number_of_planes, number_of_contours):
    #
    # Extract planes from implicit function
    #

    append = vtk.vtkAppendFilter()

    dims = func.GetSampleDimensions()
    slice_increment = (dims[2] - 1) // (number_of_planes + 1)

    slice_num = -4
    for i in range(0, number_of_planes):
        extract = vtk.vtkExtractVOI()
        extract.SetInputConnection(func.GetOutputPort())
        extract.SetVOI(0, dims[0] - 1,
                       0, dims[1] - 1,
                       slice_num + slice_increment, slice_num + slice_increment)
        ranges = [1.0, 6.0]
        contour = vtk.vtkContourFilter()
        contour.SetInputConnection(extract.GetOutputPort())
        contour.GenerateValues(number_of_contours, ranges)
        append.AddInputConnection(contour.GetOutputPort())
        slice_num += slice_increment
    append.Update()

    # Map planes
    planes_mapper = vtk.vtkDataSetMapper()
    planes_mapper.SetInputConnection(append.GetOutputPort())
    planes_mapper.SetScalarRange(0, 7)

    actor.SetMapper(planes_mapper)
    actor.GetProperty().SetAmbient(1.)
    return


def create_outline(source, actor):
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(source.GetOutputPort())
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(outline.GetOutputPort())
    actor.SetMapper(mapper)
    return


if __name__ == "__main__":
    main()