import os
import sys
import numpy
from PyMca5.PyMcaIO import specfilewrapper as specfile
from PyMca5.PyMcaIO import ConfigDict
from PyMca5.PyMcaPhysics.xrf import ClassMcaTheory
from PyMca5.PyMcaPhysics.xrf import ConcentrationsTool

# if sys.version_info < (3,):
#     from StringIO import StringIO
# else:
#     from io import StringIO

# dataDir = PyMcaDataDir.PYMCA_DATA_DIR
# spe = os.path.join(dataDir, "Steel.mca")
# cfg = os.path.join(dataDir, "Steel.cfg")
spe = "sample-data/Nickel.mca"
cfg = "cfg/stainless-v0.7.cfg"
# self.assertTrue(os.path.isfile(spe),
#                 "File %s is not an actual file" % spe)

sf = specfile.Specfile(spe)

# TEMP ##################################################
# This code can read off the calibration parameters
print(len(sf))
calib= sf.scandata[0].header("@CALIB")
print(calib)

# NOTE: we can also load a different calib file separately - in pymca, we can save this separately
# TEMP ##################################################

# y = mcaData = sf[1].mca(1)
y = mcaData = sf[0].mca(1)
sf = None

# perform the actual XRF analysis
configuration = ConfigDict.ConfigDict()
# configuration.readfp(StringIO(cfg))
configuration.read(cfg)
mcaFit = ClassMcaTheory.ClassMcaTheory()
configuration=mcaFit.configure(configuration)
x = numpy.arange(y.size).astype(numpy.float64)

# print(mcaFit)
# TEMP ##################################################

# if self.calibration == 'None':
#     calib = [0.0, 1.0, 0.0]
# else:
#     calib = curveinfo.get('McaCalib', [0.0, 1.0, 0.0])

# self.__simplefitcalibration = calib

# calib = [-0.081195586, 0.0264471, 0]
# TODO: see if this actually does anything
# calib = [100, 0, -1]
# calibrationOrder = curveinfo.get('McaCalibOrder', 2)
# if calibrationOrder == 'TOF':
print(x)
print(y)
# x = calib[2] + calib[0] / pow(x - calib[1], 2)
# x - calib[1]
# else:
# print(x.shape)
# x = calib[0] + calib[1] * x + calib[2] * x * x
# print(x.shape)
# print(calib[1] * x + calib[2] * x * x)
# TEMP ##################################################
# print(configuration["fit"])
mcaFit.setData(x,y,
               xmin=configuration["fit"]["xmin"],
               xmax=configuration["fit"]["xmax"],
               calibration=calib)

# TODO: This seems to do the trick - we need to find a way to get these from the config though
# mcaFit.config['detector']['zero'] = -0.081195586
# mcaFit.config['detector']['gain'] = 0.026645403

# print(mcaFit.getConfiguration())
# mcaFit.setConfiguration(configuration)
# mcaFit.configure()
mcaFit.estimate()
# print(configuration['detector']['gain'])
fitResult, result = mcaFit.startFit(digest=1)
# print(result)

# fit is already done, calculate the concentrations
concentrationsConfiguration = configuration["concentrations"]
cTool = ConcentrationsTool.ConcentrationsTool()
cToolConfiguration = cTool.configure()
cToolConfiguration.update(configuration['concentrations'])

# print(configuration['concentrations'])

concentrationsResult, addInfo = cTool.processFitResult( \
            config=cToolConfiguration,
            fitresult={"result":result},
            elementsfrommatrix=False,
            fluorates = mcaFit._fluoRates,
            addinfo=True)

# print(concentrationsResult.keys())
print(concentrationsResult['mass fraction'])







