# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Identification of Potential Hydraulic Str.py
# Created on: 2024-09-21 22:16:33.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: Identification of Potential Hydraulic Str <Boundry> <Forest_Roads> <Contour> 
# Description: Coded by Dr. Taha Yasin HATAY 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Paralel işlem ayarını 0 yaparak tek çekirdek modunda çalıştır
arcpy.env.parallelProcessingFactor = "0"
arcpy.AddWarning("Parallel Processing Factor set 0")

# Script arguments

Boundry = arcpy.GetParameterAsText(0)
Forest_Roads = arcpy.GetParameterAsText(1)
Contour = arcpy.GetParameterAsText(2)

# Local variables:
CreateTin = arcpy.env.scratchGDB + "\\CreateTin"
CreateTin1_T = arcpy.env.scratchGDB + "\\CreateTin1_T"
Tin1_Clip = arcpy.env.scratchGDB + "\\Tin1_Clip"
Fill_CreateT1 = arcpy.env.scratchGDB + "\\Fill_CreateT1"
FlowDir_Fill1 = arcpy.env.scratchGDB + "\\FlowDir_Fill1"
Basin_FlowDi1 = arcpy.env.scratchGDB + "\\Basin_FlowDi1"
RasterT_Basin_F1 = arcpy.env.scratchGDB + "\\RasterT_Basin_F1"
FlowAcc_Flow1 = arcpy.env.scratchGDB + "\\FlowAcc_Flow1"
Con_FlowAcc_1 = arcpy.env.scratchGDB + "\\Con_FlowAcc_1"
StreamO_Con_1 = arcpy.env.scratchGDB + "\\StreamO_Con_1"
StreamT_StreamO1 = arcpy.env.scratchGDB + "\\StreamT_StreamO1"
StreamT_StreamO1_Select = arcpy.env.scratchGDB + "\\StreamT_StreamO1_Select"
Akarsu_Yatak_Join = arcpy.env.scratchGDB + "\\Akarsu_Yatak_Join"
Akarsu_Yatak_Join__4_ = Akarsu_Yatak_Join
Akarsu_Yatak_Join__2_ = Akarsu_Yatak_Join__4_

# Process: Create TIN
arcpy.CreateTin_3d(CreateTin, "", Contour + " Elevation Hard_Line <None>", "DELAUNAY")
arcpy.AddWarning("TIN process is finished!")

# Process: TIN to Raster
arcpy.TinRaster_3d(CreateTin, CreateTin1_T, "FLOAT", "LINEAR", "CELLSIZE 5", "1")
arcpy.AddWarning("TIN to Raster process is finished!")

# Process: Clip
arcpy.Clip_management(CreateTin1_T, "#", Tin1_Clip, Boundry, "-3.402823e+038", "NONE", "NO_MAINTAIN_EXTENT")
arcpy.AddWarning("Clip process is finished!")

# Process: Fill
arcpy.gp.Fill_sa(Tin1_Clip, Fill_CreateT1, "")
arcpy.AddWarning("Fill process is finished!")

# Process: Flow Direction
arcpy.gp.FlowDirection_sa(Fill_CreateT1, FlowDir_Fill1, "NORMAL", "#", "D8")
arcpy.AddWarning("Flow Direction is finished!")

# Process: Basin
arcpy.gp.Basin_sa(FlowDir_Fill1, Basin_FlowDi1)
arcpy.AddWarning("Basin is finished!")

# Process: Raster to Polygon
arcpy.RasterToPolygon_conversion(Basin_FlowDi1, RasterT_Basin_F1, "SIMPLIFY", "VALUE")
arcpy.AddWarning("Raster to Polygon (Basin) is finished!")

# Process: Flow Accumulation
arcpy.gp.FlowAccumulation_sa(FlowDir_Fill1, FlowAcc_Flow1, "", "FLOAT", "D8")
arcpy.AddWarning("Flow Accumulation is finished!")

# Process: Con (Flow Accumulation Threshold)
arcpy.gp.Con_sa(FlowAcc_Flow1, FlowDir_Fill1, Con_FlowAcc_1, FlowDir_Fill1, "")
arcpy.AddWarning("Con is finished!")

# Process: Stream Order
arcpy.gp.StreamOrder_sa(Con_FlowAcc_1, FlowDir_Fill1, StreamO_Con_1, "STRAHLER")
arcpy.AddWarning("Stream Order is finished!")

# Process: Stream to Feature
arcpy.gp.StreamToFeature_sa(StreamO_Con_1, FlowDir_Fill1, StreamT_StreamO1, "SIMPLIFY")
arcpy.AddWarning("Stream to Feature is finished!")

# Process: Select streams
arcpy.Select_analysis(StreamT_StreamO1, StreamT_StreamO1_Select, '"grid_code" >= 5')
arcpy.AddWarning("Stream selection set to grid_code>=5 and finished!")
arcpy.AddWarning("This value can be changed within the code.")

# Process: Spatial Join (to find intersections with forest roads)
arcpy.SpatialJoin_analysis(Forest_Roads, StreamT_StreamO1_Select, Akarsu_Yatak_Join, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT")
arcpy.AddWarning("Spatial Join is finished!")

# Process: Add Field (Potential Streams)
arcpy.AddField_management(Akarsu_Yatak_Join, "Potential_St", "FLOAT")
arcpy.AddWarning("Add Field is finished!")

# Process: Calculate Field (using Python parser instead of VB)
arcpy.CalculateField_management(Akarsu_Yatak_Join__4_, "Potential_St", "!Join_Count!", "PYTHON_9.3")
arcpy.AddWarning("Calculate Field is finished!")

# Process: Join Field
arcpy.JoinField_management(Forest_Roads, "OBJECTID", Akarsu_Yatak_Join__2_, "OBJECTID", "Potential_St")
arcpy.AddWarning("Join Field is finished!")

arcpy.AddWarning("All the process is complete. All intermediate elements are saved in the ArcGIS folder in scratchgdb.gdb. Control can be performed from there.")
