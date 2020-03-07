import vtk
from typing import Tuple, List
from numpy import arange


def get_program_parameters() -> str:
    import argparse
    description = 'The skin extracted from a CT dataset of the head.'
    epilogue = '''
    Derived from VTK/Examples/Cxx/Medical1.cxx
    This example reads a volume dataset, extracts an isosurface that
     represents the skin and displays it.
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='FullHead.mhd')
    args = parser.parse_args()
    return args.filename


def configure_render() -> Tuple[vtk.vtkRenderer, vtk.vtkRenderWindow, vtk.vtkRenderWindowInteractor]:
    ren = vtk.vtkRenderer()
    ren_win = vtk.vtkRenderWindow()
    ren_win.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)

    return ren, ren_win, iren

def generate_data() -> Tuple[List[float], List[float], List[float]]:

    pass

def main():
    (ren, ren_win, iren) = configure_render()
    colors = vtk.vtkNamedColors()



    # Define grid
    # Generate Scalar field

    # TODO Design Color table
    # Put the values in the grid

    # 4 Displays
    # TODO: IsoSurface
    # TODO: Cutting Planes
    # TODO: Contour Lines
    # TODO: Document techniques

    # Setup the renderer

    # render the stuff

    ren.SetBackground(colors.GetColor3d('Navy'))
    ren_win.SetSize(300, 300)

    # interact with data
    iren.Initialize()
    ren_win.Render()
    iren.Start()


if __name__ == '__main__':
    main()