#
# fitreference = False
# if configuration['concentrations']['usematrix']:
#     # _logger.debug("USING MATRIX")
#     if configuration['concentrations']['reference'].upper() == "AUTO":
#         fitreference = True
# # elif autotime:
# #     # we have to calculate with the time in the configuration
# #     # and correct later on
# #     cToolConfiguration["autotime"] = 0
#
# fitresult = {}
# if fitreference:
#     # we have to fit the "reference" spectrum just to get the reference element
#     mcafitresult = mcaFit.startfit(digest=0, linear=True)
#     # if one of the elements has zero area this cannot be made directly
#     fitresult['result'] = mcaFit.imagingDigestResult()
#     fitresult['result']['config'] = configuration
#     concentrationsResult, addInfo = cTool.processFitResult(config=cToolConfiguration,
#                                         fitresult=fitresult,
#                                         elementsfrommatrix=False,
#                                         fluorates=mcaFit._fluoRates,
#                                         addinfo=True)
#     # and we have to make sure that all the areas are positive
#     for group in fitresult['result']['groups']:
#         if fitresult['result'][group]['fitarea'] <= 0.0:
#             # give a tiny area
#             fitresult['result'][group]['fitarea'] = 1.0e-6
#     config['concentrations']['reference'] = addInfo['ReferenceElement']
# else:
#     fitresult['result'] = {}
#     fitresult['result']['config'] = configuration
#     fitresult['result']['groups'] = []
#     idx = 0
#     for iParam, param in enumerate(mcaFit.PARAMETERS):
#         # if mcaFit.codes[0][iParam] == Gefit.CFIXED:
#         #     continue
#         if iParam < mcaFit.NGLOBAL:
#             # background
#             pass
#         else:
#             fitresult['result']['groups'].append(param)
#             fitresult['result'][param] = {}
#             # we are just interested on the factor to be applied to the area to get the
#             # concentrations
#             fitresult['result'][param]['fitarea'] = 1.0
#             fitresult['result'][param]['sigmaarea'] = 1.0
#         idx += 1
# concentrationsResult, addInfo = cTool.processFitResult(config=cToolConfiguration,
#                                         fitresult=fitresult,
#                                         elementsfrommatrix=False,
#                                         fluorates=mcaFit._fluoRates,
#                                         addinfo=True)
#
# print(concentrationsResult['mass fraction'])

















# cToolConfiguration['usematrix'] = 0
# cToolConfiguration['flux'] = addInfo["Flux"]
# cToolConfiguration['time'] = addInfo["Time"]
# cToolConfiguration['area'] = addInfo["DetectorArea"]
# cToolConfiguration['distance'] = addInfo["DetectorDistance"]
# concentrationsResult2, addInfo = cTool.processFitResult( \
#             config=cToolConfiguration,
#             fitresult={"result":result},
#             elementsfrommatrix=False,
#             fluorates = mcaFit._fluoRates,
#             addinfo=True)
# referenceElement = addInfo['ReferenceElement']
# referenceTransitions = addInfo['ReferenceTransitions']
# # make sure we are using Co as internal standard
# cToolConfiguration["usematrix"] = 1
# cToolConfiguration["reference"] = "Co"
# concentrationsResult, addInfo = cTool.processFitResult( \
#             config=cToolConfiguration,
#             fitresult={"result":result},
#             elementsfrommatrix=False,
#             fluorates = mcaFit._fluoRates,
#             addinfo=True)
# referenceElement = addInfo['ReferenceElement']
# referenceTransitions = addInfo['ReferenceTransitions']
# self.assertTrue(referenceElement == "Co",
#        "referenceElement is <%s> instead of <Co>" % referenceElement)
# cobalt = concentrationsResult["mass fraction"]["Co K"]
# self.assertTrue( abs(cobalt-0.0005) < 1.0E-7,
#                 "Wrong Co concentration %f expected 0.0005" % cobalt)
#
# # we should get the same result with internal parameters
# cTool = ConcentrationsTool.ConcentrationsTool()
# cToolConfiguration = cTool.configure()
# cToolConfiguration.update(configuration['concentrations'])
#
# # make sure we are not using an internal standard
# cToolConfiguration['usematrix'] = 0
# cToolConfiguration['flux'] = addInfo["Flux"]
# cToolConfiguration['time'] = addInfo["Time"]
# cToolConfiguration['area'] = addInfo["DetectorArea"]
# cToolConfiguration['distance'] = addInfo["DetectorDistance"]
# concentrationsResult2, addInfo = cTool.processFitResult( \
#             config=cToolConfiguration,
#             fitresult={"result":result},
#             elementsfrommatrix=False,
#             fluorates = mcaFit._fluoRates,
#             addinfo=True)
# referenceElement = addInfo['ReferenceElement']
# referenceTransitions = addInfo['ReferenceTransitions']
# self.assertTrue(referenceElement in ["None", "", None],
#        "referenceElement is <%s> instead of <None>" % referenceElement)
#
# for key in concentrationsResult["mass fraction"]:
#     internal = concentrationsResult["mass fraction"][key]
#     fp = concentrationsResult2["mass fraction"][key]
#     delta = 100 * (abs(internal - fp) / internal)
#     self.assertTrue( delta < 1.0e-5,
#         "Error for <%s> concentration %g != %g" % (key, internal, fp))





