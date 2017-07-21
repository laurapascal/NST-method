import sys, os
from PyQt4 import QtCore


fixedrootname = "01"
movingrootname = "02"
fixedVolume = ["data/" + fixedrootname + ".nrrd", "results/WarpImageMultiTransform/" + movingrootname + "-warped.nrrd", "results/WarpImageMultiTransform/" + movingrootname + "-warped2.nrrd"]
fixedModel = ["data/" + fixedrootname + ".vtk", "results/PolydataTransform/" + movingrootname + "-warped.vtk", "results/PolydataTransform/" + movingrootname + "-warped2.vtk"]
movingVolume = "data/" + movingrootname + ".nrrd"
movingModel = "data/" + movingrootname + ".vtk"
rootname = [fixedrootname + "_to_" + movingrootname, movingrootname + "-warped_to_" + movingrootname, movingrootname + "-warped2_to_" + movingrootname]
SignedMaurerDistanceMapFixedVolume = ["results/SignedMaurerDistanceMapImageFilter/" + fixedrootname + ".nrrd", "results/SignedMaurerDistanceMapImageFilter/" + movingrootname + "-warped.nrrd", "results/SignedMaurerDistanceMapImageFilter/" + movingrootname + "-warped.nrrd"]
SignedMaurerDistanceMapMovingVolume = "results/SignedMaurerDistanceMapImageFilter/" + movingrootname + ".nrrd"
warpedVolume = ["results/WarpImageMultiTransform/" + movingrootname + "-warped-test.nrrd", "results/WarpImageMultiTransform/" + movingrootname + "-warped2.nrrd", "results/WarpImageMultiTransform/" + movingrootname + "-warped3.nrrd"]
warpedModel = ["results/PolydataTransform/" + movingrootname + "-warped.vtk", "results/PolydataTransform/" + movingrootname + "-warped2.vtk", "results/PolydataTransform/" + movingrootname + "-warped3.vtk"]


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
    process.setStandardErrorFile( "logs/myANTSlog.log", QtCore.QIODevice.Append)
    process.setStandardOutputFile( "logs/myANTSlogOutputFile.log", QtCore.QIODevice.Append)
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
    process.setStandardErrorFile("logs/myITKTransformToolslog.log", QtCore.QIODevice.Append)
    process.setStandardOutputFile("logs/myITKTransformToolslogOutputFile.log", QtCore.QIODevice.Append)
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
    process.setStandardErrorFile("logs/mypolydatatransformlog.log", QtCore.QIODevice.Append)
    process.setStandardOutputFile("logs/mypolydatatransformlogOutputFile.log", QtCore.QIODevice                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   .Append)
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