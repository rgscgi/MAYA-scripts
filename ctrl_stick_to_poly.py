#  Sticky Ctrls 
# copyright by Ronin  Garay 

import maya.cmds as cmds
from functools import partial

class Structure:
    
    def __init__(self , objectName ):
        self.__group = 'grp_' + objectName
        self.__joints = 'grp_jnt_' + objectName
        self.__control = 'grp_ctrl_' + objectName
        
        self.__count = 1
        while cmds.objExists( "ctrl_"+objectName + '_' + str(self.__count) ):
            self.__count += 1
    
    def GetGroup(self):
        return self.__group
        
    def GetJoint(self):
        return self.__joints
        
    def GetControl(self):
        return self.__control
    
    def GetCount(self):
        return self.__count
        
        
    #********************* Setup the structure if doesn't exist  *********************
    def createStructure(self):
        #************   Create a surfaceShader if it doesn`t exist  **********************************

        shader = 'mat_blue_ctrl'
        
        if not cmds.objExists("mat_blue_ctrl"):
            shader = cmds.shadingNode("surfaceShader",asShader=True , n = 'mat_blue_ctrl')
            cmds.setAttr(shader+".outColor" , 0 , 0 , 1 )
            shading_group = cmds.sets(renderable=True,noSurfaceShader=True,empty=True , n = shader+'SG')
            cmds.connectAttr('%s.outColor' %shader ,'%s.surfaceShader' %shading_group)
            
        if not cmds.objExists( self.__group ) and not cmds.objExists( self.__joints ) and not cmds.objExists( self.__control ):
            cmds.group( empty = True , n = self.__group )
            cmds.group( empty = True , n = self.__control )
            cmds.group( empty = True , n = self.__joints )
            cmds.parent( self.__joints , self.__group )
            cmds.parent( self.__control , self.__group )   
            
#******************************************************************************************************************
#************************** Create a 2 group over object to maintain the same values  *****************************
#******************************************************************************************************************

def _2GrpUp( object ):
    position = cmds.xform(object, q = True,ws =True ,  piv = True )
    rotate = cmds.xform(object, q = True, ws = True, ro = True )
    cmds.group( em = True , n = ("grp_drv_"+object))
    cmds.group( em = True , n = ("grp_pos_"+object))
    cmds.parent( ("grp_pos_"+object) , ("grp_drv_"+object))   
    cmds.xform( ("grp_drv_"+object) , t = [position[0] , position[1] , position[2] ])
    cmds.xform( ("grp_drv_"+object) , ro = [rotate[0] , rotate[1] , rotate[2] ])
    cmds.parent( object , ("grp_pos_"+object))
    cmds.makeIdentity( object, apply = True , t = True , r = True , s = True , n = False , pn = True)
    return("grp_drv_"+object)  
    

#******************************************************************************************************************
#******************  Create two group upper object to set up channels to 0 ****************************************
#******************************************************************************************************************

def twoGrpUP( object ):
    position = cmds.xform(object, q = True,ws =True ,  piv = True )
    rotate = cmds.xform(object, q = True, ws = True, ro = True )
    pivo = cmds.xform( object ,  q = True , piv = True )
    cmds.group( em = True , n = ("grp_drv_"+object))
    cmds.group( em = True , n = ("grp_pos_"+object))
    cmds.parent( ("grp_pos_"+object) , ("grp_drv_"+object))   
    cmds.xform( ("grp_drv_"+object) , t = [position[0] , position[1] , position[2] ])
    cmds.xform( ("grp_drv_"+object) , ro = [rotate[0] , rotate[1] , rotate[2] ])
    cmds.parent( object , ("grp_pos_"+object))
    if cmds.nodeType(object)!='joint':
        cmds.makeIdentity( object, apply = True , t = True , r = True , s = True , n = False , pn = True)    
    cmds.xform( ("grp_drv_" + object) , t = [ position[0] , position[1] , position[2] ] )
    
    return("grp_drv_"+object)    
 
#************************************************************************************************************************************   
#********************** create a group to substract traslation and rotation values to keep the same position  ***********************	
#************************************************************************************************************************************

