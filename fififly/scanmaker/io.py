#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 10:53:41 2021

@author: dfadda
"""
from xml.etree.ElementTree import ElementTree as ET
import numpy as np
import os


def loadTitles(aorfile):
    
    tree = ET(file=aorfile)
    vector = tree.find('list/vector')
    titles = [item.text for item in vector.findall('Request/title')]
    titles = np.array(titles)

    return titles

def makeScans(folder, aor):
    """Export AOR into scans for observation"""
    from fififly.scanmaker.grating import wavelength2inductosyn as w2i
    
    print('Folder is ', folder)
    # Case of OTF MAP
    
    # For each offset, create two files (one ON and one OFF)
    # The difference is 
    
    # Compute grating positions
    print('wave, dichroic, order ', aor.waveBlue, aor.dichroic, aor.order)
    aor.gratingBlue = w2i(float(aor.waveBlue), aor.dichroic, 'BLUE', aor.order)
    aor.gratingRed = w2i(float(aor.waveRed), aor.dichroic,'RED', 1)
    
    # Go through all the files (on and off)
    # Special case for OTF
    # Write all the scans (on and off)
    j = 0
    for i, lam in enumerate(aor.dlam_map):
        filename = os.path.join(folder,'{0:05d}_{1:s}_scan_off.scn'.format(j,aor.objName))
        writeFile(filename, aor, i, off=True)
        j+=1
        filename = os.path.join(folder,'{0:05d}_{1:s}_scan.scn'.format(j,aor.objName))
        writeFile(filename, aor, i, off=True)
        j+=1
    print('All files written')
    
    
def writeFile(filename, aor, i, off=False):
    """Generic scan taken from obsmaker, it should be updated"""
    import time
    with open(filename, 'w') as f:
        f.write('# Time stamp at last update: ' + str(time.time()) + '\n')
        f.write('#    ASTRONOMY\n')
        f.write('%s%s%s' % ("AOR_ID".ljust(12),  # adjust ljust param
                              ('"' + aor.aorID + '"').ljust(20), '# from DCS\n'))
        f.write('%s%s%s' % ("OBSERVER".ljust(12),  # adjust ljust param
                              ('"' + aor.observer + '"').ljust(20), '# from DCS\n'))
        f.write('%s%s%s' % ("FILEGP_R".ljust(12),
                               ('"' + aor.fileGroupIdR + '"').ljust(20),
                               '# file group id RED for DPS use\n'))
        f.write('%s%s%s' % ("FILEGP_B".ljust(12),
                               ('"' + aor.fileGroupIdB + '"').ljust(20),
                               '# file group id BLUE for DPS use\n'))
        f.write('%s%s%s' % ("OBSTYPE".ljust(12),
                               ('"' + aor.obsType + '"').ljust(20),
                               '# Observation type for DPS use\n'))
        f.write('%s%s%s' % ("SRCTYPE".ljust(12),
                               ('"' + aor.sourceType + '"').ljust(20),
                               '# Source type for DPS use\n'))
        f.write('%s%s%s' % ("INSTMODE".ljust(12),
                               ('"' + aor.obsPlanMode + '"').ljust(20),
                               '# Instrument mode\n'))
        f.write('%s%s%s' % ("OBJ_NAME".ljust(12),
                               ('"' + aor.objName + '"').ljust(20),
                               '# Name of astronomical object observed\n'))
        if aor.naifId != "":
            f.write('%s%s%s' % ("NAIF_ID".ljust(12),
                                   (aor.naifId).ljust(20),
                                   '# NAIF ID of object observed\n'))
        f.write('%s%s%s' % ("REDSHIFT".ljust(12),
                               str(aor.redshift).ljust(20),
                               '# redshift of the source (z)\n'))
        f.write('%s%s%s' % ("COORDSYS".ljust(12),
                               ('"' + aor.coordSys + '"').ljust(20),
                               '# Target coordinate system\n'))
        f.write('%s%s%s' % ("OBSLAM".ljust(12),  # adjust ljust param
                               str(aor.posLonN).ljust(20), '# in deg\n'))
        f.write('%s%s%s' % ("OBSBET".ljust(12),  # adjust ljust param
                               str(aor.posLatN).ljust(20), '# in deg\n'))
        f.write('%s%s%s' % ("DET_ANGL".ljust(12),  # adjust ljust param
                               str("%.3f" % aor.detangle).ljust(20),
                               '# Detector y-axis EofN\n'))
        f.write('%s%s%s' % ("CRDSYSMP".ljust(12),  # adjust ljust param
                               ('"' + aor.mapCoordSys + '"').ljust(20),
                               '# Mapping coordinate system\n'))
        if off:
            f.write('%s%s%s' % ("DLAM_MAP".ljust(12),
                                   str("%.1f" % 0.).ljust(20), '# arcsec\n'))
            f.write('%s%s%s' % ("DBET_MAP".ljust(12),
                                   str("%.1f" % 0.).ljust(20), '# arcsec\n'))
        else:            
            f.write('%s%s%s' % ("DLAM_MAP".ljust(12),
                                str("%.1f" % aor.dlam_map[i]).ljust(20), '# arcsec\n'))
            f.write('%s%s%s' % ("DBET_MAP".ljust(12),
                                str("%.1f" % aor.dbet_map[i]).ljust(20), '# arcsec\n'))
        if aor.instmode == "OTF_TP":
            if off:
                f.write('%s%s%s' % ("SKYSPEED".ljust(12),
                                       str("%.1f" % 0.0).ljust(20),
                                       '# OTF sky scan speed, arcsec/s\n'))                
            else:
                f.write('%s%s%s' % ("SKYSPEED".ljust(12),
                                       str("%.1f" % aor.scanspeed[i]).ljust(20),
                                       '# OTF sky scan speed, arcsec/s\n'))
            f.write('%s%s%s' % ("VELANGLE".ljust(12),
                str("%.1f" % aor.velangle[i]).ljust(20),
                '# Angle of the velocity vector for OTF scan, EofN in deg\n'))
            f.write('%s%s%s' % ("TRK_DRTN".ljust(12),
                str("%.1f" % aor.timePerPoint).ljust(20),
                '# Duration of OTF scan\n'))
        f.write('%s%s%s' % ("CRDSYSOF".ljust(12),
            ('"' + aor.offCoordSys + '"').ljust(20),
            '# Off position coordinate system\n'))
        if off:
            f.write('%s%s%s' % ("DLAM_OFF".ljust(12),
                                   str("%.1f" % aor.dlam_off).ljust(20), '# arcsec\n'))
            f.write('%s%s%s' % ("DBET_OFF".ljust(12),
                                   str("%.1f" % aor.dbet_off).ljust(20), '# arcsec\n'))
        else:
            f.write('%s%s%s' % ("DLAM_OFF".ljust(12),
                                str("%.1f" % 0.).ljust(20), '# arcsec\n'))
            f.write('%s%s%s' % ("DBET_OFF".ljust(12),
                                str("%.1f" % 0.).ljust(20), '# arcsec\n'))            
        f.write('%s%s%s' % ("PRIMARAY".ljust(12),
            ('"' + aor.primeArray + '"').ljust(20),
            '# Primary array\n'))
        if off:
            f.write('%s%s%s' % ("LOSF_UPD".ljust(12),
                                str(0).ljust(20),
                                '# 0/1/2  block/allow/force updates\n'))
        else:            
            f.write('%s%s%s' % ("LOSF_UPD".ljust(12),
                                str(aor.losFocusUpdate).ljust(20),
                                '# 0/1/2  block/allow/force updates\n'))
        if aor.nodType != 'OTF_MAP':
            f.write('%s%s%s' % ("NODPATT".ljust(12),
                                ('"' + aor.nodPattern + '"').ljust(20),
                                '# Nod pattern\n'))
        f.write('\n#    DICHROIC SETTING\n')
        f.write('%s%s%s' % ("DICHROIC".ljust(12),
                            str(aor.dichroic).ljust(20),
                            '# Dichroic wavelength in um\n'))
        f.write('\n#    GRATING\n# Blue\n')
        f.write('%s%s%s' % ("G_ORD_B".ljust(12),
                            str(aor.orderBlue).ljust(15),
                            '# Blue grating order to be used\n'))
        f.write('%s%s%s' % ("G_FLT_B".ljust(12),
                            str(aor.filterBlue).ljust(15),
                            '# Filter number for Blue\n'))
        f.write('%s%s%s' % ("G_WAVE_B".ljust(12),
                            str("%.3f" % aor.waveBlue).ljust(15),
                            '# Wavelength to be observed in um INFO ONLY\n'))
        f.write('%s%s%s' % ("RESTWAVB".ljust(12),
                            str("%.3f" % aor.restWaveBlue).ljust(15),
                            '# Reference wavelength in um\n'))
        f.write('%s%s%s' % ("G_CYC_B".ljust(12),
                            str(aor.gratingCyclesB).ljust(15),
                            '# The number of grating cycles (up-down)\n'))
        f.write('%s%s%s' % ("G_STRT_B".ljust(12),
                            str(aor.gratingBlue).ljust(15),
                            '# absolute starting value in inductosyn units\n'))
        f.write('%s%s%s' % ("G_PSUP_B".ljust(12),
                            str(aor.gratingPosUpB).ljust(15),
                            '# number of grating position up in one cycle\n'))
        f.write('%s%s%s' % ("G_SZUP_B".ljust(12),
                            str(aor.gratingStepSizeUpB).ljust(15),
                            '# step size on the way up; same unit as G_STRT\n'))
        f.write('%s%s%s' % ("G_PSDN_B".ljust(12),
                            str(aor.gratingPosDownB).ljust(15),
                            '# number of grating position down in one cycle\n'))
        f.write('%s%s%s' % ("G_SZDN_B".ljust(12),
                            str(aor.gratingStepSizeDownB).ljust(15),
                            '# step size on the way down; same unit as G_STRT\n'))
        f.write('# Red\n')
        f.write('%s%s%s' % ("G_WAVE_R".ljust(12),
                            str("%.3f" % aor.waveRed).ljust(15),
                            '# Wavelength to be observed in um INFO ONLY\n'))
        f.write('%s%s%s' % ("RESTWAVR".ljust(12),
                            str("%.3f" % aor.restWaveRed).ljust(15),
                            '# Reference wavelength in um\n'))
        f.write('%s%s%s' % ("G_CYC_R".ljust(12),
                            str(aor.gratingCyclesR).ljust(15),
                            '# The number of grating cycles (up-down)\n'))
        f.write('%s%s%s' % ("G_STRT_R".ljust(12),
                            str(aor.gratingRed).ljust(15),
                            '# absolute starting value in inductosyn units\n'))
        f.write('%s%s%s' % ("G_PSUP_R".ljust(12),
                            str(aor.gratingPosUpR).ljust(15),
                            '# number of grating position up in one cycle\n'))
        f.write('%s%s%s' % ("G_SZUP_R".ljust(12),
                            str(aor.gratingStepSizeUpR).ljust(15),
                            '# step size on the way up; same unit as G_STRT\n'))
        f.write('%s%s%s' % ("G_PSDN_R".ljust(12),
                            str(aor.gratingPosDownR).ljust(15),
                            '# number of grating position down in one cycle\n'))
        f.write('%s%s%s' % ("G_SZDN_R".ljust(12),
                            str(aor.gratingStepSizeDownR).ljust(15),
                            '# step size on the way down; same unit as G_STRT\n'))
        f.write('\n#    RAMP\n')
        f.write('%s%s%s' % ("RAMPLN_B".ljust(12),
                            str(aor.rampLengthB).ljust(15),
                            '# number of readouts per blue ramp\n'))
        f.write('%s%s%s' % ("RAMPLN_R".ljust(12),
                            str(aor.rampLengthR).ljust(15),
                            '# number of readouts per red ramp\n'))
        f.write('\n#    CHOPPER\n')
        f.write('%s%s%s' % ("C_SCHEME".ljust(12),
                            ('"' + aor.chopScheme + '"').ljust(15),
                            '# Chopper scheme; 2POINT or 4POINT\n'))
        f.write('%s%s%s' % ("C_CRDSYS".ljust(12),
                            ('"' + aor.chopCoordSys + '"').ljust(15),
                            '# Chopper coodinate system\n'))
        f.write('%s%s%s' % ("C_AMP".ljust(12),
                            str(aor.chopAmplitude).ljust(15),
                            '# chop amplitude in arcsec\n'))
        f.write('%s%s%s' % ("C_TIP".ljust(12),
                            str(aor.chopTip).ljust(15), '# fraction\n'))
        f.write('%s%s%s' % ("C_BEAM".ljust(12),
                            str("%.1f" % aor.chopBeam).ljust(15), '# nod phase\n'))
        f.write('%s%s%s' % ("C_POSANG".ljust(12),
                            str(aor.chopPosAngle).ljust(15), '# deg, S of E\n'))
        f.write('%s%s%s' % ("C_CYC_B".ljust(12),
                            str(aor.chopCyclesB).ljust(15),
                            '# chopping cycles per grating position\n'))
        f.write('%s%s%s' % ("C_CYC_R".ljust(12),
                            str(aor.chopCyclesR).ljust(15),
                            '# chopping cycles per grating position\n'))
        f.write('%s%s%s' % ("C_PHASE".ljust(12),
                            str("%.1f" % float(aor.chopPhase)).ljust(15),
                            '# chopper signal phase shift relative to R/O in deg\n'))
        f.write('%s%s%s' % ("C_CHOPLN".ljust(12),
                            str(aor.chopLength).ljust(15),
                            '# number of readouts per chop position\n'))
        f.write('\n#    CAPACITORS\n')
        f.write('%s%s%s' % ("CAP_B".ljust(12),
                            str(aor.capB).ljust(15),
                            '# Integrating capacitors in pF\n'))
        f.write('%s%s%s' % ("CAP_R".ljust(12),
                            str(aor.capR).ljust(15),
                            '# Integrating capacitors in pF\n'))
        f.write('\n#    CONVERTER\n# Blue\n')
        f.write('%s%s%s' % ("ZBIAS_B".ljust(12),
                            str("%.3f" % aor.zbiasB).ljust(15),
                            '# Voltage in mV\n'))
        f.write('%s%s%s' % ("BIASR_B".ljust(12),
                            str("%.3f" % aor.biasrB).ljust(15), '# Voltage in mV\n'))
        f.write('%s%s%s' % ("HEATER_B".ljust(12),
                            str("%.3f" % aor.heaterB).ljust(15), '# Voltage in mV\n'))
        f.write('# Red\n')
        f.write('%s%s%s' % ("ZBIAS_R".ljust(12),
                            str("%.3f" % aor.zbiasR).ljust(15),
                            '# Voltage in mV\n'))
        f.write('%s%s%s' % ("BIASR_R".ljust(12),
                            str("%.3f" % aor.biasrR).ljust(15), '# Voltage in mV\n'))
        f.write('%s%s%s' % ("HEATER_R".ljust(12),
                            str("%.3f" % aor.heaterR).ljust(15), '# Voltage in mV\n'))
        f.write('\n#    CALIBRATION SOURCE\n')
        f.write('%s%s%s' % ("CALSTMP".ljust(12),
                            str(aor.calstmp).ljust(15), '# Kelvin\n'))
        f.write('\nHERE_COMETH_THE_END\n')

class AOR(object):
    """AOR from a list of AORs"""
    
    def __init__(self, aorfile, title):
        # Read the file
        tree = ET(file=aorfile)
        vector = tree.find('list/vector')
        requests = [item for item in vector.findall('Request')]
        titles = [item.text for item in vector.findall('Request/title')]
        PI = tree.find('list/ProposalInfo/Investigator')
        self.observer = PI.attrib['FirstName'] + ' ' + PI.attrib['LastName']
        # Select the requested title
        titles = np.array(titles)
        idx = np.argwhere(titles==title)
        self.request = requests[idx[0][0]]
        # Check the obsplan
        self.obsPlanMode = self.request.findall('instrument/data/ObsPlanMode')[0].text
        # Order and dichroic
        self.order = self.request.findall('instrument/data/order')[0].text
        dichroic = self.request.findall('instrument/data/Dichroic')[0].text
        if dichroic == '105_micron':
            self.dichroic = 105
        else:
            self.dichroic = 130
        # Astronomy
        self.aorID = self.request.findall('instrument/data/aorID')[0].text
        self.objName = self.request.findall('target/name')[0].text
        # Take out blanks out of object name
        self.objName = self.objName.replace(" ", "")
        self.sourceType = self.request.findall('instrument/data/SourceType')[0].text
        # Check if equatorial is true
        self.redshift = self.request.findall('instrument/data/Redshift')[0].text
        self.coordSys = self.request.findall('target/position/coordSystem/equinoxDesc')[0].text
        self.mapCoordSys = 'J2000'
        self.offCoordSys = 'J2000'
        self.posLonN = self.request.findall('target/position/lon')[0].text
        self.posLatN = self.request.findall('target/position/lat')[0].text
        self.timePerPoint = float(self.request.findall('instrument/data/TimePerPoint')[0].text)
        self.dlam_off = float(self.request.findall('instrument/data/RAOffset')[0].text)
        self.dbet_off = float(self.request.findall('instrument/data/DecOffset')[0].text)
        self.primeArray = self.request.findall('instrument/data/PrimeArray')[0].text
        # Nod
        self.nodType = self.request.findall('instrument/data/NodType')[0].text
        # Dichroic
        self.dichroic = self.request.findall('instrument/data/Dichroic')[0].text
        self.dichroic = self.dichroic[:3]
        # Grating
        # Central wavelengths
        self.waveRed = float(self.request.findall('instrument/data/WavelengthRed')[0].text)
        self.restWaveRed = self.waveRed
        self.waveBlue = float(self.request.findall('instrument/data/WavelengthBlue')[0].text)
        self.restWaveBlue = self.waveBlue
        # Choose order and filter for the blue channel
        bluewave = float(self.waveBlue) * (1 + float(self.redshift))
        # Default values
        if bluewave < 70:
            self.orderBlue = 2
            self.filterBlue = 2
        else:
            self.orderBlue = 1
            self.filterBlue = 1
        # Capacitors
        self.capB = 1330
        self.capR = 1330
        # Converter
        self.zbiasB = 75.000
        self.biasrB = 0.000
        self.heaterB = 0.000
        self.zbiasR = 60.000
        self.biasrR = 0.000
        self.heaterR = 0.000
        # Cal source
        self.calstmp = 0.0
        
        # Build the group ID
        self.fileGroupIdR = self.objName + '_R_'+ '{0:.1f}'.format(self.restWaveRed)
        self.fileGroupIdB = self.objName + '_B_'+ '{0:.1f}'.format(self.restWaveBlue)
        
        # Features peculiar of the observation mode
        if self.obsPlanMode == 'OTF_MAP':
            self.instmode = 'OTF_TP'
            self.losFocusUpdate = 1 # Allow rewind for OTF

            # Defaults for OTF_MAP
            self.gratingCyclesB = 1
            self.gratingCyclesR = 1
            self.gratingPosUpB = 1
            self.gratingPosUpR = 1
            self.gratingPosDownB = 0
            self.gratingPosDownR = 0
            self.gratingStepSizeUpB = 600
            self.gratingStepSizeUpR = 547
            self.gratingStepSizeDownB = 0
            self.gratingStepSizeDownR = 0
            self.rampLengthB = 32
            self.rampLengthR = 32
            # Chopping
            self.chopPosAngle = 0
            self.chopScheme = '2POINT'
            self.chopCoordSys = 'TARF'
            self.chopLength = 64
            self.chopAmplitude = 0.0
            self.chopTip = 0.0
            self.chopBeam = 0.0
            self.chopPhase = 0.0
            self.chopCyclesB = 16
            self.chopCyclesR = 16
            self.obsType = 'OBJECT'
            self.naifId = ''
            self.read_OTF()
            
    def read_OTF(self):
        
        # Read the map
        scanpath = 'instrument/scanParams/sspot.sofia.data.fifils.ScanParameters/'
        dlam_map = [item.text for item in self.request.findall(scanpath+'deltaX')]
        dbet_map = [item.text for item in self.request.findall(scanpath+'deltaY')]
        scanspeed = [item.text for item in self.request.findall(scanpath+'scanSpeed')]
        scandirection = [item.text for item in self.request.findall(scanpath+'scanDirection')]
        velangle = []
        for sc in scandirection:
            if sc == '+X': 
                va = 90
            elif sc == '-X':
                va = 270
            elif sc == '+Y':
                va = 0
            elif sc == '-Y':
                va = 180
            velangle.append(va)
        self.velangle = np.array(velangle, dtype=float)
        self.scanspeed = np.array(scanspeed, dtype=float)
        
        detangle = float(self.request.findall('instrument/data/MapRotationAngle')[0].text)
        self.detangle = (((detangle + 11.3) + 180 + 360) % 360) - 180
        
        # Rotation matrix
        detang = self.detangle * np.pi / 180.0
        cosa = np.cos(detang)
        sina = np.sin(detang)
        r = np.array([[cosa, -sina], [sina, cosa]])
        self.dlam_map = np.array(dlam_map, dtype='float')
        self.dbet_map = np.array(dbet_map, dtype='float')

        self.scantime = float(self.request.findall('instrument/data/TimePerPoint')[0].text)
        distance = self.scanspeed * self.scantime
        
        # Compute the last position of the scan
        dlam_end = self.dlam_map.copy()
        dbet_end = self.dbet_map.copy()

        idx = self.velangle == 90
        if np.sum(idx) > 0:
            dlam_end[idx] += distance[idx]
        idx = self.velangle == 270
        if np.sum(idx) > 0:
            dlam_end[idx] -= distance[idx]
        idx = self.velangle == 0
        if np.sum(idx) > 0:
            dbet_end[idx] += distance[idx]
        idx = self.velangle == 180
        if np.sum(idx) > 0:
            dbet_end[idx] -= distance[idx]
        x1, y1 = self.dlam_map.copy(), self.dbet_map.copy()
        x2, y2 = self.dlam_map.copy(), self.dbet_map.copy()
        x3, y3 = dlam_end.copy(), dbet_end.copy()
        x4, y4 = dlam_end.copy(), dbet_end.copy()

        mapoffsets = np.array([self.dlam_map, self.dbet_map])
        rot_mapoffsets = np.dot(np.transpose(r), mapoffsets)
        mapends = np.array([dlam_end, dbet_end])
        rot_mapends = np.dot(np.transpose(r), mapends)

        # Find the corners of the scan
        dr = 30 # case of red array, half side is 30 arcsec
        idx = velangle == 90
        if np.sum(idx) > 0:
            x1[idx] -= dr
            x2[idx] -= dr
            x3[idx] += dr
            x4[idx] += dr
            y1[idx] += dr
            y2[idx] -= dr
            y3[idx] -= dr
            y4[idx] += dr
        idx = velangle == 270
        if np.sum(idx) > 0:
            x1[idx] += dr
            x2[idx] += dr
            x3[idx] -= dr
            x4[idx] -= dr
            y1[idx] += dr
            y2[idx] -= dr
            y3[idx] -= dr
            y4[idx] += dr
        idx = velangle == 0
        if np.sum(idx) > 0:
            x1[idx] -= dr
            x2[idx] += dr
            x3[idx] += dr
            x4[idx] -= dr
            y1[idx] -= dr
            y2[idx] -= dr
            y3[idx] += dr
            y4[idx] += dr
        idx = velangle == 180
        if np.sum(idx) > 0:
            x1[idx] -= dr
            x2[idx] += dr
            x3[idx] += dr
            x4[idx] -= dr
            y1[idx] += dr
            y2[idx] += dr
            y3[idx] -= dr
            y4[idx] -= dr
        
        
        xy1 = np.array([x1, y1])
        xy2 = np.array([x2, y2])
        xy3 = np.array([x3, y3])
        xy4 = np.array([x4, y4])
        self.rxy1 = np.dot(np.transpose(r), xy1)
        self.rxy2 = np.dot(np.transpose(r), xy2)
        self.rxy3 = np.dot(np.transpose(r), xy3)
        self.rxy4 = np.dot(np.transpose(r), xy4)
