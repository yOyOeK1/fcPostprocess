
from FileActions import *
from MyCalculate import *
import sys,math,os


fa = FileActions()

if len(sys.argv) == 3:
    print( sys.argv )
    fFromArg = sys.argv[1]
    zInWorkFile = sys.argv[2]
else:
    print( """give some args !
        
        Usage: 
            fcToTabs.py [srcFile.gcode] [zToUseInSrcFile]
        
        It can process freecad grbl_81 
            pycam engrave to Z0.0 is working stock and engrave -2.0
        
        If use as:
            fcToTabs.py [srcFile.gcode] pycam3d
            postprocess gcode to marlin
            
        fcToTabs.py [srcFile.gcode] [ -2.0 | pycam | pycam3d | heeks ]
        
        only first option is doing automatic tabs! 
            
    """)
    sys.exit(1)

# find z level as a base to work on
fwl = zInWorkFile#-2.500

rapidZSafe = 10.0
sd = 0.0 #start cut at
ed = -20.0 #end cut at 
stepd = 3.5 #step z down

#tabs
tEvery = 550.00 
tW = 5.0 + 3.175 #width of the tab
tH = stepd*1.9  #height of the tab 


fRapid = 20000 # mm/min
fWorkHorizontal = 1600
fWorkVertical = 800
fFirstLayerSlower = 0.9#    multiplayer

fPath = fFromArg#"/home/yoyo/OceanBuilders/hannes_flange3/moreMoons.gcode"
relPath = fFromArg.replace(".gcode","_tabs.gcode").replace(".ngc","_correct.ngc")#"/tmp/res.gcode"
paths = []
path = []


lines = fa.loadFile(fPath)

class P:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def lineHave(line, str):
    try:
        line.index(str)
        return True
    except:
        return False

def replace(line, findStr, newValue):
    if lineHave(line, findStr):
        s = line.split(" ")
        for i,v in enumerate(s):
            if lineHave(v, findStr):
                s[i] = "%s%s" % (findStr, newValue)
                
        return " ".join(s)
    else:
        return line
    
def getV4l(line):
    v = {'orgLine':line}
    s = line.split(" ")
    for i in s:
        if i != "":
            try:
                v[i[0]] = float(i[1:])
            except:
                v[i[0]] = i[1:]
    return v


def lvToString(l):
    tr = []
    for k in l.keys():
        if k != 'orgLine':
            if k in ["G"]:
                tr.append(str( k+str(int(l[k])) ))
            else:    
                tr.append(str( k+str(l[k]) ))
    return " ".join(tr)
    
def distance(x0,y0, x1,y1):
    return math.sqrt( 
        (x1-x0)**2 + (y1-y0)**2
         )
    
def writeCorrectFile(tr, m2 = True):
    if m2:
        tr.append("M2")
    
    print("new file: ",relPath)
    fa.writeFile(relPath, "\n".join(tr) )
    print("DONE it have",len(tr),"lines")





print("pycam 3D or heeks?")
if zInWorkFile in[ "pycam3d", "heeks"]:
    print("    YES")
    
    
    
    tr = []
    lastG = 0
    for n,l in enumerate(lines[5:-2]):
        if l[0] == "G":
            l = l[0]+l[2:]
            
        else:
            l = "G%s %s"%(int(lastG),l)
            
        
        l1 = getV4l(l)
        try:
            f = l1['F']
            #f*= 60
            l = replace(l, "F", f)
        except:
            pass
        
        if lastG == 0:
            if not lineHave(l, 'Z') and not lineHave(l, 'F'):
                l = "%s F%s" % ( l, fRapid )
        
        
        tr.append(l)
        
        if l[0] == "G":
            lastG = int(l[1])
        
        #print(n,"  - ",l)
        #if n > 10:
        #    break
    if zInWorkFile in[ "heeks"]:
        print("heeks need more steps so no M2 !")
        writeCorrectFile(tr,m2=False)
    else:
        writeCorrectFile(tr)
    
    if zInWorkFile in[ "heeks"]:
        print("heeks so one more round :) ")
        print("for Z-2 !!")
        cmd = "fcToTabs.sh %s -2" %relPath
        print("so lets run it [",cmd,"]")
        print("/-------------------------\\")
        os.system(cmd)
        print("\------------------------/DONE")
        
    sys.exit(0)
