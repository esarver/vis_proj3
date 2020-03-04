cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(vis_proj3)

# VTK Configuration
find_package(VTK COMPONENTS
  vtkCommonColor
  vtkCommonCore
  vtkFiltersSources
  vtkInteractionStyle
  vtkRenderingContextOpenGL2
  vtkRenderingCore
  vtkRenderingFreeType
  vtkRenderingGL2PSOpenGL2
  vtkRenderingOpenGL2 QUIET)

message(STATUS "VTK_VERSION: ${VTK_VERSION}")

# Normally there is some VTK version checking
# here, but it was annoying for my workflow.

# END VTK Configuration

set( sources
    main.cpp
)

set( headers
)

set( objects
)

add_executable(${PROJECT_NAME} ${sources})
target_link_libraries(${PROJECT_NAME} PRIVATE ${VTK_LIBRARIES})

# This is only valid after VTK 8.90.0
# vtk_module_autoinit(
#     TARGETS ${PROJECT_NAME}
#     MODULES ${VTK_LIBRARIES}
# )