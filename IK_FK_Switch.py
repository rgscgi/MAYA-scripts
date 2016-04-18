#**********************************************************************************
#*********************   IK FK switch matching   **********************************
#**********************************************************************************

import maya.cmds as cmds

akf = cmds.autoKeyframe(q=True, state=True)
if akf:
    cmds.autoKeyframe(state=0)
    
selecList = cmds.ls(sl=True)

for selection in selecList:
    if "IK" in selection or "FK" in selection:
        namespace = selection.split(':')
        namespace = namespace[0]+":" if len(namespace)>1  else ""
        ctrl_IK =""
        ctrl_IK_pole = ""
        ctrls_FK_tip = ""
        ctrls_FK_mid = ""
        ctrls_FK_base = ""
        ctrl_IK_FK_switch = ""
        jnt_base = ""
        jnt_mid = ""
        lc_base = ""
        lc_mid = ""
        if "ctrl_arm_IK_left" == selection or "ctrl_hand_FK_left" == selection:
            ctrl_IK = namespace+"ctrl_arm_IK_left"
            ctrl_IK_pole = namespace+"ctrl_elbow_IK_left"
            ctrls_FK_tip = namespace+"ctrl_hand_FK_left"
            ctrls_FK_mid = namespace+"ctrl_elbow_FK_left"
            ctrls_FK_base = namespace+"ctrl_arm_FK_left"
            ctrl_IK_FK_switch = namespace+"ctrl_arm_IK_FK_left"
            jnt_base = namespace+"jnt_arm_left"
            jnt_mid = namespace+"jnt_elbow_left"
            lc_base = namespace+"lc_arm_left_pivot"
            lc_mid = namespace+"lc_elbow_left_pivot"            
            
        if namespace+"ctrl_arm_IK_right" == selection or namespace+"ctrl_hand_FK_right" == selection:
            ctrl_IK =namespace+"ctrl_arm_IK_right"
            ctrl_IK_pole = namespace+"ctrl_elbow_IK_right"
            ctrls_FK_tip = namespace+"ctrl_hand_FK_right"
            ctrls_FK_mid = namespace+"ctrl_elbow_FK_right"
            ctrls_FK_base = namespace+"ctrl_arm_FK_right"
            ctrl_IK_FK_switch = namespace+"ctrl_arm_IK_FK_right"
            jnt_base = namespace+"jnt_arm_right"
            jnt_mid = namespace+"jnt_elbow_right"
            lc_base = namespace+"lc_arm_right_pivot"
            lc_mid = namespace+"lc_elbow_right_pivot"               
            
        if namespace+"ctrl_foot_IK_left" == selection or namespace+"ctrl_foot_FK_left" == selection:
            ctrl_IK = namespace+"ctrl_foot_IK_left"
            ctrl_IK_pole = namespace+"ctrl_knee_IK_left"
            ctrls_FK_tip = namespace+"ctrl_foot_FK_left"
            ctrls_FK_mid = namespace+"ctrl_knee_FK_left"
            ctrls_FK_base = namespace+"ctrl_leg_FK_left"
            ctrl_IK_FK_switch = namespace+"ctrl_foot_IK_FK_left"
            jnt_base = namespace+"lc_leg_left_pivot"
            jnt_mid = namespace+"lc_knee_left_pivot"
            lc_base = namespace+"lc_foot_left_pivot"
            lc_mid = namespace+"lc_knee_IK_left_pivot"             
            
        if namespace+"ctrl_foot_IK_right" == selection or namespace+"ctrl_foot_FK_right" == selection:
            ctrl_IK =namespace+"ctrl_foot_IK_right"
            ctrl_IK_pole = namespace+"ctrl_knee_IK_right"
            ctrls_FK_tip = namespace+"ctrl_foot_FK_right"
            ctrls_FK_mid = namespace+"ctrl_knee_FK_right"
            ctrls_FK_base = namespace+"ctrl_leg_FK_right"
            ctrl_IK_FK_switch = namespace+"ctrl_foot_IK_FK_right"
            jnt_base = namespace+"lc_leg_right_pivot"
            jnt_mid = namespace+"lc_knee_right_pivot"
            lc_base = namespace+"lc_foot_right_pivot"
            lc_mid = namespace+"lc_knee_IK_right_pivot"              
            
        #*****  Looks to see if you are in FK or IK mode *********
        modeState = cmds.getAttr(ctrl_IK_FK_switch+'.IK_FK')

        #Depending of you mode one match throuth the other

        #*************************************************************************
        #---------------------   IK to FK mode -----------------------------------
        #*************************************************************************

        #Work when mode are in IK mode
        if modeState < 5:
            
            cmds.setKeyframe(ctrl_IK+".rotate")
            cmds.setKeyframe(ctrl_IK+".translate")
            cmds.setKeyframe(ctrl_IK_pole+".translate")
            cmds.setKeyframe(ctrl_IK_FK_switch+".IK_FK")   
                        
            #Look at your current time, goes back one frame    
            time = cmds.currentTime(q=True)
            cmds.currentTime((time-1),edit=True)

            cmds.setKeyframe(ctrls_FK_base+".rotate")
            cmds.setKeyframe(ctrls_FK_mid+".rotate")
            cmds.setKeyframe(ctrls_FK_tip+".rotate")
            cmds.setKeyframe(ctrl_IK_FK_switch+".IK_FK")         
	

            #Goes back to the key frame this procccesses started on.
            cmds.currentTime(time,edit=True)
            
            cmds.setKeyframe(ctrl_IK+".rotate")
            cmds.setKeyframe(ctrl_IK+".translate")
            cmds.setKeyframe(ctrl_IK_pole+".translate")
            cmds.setKeyframe(ctrl_IK_FK_switch+".IK_FK")  	

            #Looks at the rotation position od the skinning joints for the arn in world space and stores them in variables
            baseRot = cmds.xform( jnt_base , q = True, ws = True, ro = True )
            midRot = cmds.xform( jnt_mid  , q = True, ws = True, ro = True )
            twristRot = cmds.xform( ctrl_IK  , q = True, ws = True, ro = True )

            #switches the arm from IK mode to FK mode.
            cmds.setAttr(ctrl_IK_FK_switch+".IK_FK",0)
            
            if "left" in ctrl_IK_FK_switch:
                    #Set the FK controls to the rotate in world space we got from the skinning joints.
                    cmds.xform( ctrls_FK_base  , ws = True, ro = ( baseRot[0], baseRot[1], baseRot[2]) )
                    cmds.xform( ctrls_FK_mid , ws = True, ro = ( midRot[0], midRot[1], midRot[2])  )
                    cmds.xform( ctrls_FK_tip , ws = True, ro = ( twristRot[0], twristRot[1], twristRot[2]) )                           
            else:
                if "arm" in ctrl_IK_FK_switch:
                    cmds.xform( ctrls_FK_base  , ws = True, ro = ( baseRot[0], baseRot[1]+180, baseRot[2]) )
                    cmds.xform( ctrls_FK_mid , ws = True, ro = ( -1*midRot[0], midRot[1]+180, midRot[2])  )
                    cmds.xform( ctrls_FK_tip , ws = True, ro = ( twristRot[0], twristRot[1], twristRot[2]) )
                else:
                    cmds.xform( ctrls_FK_base  , ws = True, ro = ( baseRot[0], baseRot[1], baseRot[2]) )
                    cmds.xform( ctrls_FK_mid , ws = True, ro = ( midRot[0], midRot[1], midRot[2])  )
                    cmds.xform( ctrls_FK_tip , ws = True, ro = ( twristRot[0], twristRot[1], twristRot[2]) )    
          
            #Switch IK to FK moded
            cmds.setAttr( ctrl_IK_FK_switch+".IK_FK", 10 )

            #Sets a key frame on the FK controls to hold them in their new placement
            cmds.setKeyframe(ctrls_FK_base+".rotate")
            cmds.setKeyframe(ctrls_FK_mid+".rotate")
            cmds.setKeyframe(ctrls_FK_tip+".rotate")
            cmds.setKeyframe(ctrl_IK_FK_switch+".IK_FK")  

        #*************************************************************************
        #---------------------   FK to IK mode -----------------------------------
        #*************************************************************************

        #Work when mode are in FK mode
        if modeState >= 5:
            cmds.setKeyframe(ctrls_FK_base+".rotate")
            cmds.setKeyframe(ctrls_FK_mid+".rotate")
            cmds.setKeyframe(ctrls_FK_tip+".rotate")
            cmds.setKeyframe(ctrl_IK_FK_switch+".IK_FK")  
                        
            #Look at your current time, goes back one frame    
            time = cmds.currentTime(q=True)
            cmds.currentTime((time-1),edit=True)

            cmds.setKeyframe(ctrl_IK+".rotate")
            cmds.setKeyframe(ctrl_IK+".translate")
            cmds.setKeyframe(ctrl_IK_pole+".translate")
            cmds.setKeyframe(ctrl_IK_FK_switch+".IK_FK")           


            #Goes back to the key frame this procccesses started on.
            cmds.currentTime(time,edit=True)
            cmds.setKeyframe(ctrls_FK_base+".rotate")
            cmds.setKeyframe(ctrls_FK_mid+".rotate")
            cmds.setKeyframe(ctrls_FK_tip+".rotate")
            cmds.setKeyframe(ctrl_IK_FK_switch+".IK_FK")            

            #Looks at the rotation position of the skinning joints for the arn in world space and stores them in variables
            lc_midTra = cmds.xform( lc_mid , q = True, ws = True, t = True )
            twristTra = cmds.xform( lc_base  , q = True, ws = True, t = True )
            twristRot = cmds.xform( lc_base  , q = True, ws = True, ro = True )
            #switches the arm from IK mode to FK mode.
            cmds.setAttr(ctrl_IK_FK_switch+".IK_FK",10)
            
            print str(lc_base)+" "+str(twristTra)

            if "left" in ctrl_IK_FK_switch:
                #Set the FK controls to the rotate in world space we got from the skinning joints.
                cmds.xform( ctrl_IK_pole  , ws = True, t = ( lc_midTra[0], lc_midTra[1], lc_midTra[2]) )
                cmds.xform( ctrl_IK , ws = True, t = ( twristTra[0], twristTra[1], twristTra[2])  )
                cmds.xform( ctrl_IK , ws = True, ro = ( twristRot[0], twristRot[1], twristRot[2]) )   
            else:
                if "arm" in ctrl_IK_FK_switch:
                    cmds.xform( ctrl_IK_pole  , ws = True, t = ( lc_midTra[0], lc_midTra[1], lc_midTra[2]) )
                    cmds.xform( ctrl_IK , ws = True, t = ( twristTra[0], twristTra[1], twristTra[2])  )
                    cmds.xform( ctrl_IK , ws = True, ro = ( (-1*twristRot[0]), (twristRot[1]+180), twristRot[2]) )
                else:
                    cmds.xform( ctrl_IK_pole  , ws = True, t = ( lc_midTra[0], lc_midTra[1], lc_midTra[2]) )
                    cmds.xform( ctrl_IK , ws = True, t = ( twristTra[0], twristTra[1], twristTra[2])  )
                    cmds.xform( ctrl_IK , ws = True, ro = ( (twristRot[0]), (twristRot[1]), twristRot[2]) )            

            #Switch IK to FK moded
            cmds.setAttr( ctrl_IK_FK_switch+".IK_FK", 0 )

            #Sets a key frame on the FK controls to hold them in their new placement
            cmds.setKeyframe(ctrl_IK+".rotate")
            cmds.setKeyframe(ctrl_IK+".translate")
            cmds.setKeyframe(ctrl_IK_pole+".translate")
            cmds.setKeyframe(ctrl_IK_FK_switch+".IK_FK")   
            
        #*******  activate autoKey if was deactivate before  ******************
        if akf:
            cmds.autoKeyframe(state=1)