else:
    print("    NO")

print("pycam ?")
if zInWorkFile == "pycam":
    print("    YES")
    
    tr = []
    lastG = 0
    rep = [
        ["G0 Z25.0000",    "G0 F%s Z10.0"%fWorkVertical],
        ["G1 Z-2.0000",     "G1 F%s Z-2.0000" %fWorkVertical],        
        ]
    
    for l in lines[44:-4]:
	
        if lineHave(l,'set feedrate'):
            pass
        else:
            #print(l)
            #sys.exit(1)
            if len(tr)>0:
                if lineHave(tr[-1], "G1"):
                    lastG = 1
                else:
                    lastG = 0
            
            for r in rep:
                l = l.replace(r[0],r[1])
                
                
                
            
            if lastG == 0 and l[1] in ['X', 'Y']:
                tr.append( "G0 F%s%s"%(fRapid, l) )
                
            elif lastG == 1 and l[1] in ['X', 'Y']:
                tr.append( "G1 F%s%s"%(fWorkHorizontal, l) )
                
            else:
                tr.append(l)
            
        
    
        #print(tr[-1])
    
    
    writeCorrectFile(tr)

    sys.exit(0)
else:
    print("    NO")

# find working layer
#create paths[ path, path ]
#path is line by line G....

print("so it's freecad ?")
fc = 0
lastOk = False
memory = {
    "G":0,
    "X":0.0,
    "Y":0.0,
    "Z":15.0,
    "F":fWorkHorizontal,
    }

for lc,l in enumerate(lines):
    isWork = False
    l1 = getV4l(l)
    
    for k in memory.keys():
        if lineHave(l, k):
            try:
                memory[k] = l1[k]
            except:
                print("error - l1 not have ",k," to store")
                pass
            pass
        else:
            l+= " %s%s"%(k,memory[k])
            
    
    
    if lineHave(l, "Z%s"%fwl):
        if lineHave(l, "G1") or lineHave(l, "G2") or lineHave(l, "G3"):
            fc+=1
            isWork = True
    
    if isWork == False and len(path)>0:
        paths.append( replace(path,"Z",0) )
        path = []
    
    if isWork == True:
        path.append( replace(l,"Z",0))
    
if len(path)>0:
    paths.append(path)
    
    

    
print( "working lines:    ",fc )
print( "working paths:    ",len(paths) )
# end find working layer


zts = []
z = sd
while( True ):
    z-= stepd
    if z <= ed:
        zts.append(ed)
        break
     
    zts.append(z)


print("z working :",zts)

