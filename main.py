

from FileActions import *

tf = []
f = "/home/yoyo/OceanBuilders/routerPlateBigPrinter/fcDrils.gcode"
feedMove = 5000
feedWork = 30

tf.append(str(";postprocessing file\n;%s"%f))
tf.append(";------------------------")

fa = FileActions()
lines = fa.loadFile(f)

for line in lines:
    w = line.split(" ")
    if w[0] == "G81":
        x = w[3]
        y = w[4]
        tf.append(str(";%s"%line))
        tf.append(str("G0 %s %s %s F%s"% (x,y,"Z5.0", int(feedMove)) ) )
        tf.append("G0 Z0.2 F%s"%int(feedMove))
        
        tf.append("G1 Z0.0 F%s"%int(feedWork))
        tf.append("G0 Z0.1 F%s"%int(feedMove))
        
        tf.append("G1 Z-0.05 F%s"%int(feedWork))
        tf.append("G0 Z0.1 F%s"%int(feedMove))
        
        tf.append("G1 Z-0.1 F%s"%int(feedWork))
        tf.append("G0 Z0.1 F%s"%int(feedMove))
        
        tf.append("G1 Z-0.15 F%s"%int(feedWork))
        tf.append("G0 Z0.0 F%s"%int(feedMove))
        
        tf.append("G1 Z-0.2 F%s"%int(feedWork))
        
        
        tf.append("G0 Z5.0 F%s"%int(feedMove))
     

tf.append(";---------------------")        

fa.writeFile(
    f.replace(".gcode","_pp.gcode"),
    "\n".join(tf)
    )
        