def GrpSubsTranslation(object):
    #***************   get object values ***************************
	position = cmds.xform(object,q=True,t=True)
	pivot = cmds.xform(object,q=True,piv=True)
	#**************   get object parent  ***********************
	parent = cmds.listRelatives(object,p=True)
	
	#**************   create a subctract group  and parented to parent object ***********************
	group = cmds.group(empty=True,n=("grp_pto_sub_"+object))
	cmds.parent(group , parent[0])
	
	if cmds.nodeType(object)!="joint":
		cmds.xform(group ,t=[pivot[0] , pivot[1] , pivot[2]]);
		cmds.makeIdentity(group,apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.parent(object,group)
	mulDiv = cmds.createNode( 'multiplyDivide', n=("md_"+object) )
	cmds.connectAttr( (object+".translate") , (mulDiv+".input1") , f=True)
	cmds.connectAttr( (mulDiv+".output") , (group+".translate"),f=True)
	cmds.setAttr(mulDiv+".input2",-1,-1,-1)   
	

def StickObjectToMesh( vertex , mesh ):
    #***********   Get parent name ******************
    
    ObjectParent = cmds.listRelatives( mesh , p = True )    
    #***********   Get object position ******************
    position = cmds.xform(vertex, q = True, ws = True, t = True)
    #******* Create a group driven by pointOnPolyContraint **********
    groupName = cmds.group(em=True, name=("grp_ptc_"+mesh))
    cmds.parent(groupName,ObjectParent[0])
    #******* Get the UV map relationed with the vtx **********
    mapList = cmds.polyListComponentConversion(vertex,fv=-True , tuv=True)
    #******* Create a pointOnPolyContraint **********
    contraintNames = cmds.pointOnPolyConstraint( vertex, groupName,mo=False,o=[0,0,0],w=1 )
    #*************  Disconnect rotation  chanel  ****************************************
    mel.eval( "CBdeleteConnection "+groupName+".rotateX;")
    mel.eval( "CBdeleteConnection "+groupName+".rotateY;")
    mel.eval( "CBdeleteConnection "+groupName+".rotateZ;")
    #******* Get U and V values from map array **********
    uvvalues = cmds.polyEditUV(mapList,q=True)
    contraintAttr = cmds.listAttr(contraintNames[0] , k = True)
    #******* Assign the U and V values respectively from maplist **********
    cmds.setAttr( (contraintNames[0] + "." + contraintAttr[10] ) , uvvalues[0])
    cmds.setAttr( (contraintNames[0] + "." + contraintAttr[11] ) , uvvalues[1])
    groupDrv = _2GrpUp(mesh)
    cmds.parent(groupDrv,groupName)
    GrpSubsTranslation(mesh)	   
  

#*********************************************************************************************
#**********************************   Main program  ******************************************
#*********************************************************************************************

def stickyCtrl():
    
    radius = cmds.textFieldGrp( radiusText , q = True , text = True )
    
    vtx_list = cmds.ls(sl = True)
    
    
        
    #********************************  Create and setup  **********************************************
    for vtxObject in vtx_list:
        if 'vtx' in vtxObject: 
            
            #**************  remove type and .vtx[] characters from string  *********************
            dot_begin = vtxObject.find('.')
            underscored_begin = ( vtxObject.find('_') + 1 )
            meshName = vtxObject[underscored_begin:dot_begin]
            
            structure = Structure(meshName)
            structure.createStructure()
            count = structure.GetCount()
            print count
            
            #*********************  get vertex position value ***********************************
            position = cmds.xform( vtxObject , q = True ,ws = True , t = True)
            joint = cmds.joint( n = ( 'jnt_' + meshName + '_' + str(count)  ) , p =  [position[0] , position[1] , position[2] ] )
            sphere = cmds.sphere( n = "ctrl_"+meshName + '_' + str(count) ,r = radius , ch = False )
            
            cmds.setAttr(sphere[0]+"Shape.castsShadows", 0)
            cmds.setAttr( sphere[0]+"Shape.receiveShadows", 0)
            cmds.setAttr( sphere[0]+"Shape.motionBlur", 0)
            cmds.setAttr( sphere[0]+"Shape.primaryVisibility", 0)
            cmds.setAttr( sphere[0]+"Shape.smoothShading" ,0)
            cmds.setAttr( sphere[0]+"Shape.visibleInReflections" ,0)
            cmds.setAttr( sphere[0]+"Shape.visibleInRefractions", 0)
            cmds.setAttr( sphere[0]+"Shape.doubleSided" ,0)
            
            cmds.xform( sphere , ws = True , t = position)
            #cmds.sets(sphere, e=True, forceElement =  shader + 'SG' )
            
            #*************  Get SkinCluster if it exist  ************************************
            transformObject = vtxObject[0:dot_begin]
            shapeObject = cmds.listRelatives( transformObject , s= True)
            skinCluster = cmds.listConnections  ( shapeObject , t = 'skinCluster' )
            if not skinCluster:
                cmds.skinCluster( transformObject , joint )
            else:
                cmds.skinCluster( skinCluster , e = True , dr = 4 , ps =  0 ,  ns =  10 ,  ai = joint )    
            
            #*************************  Parent to their respective group  ***********************                        

            grp_jnt = twoGrpUP(joint)
            cmds.parent( grp_jnt , structure.GetJoint() )
            cmds.parent( sphere , structure.GetControl() )
            
            StickObjectToMesh( vtxObject , sphere[0] )
    
            cmds.connectAttr( '%s.translate' %sphere[0] ,  '%s.translate' %joint )
            cmds.connectAttr( '%s.rotate' %sphere[0] ,  '%s.rotate' %joint )
            cmds.connectAttr( '%s.scale' %sphere[0] ,  '%s.scale' %joint )
        
#*********************  Setup Window  ************************************************        
 
window = "";
      
if cmds.window( window , exists = True ):
    cmds.deleteUI(window)
    
window = cmds.window( title="Setup stick Ctrls", iconName='Stick Ctrls', widthHeight=(300, 100) , sizeable = False )
cmds.columnLayout( adj = True )
cmds.separator( h = 10 )
cmds.text('Sticky Ctrls by Ronin Garay V1.' )
cmds.separator( h = 10 )
radiusText = cmds.textFieldGrp( l = 'Ctrl Radius:  ' , ed = True )
cmds.button( label='Create Ctrls' , command = 'stickyCtrl()' )
cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
cmds.setParent( '..' )
cmds.showWindow( window )