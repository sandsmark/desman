#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration - the python way
------------------------------

Fuck.
"""

####                 ####
# Generic Configuration #

# Path to where Lollercoaster is installed:
PATH = "/home/cassarossa/itk/sandsmark/prosjekter/lollercoaster"

# Key used to authenticate communication:
KEY = "L%Fdfffd¤T¤%&//¤#RQWERFWE%T har har har, I'm an incredib"

####                ####
# Tester configuration #

# Local tests to run:
LOCAL_TESTS = ('apache_local', 'ssh_local')

# Port for the tester to listen on:
TESTER_PORT = 65000

# Max. number of threads:
MAX_CHILDREN = 10

# Path to tests:
TESTS_PATH = PATH + "/tests/"
