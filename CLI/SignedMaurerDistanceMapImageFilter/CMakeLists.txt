cmake_minimum_required(VERSION 2.8)
 
project(SignedMaurerDistanceMapImageFilter)
 
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})


# Find SlicerExecutionModel
find_package(SlicerExecutionModel REQUIRED)
include(${SlicerExecutionModel_USE_FILE})
include(${GenerateCLP_USE_FILE})

# Find ITK
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})

set(SignedMaurerDistanceMapImageFilter_SOURCE SignedMaurerDistanceMapImageFilter.cxx)

SEMMacroBuildCLI(
  NAME SignedMaurerDistanceMapImageFilter
  EXECUTABLE_ONLY
  TARGET_LIBRARIES ${ITK_LIBRARIES}
  INCLUDE_DIRECTORIES ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
  ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
  INSTALL_RUNTIME_DESTINATION bin
  INSTALL_LIBRARY_DESTINATION lib
  INSTALL_ARCHIVE_DESTINATION lib
)
