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
        
    table = ''
    for leg in root.iter('Leg'):
        name = leg.find('Name').text
        start = leg.find('Start').text
        duration = leg.find('Duration').text
        altitude = leg.find('Alt').text
        planid = leg.find('ObsPlanID')
        if planid is None:
            planid = ''
        else:
            planid = planid.text
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
        fmt = '{0:s} & {1:s} & {2:s} & {3:s} & {4:s} & {5:s} & {6:s}\\\\'
        line = fmt.format(ID, name, planid, elevation, start, duration[0:5], altitude)
        print(line)

    return table