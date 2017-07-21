import sys, os
from PyQt4 import QtCore

fixedVolume = ["data/01_seg_manuallyEdited_reg.nrrd", "results/WarpImageMultiTransform/02-warped.nrrd", "results/WarpImageMultiTransform/02-warped2.nrrd"]
fixedModel = ["data/01.vtk", "results/PolydataTransform/02-warped.vtk", "results/PolydataTransform/02-warped2.vtk"]
movingVolume = "data/02_seg_manuallyEdited.nrrd"
movingModel = "data/02.vtk"
rootname = ["01_to_02" ,"02-warped_to_02", "02-warped2_to_02"]
SignedMaurerDistanceMapFixedVolume = ["results/SignedMaurerDistanceMapImageFilter/01.nrrd", "results/SignedMaurerDistanceMapImageFilter/02-warped.nrrd", "results/SignedMaurerDistanceMapImageFilter/02-warped.nrrd"]
SignedMaurerDistanceMapMovingVolume = "results/SignedMaurerDistanceMapImageFilter/02.nrrd"
warpedVolume = ["results/WarpImageMultiTransform/02-warped-test.nrrd", "results/WarpImageMultiTransform/02-warped2.nrrd", "results/WarpImageMultiTransform/02-warped3.nrrd"]
warpedModel = ["results/PolydataTransform/02-warped.vtk", "results/PolydataTransform/02-warped2.vtk", "results/PolydataTransform/02-warped3.vtk"]


