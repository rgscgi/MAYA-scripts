import maya.cmds as cmds

listObject = cmds.ls(sl=1)
for object in listObject:
    position = cmds.xform(object,q=True,t=True)
    pivot = cmds.xform(object,q=True,piv=True)
    parent = cmds.listRelatives(object,p=True)
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
