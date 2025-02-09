# -*- coding: utf-8 -*-

__title__  = "Get Openings"
__author__  = "Jakob Steiner"
__doc__ = """Version = 1.1
Date    = 24.03.2024
_____________________________________________________________________
Scans trough the project for openings. A list with clickable
links will be presented. Open a 3D view to acces and see the
selected openings. A selection Filter will be created or
update to select all openings with one click.

Inspired by the initial work of Mohamed Bedair and Andreas Draxl.
Special thanks to Erik Frits for his help.
_____________________________________________________________________
TO DO:
- to do
_____________________________________________________________________
REQUIREMENTS:
_____________________________________________________________________
[24.03.2024] - Added selection Filter
[23.03.2024] - 1.0 First Release"""

# Imports

from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.DB import *
import os, sys, math, datetime, time
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import *
from pyrevit import script

# .NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List
import time

doc         =__revit__.ActiveUIDocument.Document
uidoc       =__revit__.ActiveUIDocument
output      = script.get_output()
selection   = uidoc.Selection
timer_start = time.time()

# GET ALL OPENINGS IN THE PROJECT

# 1. List of categories
cats = [BuiltInCategory.OST_FloorOpening,
        BuiltInCategory.OST_SWallRectOpening,
        BuiltInCategory.OST_ShaftOpening,
        BuiltInCategory.OST_RoofOpening]
list_cats = List[BuiltInCategory](cats)

# 2. Create filter
multi_cat_filter = ElementMulticategoryFilter(list_cats)

# 3. Apply filter to filteredElementCollector
all_elements = FilteredElementCollector(doc)\
                .WherePasses(multi_cat_filter)\
                .WhereElementIsNotElementType()\
                .ToElements()

# Get elements for selection filter
element_ids = FilteredElementCollector(doc).OfClass(Opening).ToElementIds()
element_ids = List[ElementId](element_ids)

# 4. Declaration of a list to contains list of wanted element properties
data = []

# 5. Collect information about the object and put it into in the data list.
for e in all_elements:
    el = []
    el.append(e.Name)
    el.append(e.Id)
    # add IFC Classification if parameter exist
    e_link = output.linkify(e.Id)
    el.append(e_link)
    data.append(el)

# # Get names of current selection filters in doc an print them
# namedFilters = FilteredElementCollector(doc).OfClass(FilterElement).ToElements()
# for nF in namedFilters:
#     print (nF.Name) # print names
#     print (nF.Id) # print Id

# Get All Selection Filters
all_sel_filters  = FilteredElementCollector(doc).OfClass(SelectionFilterElement).ToElements()
dict_sel_filters = {f.Name: f for f in all_sel_filters}

t = Transaction(doc, 'Create Openings Filter')
t.Start()

# Selection Filter Name
new_filter_name = '0_ShaftOpenings'

# Create new if doesn't exist
if new_filter_name not in dict_sel_filters:
    new_fil = SelectionFilterElement.Create(doc, new_filter_name)
    new_fil.AddSet(element_ids)
    print ('Created a filter called : {}'.format(new_filter_name))

# Update if already exists
else:
    existing_fil = dict_sel_filters[new_filter_name]
    existing_fil.AddSet(element_ids)
    print ('Updated a filter called : {}'.format(new_filter_name))

t.Commit()

# ╦═╗╔═╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ╠╦╝║╣ ╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╚═╚═╝╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================

output.print_md("#### There are {} shaftopenings in the project.".format(len(all_elements))) # TO DO Output link for all.
if data:
    output.print_table(table_data=data, title="Shafts:", columns=["Family" ,"ElementId", "Select/Show Element"])
    #output.print_md("#####Total {} WDB/WA elements has been updated.".format(len(data)))
else:
    output.print_md("#####There are no shaft openings in the project")

# End
output.print_md('---')
output.print_md('#### Script has finished in {}s'.format(time.time() - timer_start))