for i in [0,1,2]:
    print " ------------------------------------------------------------ Iteration: " + str(i)

    # SignedMaurerDistanceMapImageFilter
    SignedMaurerDistanceMapImageFilter = "/home/laura.pascal/Documents/Non-Spherical-Topology/NST-method/CLI/SignedMaurerDistanceMapImageFilter-build/bin/SignedMaurerDistanceMapImageFilter"
    arguments = list()
    arguments.append("--inputfile")
    arguments.append(fixedVolume[i])
    arguments.append("--outputfile")
    arguments.append(SignedMaurerDistanceMapFixedVolume[i])
    process = QtCore.QProcess()
    print "Calling SignedMaurerDistanceMapImageFilter"
    process.setStandardErrorFile( "logs/mySignedMaurerDistanceMapImageFilterlog.log", QtCore.QIODevice.Append)
    process.setStandardOutputFile( "logs/mySignedMaurerDistanceMapImageFilterlogOutputFile.log", QtCore.QIODevice.Append)
    process.start(SignedMaurerDistanceMapImageFilter, arguments)
    process.waitForStarted()
    print "state: " + str(process.state())
    process.waitForFinished(-1)
    print "error: " + str(process.error())


    arguments = list()
    arguments.append("--inputfile")
    arguments.append(movingVolume)
    arguments.append("--outputfile")
    arguments.append(SignedMaurerDistanceMapMovingVolume)
    process = QtCore.QProcess()
    print "Calling SignedMaurerDistanceMapImageFilter"
    process.setStandardErrorFile( "logs/mySignedMaurerDistanceMapImageFilterlog.log", QtCore.QIODevice.Append)
    process.setStandardOutputFile( "logs/mySignedMaurerDistanceMapImageFilterlogOutputFile.log", QtCore.QIODevice.Append)
    process.start(SignedMaurerDistanceMapImageFilter, arguments)
    process.waitForStarted()
    print "state: " + str(process.state())
    process.waitForFinished(-1)
    print "error: " + str(process.error())

    # Registration
    ANTS = "/home/laura/Documents/Non-Spherical-Topology/ANTs-build/bin/ANTS"
    arguments = list()
    arguments.append("3")
    arguments.append("-m")
    arguments.append("CC[" + SignedMaurerDistanceMapFixedVolume[i] + "," + SignedMaurerDistanceMapMovingVolume + ",1,4]")
    arguments.append("-i")
    arguments.append("130x50x20")
    arguments.append("-o")
    ANTS_output_name = "result/ANTS/" + rootname[i] + ".nii.gz"
    arguments.append(ANTS_output_name)
    arguments.append("-t")
    arguments.append("SyN[1]")
    arguments.append("-r")
    arguments.append("Gauss[1,0]")
    process = QtCore.QProcess()
    print "Calling ANTS"
    process.setStandardErrorFile( "log/myANTSlog.log", QtCore.QIODevice.Append)
    process.setStandardOutputFile( "log/myANTSlogOutputFile.log", QtCore.QIODevice.Append)
    process.start(ANTS, arguments)
    process.waitForStarted()
    print "state: " + str(process.state())
    process.waitForFinished(-1)
    print "error: " + str(process.error())
    print "exitStatus: " + str(process.exitStatus())

    # Concatenation of transform and warping of polydata
    #   Concatenation of original transfor/m
    ITKTransformTools = "/home/laura/Documents/Non-Spherical-Topology/ITKTransformTools-build/ITKTransformTools"
    arguments = list()
    arguments.append("concatenate")
    concatenated_transform = "result/ITKTransformTools/" + rootname[i] + "ConcatenatedTransform.nrrd"
    arguments.append(concatenated_transform)
    arguments.append("-r")
    arguments.append(movingVolume)
    deformation_field = "result/ANTS/" + rootname[i] + "Warp.nii.gz"
    arguments.append(deformation_field)
    arguments.append("displacement")
    affine_transform = "result/ANTS/" + rootname[i] + "Affine.txt"
    arguments.append(affine_transform)
    process = QtCore.QProcess()
    print "Calling ITKTransformTools"
    process.setStandardErrorFile("log/myITKTransformToolslog.log", QtCore.QIODevice.Append)
    process.setStandardOutputFile("log/myITKTransformToolslogOutputFile.log", QtCore.QIODevice.Append)
    process.start(ITKTransformTools, arguments)
    process.waitForStarted()
    print "state: " + str(process.state())
    process.waitForFinished(-1)
    print "error: " + str(process.error())
    print "exitStatus: " + str(process.exitStatus())

    #   Polydata transformation
    polydatatransform = "/home/laura/Documents/Slicer-nightly/Slicer-build/Slicer-build/lib/Slicer-4.7/cli-modules/polydatatransform"
    arguments = list()
    arguments.append("--fiber_file")
    fiber_file = fixedModel[i]
    arguments.append(fiber_file)
    arguments.append("--displacement_field")
    arguments.append(concatenated_transform)
    arguments.append("--fiber_output")
    arguments.append(warpedModel[i])
    arguments.append("--invertx")
    arguments.append("--inverty")
    process = QtCore.QProcess()
    print "Calling polydatatransform"
    process.setStandardErrorFile("log/mypolydatatransformlog.log", QtCore.QIODevice.Append)
    process.setStandardOutputFile("log/mypolydatatransformlogOutputFile.log", QtCore.QIODevice                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   .Append)
    process.start(polydatatransform, arguments)
    process.waitForStarted()
    print "state: " + str(process.state())
    process.waitForFinished(-1)
    print "error: " + str(process.error())
    print "exitStatus: " + str(process.exitStatus())


    #   Warping of fixed image to moving image with WarpImageMultiTransform
    WarpImageMultiTransform = "/home/laura/Documents/Non-Spherical-Topology/ANTs-build/bin/WarpImageMultiTransform"
    arguments = list()
    arguments.append("3")
    arguments.append(movingVolume)
    arguments.append(warpedVolume[i])
    arguments.append("-R")
    arguments.append(fixedVolume[i])
    arguments.append(deformation_field)
    arguments.append(affine_transform)
    arguments.append("--use-NN")
    process = QtCore.QProcess()
    print "Calling WarpImageMultiTransform"
    process.setStandardErrorFile("log/myWarpImageMultiTransformlog.log", QtCore.QIODevice.Append)
    process.setStandardOutputFile("log/myWarpImageMultiTransformlogOutputFile.log", QtCore.QIODevice.Append)
    process.start(WarpImageMultiTransform, arguments)
    process.waitForStarted()
    print "state: " + str(process.state())
    process.waitForFinished(-1)
    print "error: " + str(process.error())
    print "exitStatus: " + str(process.exitStatus())