distGlobTotal = 0.0
# add tabs
if 1:
    mc = MyCalculate()
    for i,p in enumerate(paths):
        #print("path nr",i," have pathlines:",len(p))
        
        dist = 0.0
        distT = 0.0
        l0 = getV4l(p[0])
        nwp = [p[0]]
        tabC = 0
        for wi,w in enumerate(p[1:]):
            tabAdded = False
            l1 = getV4l(w)
                
            p0 = P(l0['X'],l0['Y'])
            p1 = P(l1['X'],l1['Y'])
            
            if l1['X'] and l1['Y'] and l0['X'] and l0['Y']:
                d = mc.distance(p0,p1)
                dist+= d
                distT+= d
                
            #if l1['G'] == 1 and (l0['G'] in [1,2,3]):
            #    print(wi," tab data segment len",round(d,2)," dist total",round(dist,2))
            
            if l1['G'] == 1 and (l0['G'] in [1,2,3]) and d >= tW and dist >= tEvery:
                tabC+=1 
            #    print("    add")
                #print("posible tab")
                #print("    l0:    ",l0)
                #print("    l1:    ",l1)
                #print("    wpath length:",mc.distance(p0,p1) )
                #print("    wpath angle:",mc.angle(p0,p1))
                p0_0 = mc.newPoint(p0,p1,tW*0.1)
                p0_1 = mc.newPoint(p0,p1,tW*0.9)
                p0_2 = mc.newPoint(p0,p1,tW) 
                nwp.append(
                    "G1 X"+str(p0_2.x)+" Y"+str(p0_2.y)+" Z0 F"+str(fWorkHorizontal)+" (tap start)"
                     )
                nwp.append(
                    "G1 X"+str(p0_1.x)+" Y"+str(p0_1.y)+" Z0 F"+str(fWorkVertical)+" (tap pik0)"
                     )
                nwp.append(
                    "G1 X"+str(p0_0.x)+" Y"+str(p0_0.y)+" Z0 F"+str(fWorkHorizontal)+" (tap pik1)"
                     )
                tabAdded = True
                dist = 0.0
                
                    
            
            l0 = l1
            
            tAdd = l1['orgLine']
            if tabAdded:
                tAdd = replace(tAdd, "F", fWorkVertical*0.3)+" (tap end)"
            nwp.append(tAdd)
        paths[i] = nwp
        
        print("[",i,"] work path is: ",round(distT,2),"mm nwp.len",len(nwp)," old.len",len(p)," tabs added",tabC)
        distGlobTotal+= distT
        #print(p[-1])
        #print(nwp[-1])
    #end add tabs      
distGlobTotal*=len(zts)
print("Total work path length: ",round(distGlobTotal,2),"mm")
print("Working time ~ ",round((distGlobTotal/fWorkHorizontal),2),"min with feed ",fWorkHorizontal,"mm/min" )
print("With ",len(zts)," passys to get to deth")
#sys.exit(1)
tr = []
for i,p in enumerate(paths):
    
    tr.append( "(part start    "+str(i)+")" )
    #tr.append("M117 part %s/%s"%(i+1, len(paths)))
    g0 = replace( p[0], "F", fRapid ).replace("G1", "G0")
    g0 = replace( g0, "Z", rapidZSafe )
    tr.append( g0 )
    
    for iz,z in enumerate(zts):
        
        
        for w in p:
            l1 = getV4l(w)
            
            if iz == 0:
                fMulti = fFirstLayerSlower
            else:
                fMulti = 1.0
                
            if lineHave(w, "(tap pik") and z <= (ed+tH):
                l1['Z'] = z+tH
                if iz>0 and l1['Z'] > zts[iz-1]:
                    l1['Z'] = ed+tH

                lStr = lvToString(l1)
                lta = replace(lStr,"Z", l1['Z'])
                lta = replace(lta, "F", (l1['F']*fMulti) )
                tr.append( lta )
                
            elif lineHave(w, "(tap ") and z > (ed+tH):
                ts = replace(w,"Z", z)
                if lineHave(ts, 'F'):
                    #ts = replace( ts, "F", l1['F']*fMulti )
                    ts = replace(ts, "F", fWorkHorizontal ) + "(tap bud no action to shallow) "
                tr.append( ts )
                
            else:
                ts = replace(w,"Z", z)
                if lineHave(ts, 'F'):
                    ts = replace( ts, "F", l1['F']*fMulti )
                tr.append( ts )
        
    #print(p[-1])
    ll = getV4l(p[-1])
    tr.append( str( 
        "G0 X"+str(ll['X'])+" Y"+str(ll["Y"])+" Z"+str(rapidZSafe)+" F"+str(fRapid)
         ))
    
    #print(p[0])
    #print("replace F [",replace(p[0],"F", "666.00" ),"]" )
    tr.append( "(part End    "+str(i)+")" )
    tr.append("")
    tr.append("")
#print( tr )

tr.append("M2")

print('''Tab every: {:.3f} mm height of tab: {:.3f} mm width {:.2f} mm'''.format(
    tEvery, tH, tW))

fa.writeFile(relPath, ("\n".join(tr)).replace("K0.000","") )
print("File is ready: ",relPath)