#
# import os
# import numpy
# import h5py
#
# # use a dummy 3D array generated using data supplied with PyMca
# from PyMca5 import PyMcaDataDir
# from PyMca5.PyMcaIO import specfilewrapper as specfile
# from PyMca5.PyMcaIO import ConfigDict
#
# # dataDir = PyMcaDataDir.PYMCA_DATA_DIR
# # spe = os.path.join(dataDir, "Steel.mca")
# # cfg = os.path.join(dataDir, "Steel.cfg")
# spe = "sample-data/Nickel.mca"
# cfg = "cfg/stainless-v0.7.cfg"
# sf = specfile.Specfile(spe)
# y = counts = sf[0].mca(1)
# x = channels = numpy.arange(y.size).astype(numpy.float)
# configuration = ConfigDict.ConfigDict()
# configuration.read(cfg)
# calibration = configuration["detector"]["zero"], \
#               configuration["detector"]["gain"], 0.0
# initialTime = configuration["concentrations"]["time"]
#
# # create the data
# nRows = 5
# nColumns = 10
# nTimes = 3
# data = numpy.zeros((nRows, nColumns, counts.size), dtype = numpy.float)
# live_time = numpy.zeros((nRows * nColumns), dtype=numpy.float)
#
# mcaIndex = 0
# for i in range(nRows):
#     for j in range(nColumns):
#         factor = (1 + mcaIndex % nTimes)
#         data[i, j] = counts * factor
#         live_time[i * nColumns + j] = initialTime * factor
#         mcaIndex += 1
#
#
# h5File = "Nickel.h5"
# if os.path.exists(h5File):
#     os.remove(h5File)
# h5 = h5py.File(h5File, "w")
# h5["/entry/instrument/detector/calibration"] = calibration
# h5["/entry/instrument/detector/channels"] = channels
# h5["/entry/instrument/detector/data"] = data
# h5["/entry/instrument/detector/live_time"] = live_time
#
# # add nexus conventions (not needed)
# h5["/entry/title"] = u"Dummy generated map"
# h5["/entry"].attrs["NX_class"] = u"NXentry"
# h5["/entry/instrument"].attrs["NX_class"] = u"NXinstrument"
# h5["/entry/instrument/detector/"].attrs["NX_class"] = u"NXdetector"
# h5["/entry/instrument/detector/data"].attrs["interpretation"] = \
#                                                       u"spectrum"
# # implement a default plot named measurement (not needed)
# h5["/entry/measurement/data"] = \
#                     h5py.SoftLink("/entry/instrument/detector/data")
# h5["/entry/measurement"].attrs["NX_class"] = u"NXdata"
# h5["/entry/measurement"].attrs["signal"] = u"data"
# h5["/entry"].attrs["default"] = u"measurement"
#
# h5.flush()
# h5.close()
# h5 = None
# #
# # from PyMca5.PyMcaPhysics.xrf.FastXRFLinearFit import FastXRFLinearFit
# #
# #
# # # configurationFile = 'cfg/stainless-v0.7.cfg'
# #
# # fastFit = FastXRFLinearFit()
# # fastFit.setFitConfigurationFile(cfg)
# # outputBuffer = fastFit.fitMultipleSpectra(y=data)
# # print(outputBuffer)
#
#
# ###############
# # from PyMca5.PyMcaPhysics.xrf.FastXRFLinearFit import FastXRFLinearFit
# #
# #
# # configurationFile = 'cfg/stainless-v0.7.cfg'
# #
# # fastFit = FastXRFLinearFit()
# # fastFit.setFitConfigurationFile(configurationFile)
#
#
#
# ############
#
# # outputBuffer = fastFit.fitMultipleSpectra(y=dataStack,
# #                                                 weight=weight,
# #                                                 refit=refit,
# #
# # concentrations=concentrations,
# #                                                 outbuffer=None)
#
#
#
#
# # import sys
# # import os
# # import logging
# # _logger = logging.getLogger(__name__)
# #
# # from PyMca5.PyMcaGui import PyMcaQt as qt
# # QTVERSION = qt.qVersion()
# # from PyMca5.PyMcaGui import PyMca_Icons as icons
# # from PyMca5.PyMcaIO import spswrap as sps
# # from PyMca5 import PyMcaDirs
# # from PyMca5.PyMcaGui.io import PyMcaFileDialogs
# #
# # BLISS = False
# # if sys.version_info > (3, 5):
# #     try:
# #         from PyMca5.PyMcaCore import RedisTools
# #         BLISS = True
# #     except:
# #         _logger.info("Bliss data file direct support not available")
# #
# #
# # class QSourceSelector(qt.QWidget):
# #     sigSourceSelectorSignal = qt.pyqtSignal(object)
# #     def __init__(self, parent=None, filetypelist=None, pluginsIcon=False):
# #         qt.QWidget.__init__(self, parent)
# #         self.mainLayout= qt.QVBoxLayout(self)
# #         self.mainLayout.setContentsMargins(0, 0, 0, 0)
# #         self.mainLayout.setSpacing(0)
# #         if filetypelist is None:
# #             self.fileTypeList = ["Spec Files (*mca)",
# #                                 "Spec Files (*dat)",
# #                                 "Spec Files (*spec)",
# #                                 "SPE Files (*SPE)",
# #                                 "EDF Files (*edf)",
# #                                 "EDF Files (*ccd)",
# #                                 "CSV Files (*csv)",
# #                                 "All Files (*)"]
# #         else:
# #             self.fileTypeList = filetypelist
# #         self.lastFileFilter = self.fileTypeList[0]
# #
# #         # --- file combo/open/close
# #         self.lastInputDir = PyMcaDirs.inputDir
# #         self.fileWidget= qt.QWidget(self)
# #         fileWidgetLayout= qt.QHBoxLayout(self.fileWidget)
# #         fileWidgetLayout.setContentsMargins(0, 0, 0, 0)
# #         fileWidgetLayout.setSpacing(0)
# #         self.fileCombo  = qt.QComboBox(self.fileWidget)
# #         self.fileCombo.setEditable(0)
# #         self.mapCombo= {}
# #         openButton= qt.QPushButton(self.fileWidget)
# #
# #         self.openIcon   = qt.QIcon(qt.QPixmap(icons.IconDict["fileopen"]))
# #         self.closeIcon  = qt.QIcon(qt.QPixmap(icons.IconDict["close"]))
# #         self.reloadIcon = qt.QIcon(qt.QPixmap(icons.IconDict["reload"]))
# #         if BLISS:
# #             self.specIcon   = qt.QIcon(qt.QPixmap(icons.IconDict["bliss"]))
# #         else:
# #             self.specIcon   = qt.QIcon(qt.QPixmap(icons.IconDict["spec"]))
# #
# #         openButton.setIcon(self.openIcon)
# #         openButton.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Minimum))
# #         openButton.setToolTip("Open new file data source")
# #
# #         closeButton= qt.QPushButton(self.fileWidget)
# #         closeButton.setIcon(self.closeIcon)
# #         closeButton.setToolTip("Close current data source")
# #
# #         refreshButton= qt.QPushButton(self.fileWidget)
# #         refreshButton.setIcon(self.reloadIcon)
# #         refreshButton.setToolTip("Refresh data source")
# #
# #         specButton= qt.QPushButton(self.fileWidget)
# #         specButton.setIcon(self.specIcon)
# #         if BLISS:
# #             specButton.setToolTip("Open data acquisition source")
# #         else:
# #             specButton.setToolTip("Open new shared memory source")
# #
# #         closeButton.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Minimum))
# #         specButton.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Minimum))
# #         refreshButton.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Minimum))
# #
# #         openButton.clicked.connect(self._openFileSlot)
# #         closeButton.clicked.connect(self.closeFile)
# #         refreshButton.clicked.connect(self._reload)
# #
# #         specButton.clicked.connect(self.openBlissOrSpec)
# #         self.fileCombo.activated[str].connect(self._fileSelection)
# #
# #         fileWidgetLayout.addWidget(self.fileCombo)
# #         fileWidgetLayout.addWidget(openButton)
# #         fileWidgetLayout.addWidget(closeButton)
# #         fileWidgetLayout.addWidget(specButton)
# #         if sys.platform == "win32":specButton.hide()
# #         fileWidgetLayout.addWidget(refreshButton)
# #         self.specButton = specButton
# #         if pluginsIcon:
# #             self.pluginsButton = qt.QPushButton(self.fileWidget)
# #             self.pluginsButton.setIcon(qt.QIcon(qt.QPixmap(icons.IconDict["plugin"])))
# #             self.pluginsButton.setToolTip("Plugin handling")
# #             self.pluginsButton.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Minimum))
# #             fileWidgetLayout.addWidget(self.pluginsButton)
# #         self.mainLayout.addWidget(self.fileWidget)
# #
# #     def _reload(self):
# #         _logger.debug("_reload called")
# #         qstring = self.fileCombo.currentText()
# #         if not len(qstring):
# #             return
# #
# #         key = qt.safe_str(qstring)
# #         ddict = {}
# #         ddict["event"] = "SourceReloaded"
# #         ddict["combokey"] = key
# #         ddict["sourcelist"] = self.mapCombo[key] * 1
# #         self.sigSourceSelectorSignal.emit(ddict)
# #
# #     def _openFileSlot(self):
# #         self.openFile(None, None)
# #
# #     def openSource(self, sourcename, specsession=None):
# #         if specsession is None:
# #             if sourcename in sps.getspeclist():
# #                 specsession=True
# #             elif BLISS and sourcename in RedisTools.get_sessions_list():
# #                 specsession = "bliss"
# #             else:
# #                 specsession=False
# #         self.openFile(sourcename, specsession=specsession)
# #
# #     def openFile(self, filename=None, justloaded=None, specsession=False):
# #         _logger.debug("openfile = %s", filename)
# #         staticDialog = False
# #         if specsession == "bliss":
# #             specsession = False
# #             session = filename
# #             node = RedisTools.get_node(session)
# #             if not node:
# #                 txt = "No REDIS information retrieved from session %s"  % \
# #                         session
# #                 raise IOError(txt)
# #             filename = RedisTools.get_session_filename(node)
# #             if not len(filename):
# #                 txt = "Cannot retrieve last output filename from session %s"  % \
# #                         session
# #                 raise IOError(txt)
# #             if not os.path.exists(filename):
# #                 txt = "Last output file <%s>  does not exist"  % filename
# #                 raise IOError(txt)
# #             filename = [filename]
# #             key = os.path.basename(filename[0])
# #             try:
# #                 self._emitSourceSelectedOrReloaded(filename, key)
# #             except:
# #                 _logger.error("Problem opening %s" % filename[0])
# #             key = "%s" % session
# #             self._emitSourceSelectedOrReloaded([session], key)
# #             return
# #         if not specsession:
# #             if justloaded is None:
# #                 justloaded = True
# #             if filename is None:
# #                 if self.lastInputDir is not None:
# #                     if not os.path.exists(self.lastInputDir):
# #                         self.lastInputDir = None
# #                 wdir = self.lastInputDir
# #                 filelist, fileFilter =  PyMcaFileDialogs.getFileList(self,
# #                                                  filetypelist=self.fileTypeList,
# #                                                  message="Open a new source file",
# #                                                  currentdir=wdir,
# #                                                  mode="OPEN",
# #                                                  getfilter=True,
# #                                                  single=False,
# #                                                  currentfilter=self.lastFileFilter)
# #                 if not len(filelist):
# #                     return
# #                 if not len(filelist[0]):
# #                     return
# #                 filename=[]
# #                 for f in filelist:
# #                     filename.append(qt.safe_str(f))
# #                 if not len(filename):
# #                     return
# #                 if len(filename):
# #                     self.lastInputDir  = os.path.dirname(filename[0])
# #                     PyMcaDirs.inputDir = os.path.dirname(filename[0])
# #                     self.lastFileFilter = fileFilter
# #                 justloaded = True
# #             if justloaded:
# #                 if type(filename) != type([]):
# #                     filename = [filename]
# #             if not os.path.exists(filename[0]):
# #                 if '%' not in filename[0]:
# #                     raise IOError("File %s does not exist" % filename[0])
# #             #check if it is a stack
# #             if len(filename) > 1:
# #                 key = "STACK from %s to %s" % (filename[0], filename[-1])
# #             else:
# #                 key = os.path.basename(filename[0])
# #         else:
# #             key = filename
# #             if key not in sps.getspeclist():
# #                 qt.QMessageBox.critical(self,
# #                                     "SPS Error",
# #                                     "No shared memory source named %s" % key)
# #                 return
# #
# #         self._emitSourceSelectedOrReloaded(filename, key)
# #
# #     def _emitSourceSelectedOrReloaded(self, filename, key):
# #         ddict = {}
# #         ddict["event"] = "NewSourceSelected"
# #         if key in self.mapCombo.keys():
# #             if self.mapCombo[key] == filename:
# #                 #Reloaded event
# #                 ddict["event"] = "SourceReloaded"
# #             else:
# #                 i = 0
# #                 while key in self.mapCombo.keys():
# #                     key += "_%d" % i
# #         ddict["combokey"]   = key
# #         ddict["sourcelist"] = filename
# #         self.mapCombo[key] = filename
# #         if ddict["event"] =="NewSourceSelected":
# #             nitems = self.fileCombo.count()
# #             self.fileCombo.insertItem(nitems, key)
# #             self.fileCombo.setCurrentIndex(nitems)
# #         else:
# #             if hasattr(qt, "QString"):
# #                 nitem = self.fileCombo.findText(qt.QString(key))
# #             else:
# #                 nitem = self.fileCombo.findText(key)
# #             self.fileCombo.setCurrentIndex(nitem)
# #
# #         self.sigSourceSelectorSignal.emit(ddict)
# #
# #     def closeFile(self):
# #         _logger.debug("closeFile called")
# #         #get current combobox key
# #         qstring = self.fileCombo.currentText()
# #         if not len(qstring):
# #             return
# #         key = qt.safe_str(qstring)
# #         ddict = {}
# #         ddict["event"] = "SourceClosed"
# #         ddict["combokey"] = key
# #         ddict["sourcelist"] = self.mapCombo[key] * 1
# #         if hasattr(qt, "QString"):
# #             nitem = self.fileCombo.findText(qt.QString(key))
# #         else:
# #             nitem = self.fileCombo.findText(key)
# #         self.fileCombo.removeItem(nitem)
# #         del self.mapCombo[key]
# #         self.sigSourceSelectorSignal.emit(ddict)
# #
# #     def openBlissOrSpec(self):
# #         if not BLISS:
# #             return self.openSpec()
# #         sessionList = RedisTools.get_sessions_list()
# #         if not len(sessionList):
# #             return self.openSpec()
# #         activeList = []
# #         for session in sessionList:
# #             node = RedisTools.get_node(session)
# #             if node:
# #                 activeList.append(session)
# #         if not len(activeList):
# #             _logger.info("Bliss sessions found but no info in REDIS")
# #             return self.openSpec()
# #         sessionList = activeList
# #
# #         menu = qt.QMenu()
# #         for session in sessionList:
# #             if hasattr(qt, "QString"):
# #                 menu.addAction(qt.QString(session),
# #                         lambda i=session:self.openFile(i, specsession="bliss"))
# #             else:
# #                 menu.addAction(session,
# #                         lambda i=session:self.openFile(i, specsession="bliss"))
# #         menu.exec_(self.cursor().pos())
# #
# #
# #     def openSpec(self):
# #         speclist = sps.getspeclist()
# #         if not len(speclist):
# #             qt.QMessageBox.information(self,
# #                     "No SPEC Shared Memory or Bliss session in REDIS Found",
# #                     "No shared memory source available")
# #             return
# #
# #         menu = qt.QMenu()
# #         for spec in speclist:
# #             if hasattr(qt, "QString"):
# #                 menu.addAction(qt.QString(spec),
# #                         lambda i=spec:self.openFile(i, specsession=True))
# #             else:
# #                 menu.addAction(spec,
# #                         lambda i=spec:self.openFile(i, specsession=True))
# #         menu.exec_(self.cursor().pos())
# #
# #
# #     def _fileSelection(self, qstring):
# #         _logger.debug("file selected %s", qstring)
# #         key = str(qstring)
# #         ddict = {}
# #         ddict["event"] = "SourceSelected"
# #         ddict["combokey"] = key
# #         ddict["sourcelist"] = self.mapCombo[key]
# #         print(ddict)
# #         self.sigSourceSelectorSignal.emit(ddict)
# #
# # def test():
# #     a = qt.QApplication(sys.argv)
# #     #new access
# #     from PyMca5.PyMcaGui.pymca import QDataSource
# #     w= QSourceSelector()
# #     def mySlot(ddict):
# #         print(ddict)
# #         if ddict["event"] == "NewSourceSelected":
# #             d = QDataSource.QDataSource(ddict["sourcelist"][0])
# #             w.specfileWidget.setDataSource(d)
# #             w.sigSourceSelectorSignal.connect(mySlot)
# #
# #     a.lastWindowClosed.connect(a.quit)
# #
# #     w.show()
# #     a.exec_()
# #
# #
# # if __name__=="__main__":
# #     test()
# #
# # #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# # # # import mcareader
# # # #
# # # # xrf_data = mcareader.Mca('sample-data/Stainless 316.mca')
# # # # xrf_data.plot(log_y=True)
# # #
# # #
# # # from PyMca5 import Plugin1DBase
# # #
# # # class Shifting(Plugin1DBase.Plugin1DBase):
# # #     def getMethods(self, plottype=None):
# # #         return ["Shift"]
# # #
# # #     def getMethodToolTip(self, methodName):
# # #         if methodName != "Shift":
# # #             raise InvalidArgument("Method %s not valid" % methodName)
# # #         return "Subtract minimum, normalize to maximum, and shift up by 0.1"
# # #
# # #     def applyMethod(self, methodName):
# # #         if methodName != "Shift":
# # #             raise ValueError("Method %s not valid" % methodName)
# # #         allCurves = self.getAllCurves()
# # #         increment = 0.1
# # #         for i in range(len(allCurves)):
# # #             x, y, legend, info = allCurves[i][:4]
# # #             delta = float(y.max() - y.min())
# # #             if delta < 1.0e-15:
# # #                 delta = 1.0
# # #             y = (y - y.min())/delta + i * increment
# # #             if i == (len(allCurves) - 1):
# # #                 replot = True
# # #             else:
# # #                 replot = False
# # #             if i == 0:
# # #                 replace = True
# # #             else:
# # #                 replace = False
# # #             self.addCurve(x, y, legend=legend + " %.2f" % (i * increment),
# # #                                 info=info, replace=replace, replot=replot)
# # #
# # # MENU_TEXT="Simple Shift Example"
# # # def getPlugin1DInstance(plotWindow, **kw):
# # #     ob = Shifting(plotWindow)
# # #     return ob
