#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:51:35 2021

@author: dfadda
"""

def flightTable(aorfile):
    """
    Read the *.misxml file describing the flight
    and creates a Latex table with the description of the legs

    Parameters
    ----------
    aorfile : TYPE  string
        DESCRIPTION name and path of the *misxml file describing the flight

    Returns
    -------
    table : TYPE  string
        DESCRIPTION. Latex table with description of the legs

    """
    import xml.etree.ElementTree as ET
    #aorfile = '../test/202105_FI_MAXINE_WX12.misxml'
    tree = ET.parse(aorfile)
    root = tree.getroot()

    for flightplan in root.iter('FlightPlan'):
        flightTime = flightplan.attrib['FltTime']
        flightName = flightplan.attrib['Id']
        departure = flightplan.attrib['DepartureTime']
        arrival = flightplan.attrib['ArrivalTime']

        
    table = []
    table.append(r'\begin{table}[h]')
    table.append(r'\begin{center}')
    table.append(r'\begin{tabular}{cccccrr}')
    table.append(r'\hline')
    table.append(r'\hline')
    table.append(r'Leg & Target & AOR\_ID & Elevation & UTC start & Duration & Altitude\\')
    table.append(r'\hline')
    table.append(r'\hline')
    
    for leg in root.iter('Leg'):
        name = str(leg.find('Name').text)
        name = name.replace("_", "\_")
        start = leg.find('Start').text
        duration = leg.find('Duration').text
        altitude = leg.find('Alt').text
        planid = leg.find('ObsPlanID')
        if planid is None:
            planid = ''
        else:
            planid = str(planid.text)
            # Substitute underscore with \_
            planid = planid.replace("_", "\_")
            if planid is None:
                planid = ''
        elevation = leg.find('Elev')
        if elevation is not None:
            elstart = elevation.attrib['start']
            elend = elevation.attrib['end']
            elevation = elstart+'-'+elend
        else:
            elend = ''
            elstart=''
            elevation = ''
        ID = leg.attrib['id']
        ftype = leg.attrib['type']
        if ftype == 'Absolute':
            name = 'Climb'
        elif ftype == 'Arrival':
            name = 'Arrival'
        planid = planid.replace('None','')
        fmt = r'{0:2s} & {1:s} & {2:s} & {3:s} & {4:s} & {5:s} & {6:s}\\'
        line = fmt.format(ID, name, planid, elevation, start, duration[0:5], altitude)
        table.append(line)
        print(line)
        
    ID = planid = elevation = duration = ' '
    name = 'Landing'
    start = arrival[11:19]
    altitude = '0 ft'
    line = fmt.format(ID, name, planid, elevation, start, duration, altitude)
    table.append(line)
    #print(line)
    name = 'Total flight time'
    start = altitude = ''
    duration = flightTime
    line = fmt.format(ID, name, planid, elevation, start, duration, altitude)
    table.append(line)
    #print(line)
    table.append(r'\hline')
    table.append(r'\hline')
    table.append(r'\end{tabular}')
    table.append(r'\end{center}')
    table.append(r'\end{table}')

    return table

def parsTable(fifiparsfile):
    import json
    with open(fifiparsfile,'r') as f:
        fifipars = json.load(f)
        
    table = []
    table.append(r'\begin{table}[ht]')
    table.append(r'\begin{center}')
    table.append(r'\begin{tabular}{ll}')
    table.append(r'\hline')
    table.append(r'\hline')
    table.append(r'Chop angle in J2000 & \textbf{Counter} Clockwise from North\\')
    table.append(r'FOV angle in J2000 & \textbf{Counter} Clockwise from North (blue)\\')
    table.append(r'\hline')
    table.append(r'\hline')
    table.append(r'Focus Position (xml) & '+str(fifipars['Focus Position (xml)'])+r'mm\\')  
    table.append(r'Focus Relation & '+str(fifipars['Focus Relation'])+r'$\mu$m secondary move is -1mm Focus point move\\')
    table.append(r'Bias Voltages & 75mV Blue; 60mV Red\\')
    table.append(r'Chopper Phase & 356$^o$\\')
    table.append(r'D130/D105 switch blue M2 & [OIII]51.815$\mu$m + 5000~km/s\\')
    table.append(r'Blue grating switch positions & Home/far 44000/1910000 induct\\')
    table.append(r'Red grating switch positions & Home/far 37000/1753000 induct\\')
    table.append(r'Spexel size blue & '+str(fifipars['Spexel size blue'])+r' induct\\')
    table.append(r'Spexel size red & '+str(fifipars['Spexel size red'])+r' induct\\')
    table.append(r'\hline')
    table.append(r'\hline')
    table.append(r'TO: Focus at & '+str(fifipars['TO focus'])+r'$\mu$m\\')
    table.append(r'KOSMA: Setpoint: & -X '+str(fifipars['Setpoint X'])+' -Y '+str(fifipars['Setpoint Y'])+r' (arcsec)\\')
    table.append(r'TEL\_hardware\_status (in mm):&Instr\_rotator\_axis\_x='+str(fifipars['Instr_rotator_axis_x'])+r'\\')
    table.append(r'& Instr\_rotator\_axis\_y='+str(fifipars['Instr_rotator_axis_y'])+r'\\')
    table.append(r'In Rx\_hardware\_status (in mm):&\\')
    table.append(r'\hspace{2cm} BD130 & Rx\_cx[2] '+str(fifipars['BD130 Rx_cx']) + r'\hspace{1cm} Rx\_cy[2] '+str(fifipars['BD130 Rx_cy'])+r'\\')
    table.append(r'\hspace{2cm} BD105 & Rx\_cx[1] '+str(fifipars['BD105 Rx_cx']) + r'\hspace{1cm} Rx\_cy[1] '+str(fifipars['BD105 Rx_cy'])+r'\\')
    table.append(r'\hspace{2cm} Red   &  Rx\_cx[0] '+str(fifipars['Red Rx_cx']) + r'\hspace{1cm} Rx\_cy[0] '+str(fifipars['Red Rx_cy'])+r'\\')
    table.append(r'K-Mirror 0 Position: &'+str(fifipars['K-mirror 0 Position'])+r' Steps\\')
    table.append(r'\hline')
    table.append(r'\hline')
    table.append(r'\end{tabular}')
    table.append(r'\end{center}')
    table.append(r'\end{table}')

    return table
       
    

def runLatex(tex_filename):
    import os
    import platform
    import subprocess

    # TeX source filename
    filename, ext = os.path.splitext(tex_filename)
    path, fname = os.path.split(tex_filename)
    # the corresponding PDF filename
    pdf_filename = filename + '.pdf'
    print('pdf file name ', pdf_filename)

    # compile TeX file
    subprocess.run(['pdflatex', '-interaction=nonstopmode', 
                    '-output-directory='+path, tex_filename])

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        raise RuntimeError('PDF output not found')

    # open PDF with platform-specific command
    if platform.system().lower() == 'darwin':
        subprocess.run(['open', pdf_filename])
    elif platform.system().lower() == 'windows':
        os.startfile(pdf_filename)
    elif platform.system().lower() == 'linux':
        subprocess.run(['xdg-open', pdf_filename])
    else:
        raise RuntimeError('Unknown operating system "{}"'.format(platform.system()))
