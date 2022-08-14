#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 11:17:55 2022

@author: dfadda
"""

import requests
import os
from io import BytesIO

DCSURL = 'https://dcs.arc.nasa.gov'


class DCS(object):
    def __init__(self, url=DCSURL, username=None, password=None):
        self.url = url
        if username is None:
            # Ask for username
            self.username = input("Username: ")
        else:
            self.username = username
            
        if password is None:
            self.password = input("Password: ")            
        else:
            self.password = password
            
        # First login
        self.login()
            
        
    def login(self):
        '''
        Login into DCS
    
        Returns
        -------
        None.
    
        '''
        self.request = requests.get(self.url, auth=(self.username, self.password))
        
    def getAOR(self):
        '''
        Download AOR (xml + pdf) from DCS for an AORID.

        Returns
        -------
        AOR xml and pdf of proposal

        '''
        
    