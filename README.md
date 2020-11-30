# fcPostprocess

set of functions for postprocessing pycam 0.5.1, heeks 1.5.0 and path coming from feecad (path workspace)

freecad option have build in option to generate automatic tabs to hold stock material wile it's cut out. :)



give some args !
        
        - Usage: 
            fcToTabs.py [srcFile.gcode] [zToUseInSrcFile]
        
        - It can process freecad grbl_81 
            pycam engrave to Z0.0 is working stock and engrave -2.0
        
        - If use as:
            fcToTabs.py [srcFile.gcode] pycam3d
            postprocess gcode to marlin
            
        - fcToTabs.py [srcFile.gcode] [ -2.0 | pycam | pycam3d | heeks ]
        
        - only first option is doing automatic tabs! 