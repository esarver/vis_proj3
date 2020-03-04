import vtk

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

def main():
    ## Define grid
    #TODO: Uniform grid 26x26x26, xyzv ranges [0.0,1.0]...

    ## Generate Scalar field

    ## Design Color table

    ## 4 Displays
    #TODO: IsoSurface
    #TODO: Cutting Planes
    #TODO: Contour Lines
    #TODO: Document techniques
    pass

if __name__ == '__main__':
    main()