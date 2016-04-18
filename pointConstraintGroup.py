import maya.cmds as cmds
import maya.mel as mel


#******* Create a 2 group over object to maintain the same values  **********
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

#********************** create a group to substract traslation and rotation values to keep the same position  ***********************	
def GrpSubsTrans(object):
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
	
objects = cmds.ls(sl=True)


if '.vtx' in objects[0]:
    #***********   Get parent name ******************
    
    ObjectParent = cmds.listRelatives( objects[1] , p = True )    
    #***********   Get object position ******************
    position = cmds.xform(objects[0], q = True, ws = True, t = True)
    #******* Create a group driven by pointOnPolyContraint **********
    groupName = cmds.group(em=True, name=("grp_ptc_"+objects[1]))
    cmds.parent(groupName,ObjectParent[0])
    #******* Get the UV map relationed with the vtx **********
    mapList = cmds.polyListComponentConversion(objects[0],fv=-True , tuv=True)
    #******* Create a pointOnPolyContraint **********
    contraintNames = cmds.pointOnPolyConstraint( objects[0], groupName,mo=False,o=[0,0,0],w=1 )
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
    groupDrv = _2GrpUp(objects[1])
    cmds.parent(groupDrv,groupName)
    GrpSubsTrans(objects[1])