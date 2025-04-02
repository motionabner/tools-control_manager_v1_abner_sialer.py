import maya.cmds as cmds
from math import sin, cos, pi

color_names = {
    "Red": 13, "Orange": 21, "Yellow": 17, "Green": 14,
    "Blue": 6, "Cyan": 18, "Magenta": 9, "Light Gray": 2, "Black": 1
}

def create_custom_control(name, position, orient_obj=None, color=17, shape="circle", orientation="x", scale=1.0, attributes=None):
    def rotate_shape(obj, axis):
        if axis == "x":
            cmds.rotate(0, 0, "90deg", obj)
        elif axis == "z":
            cmds.rotate("90deg", 0, 0, obj)

    if shape == "circle":
        normal = {"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}[orientation.lower()]
        ctrl = cmds.circle(name=f"{name}_CTRL", normal=normal, radius=scale)[0]
    elif shape == "square":
        pts = [(-1,0,-1),(1,0,-1),(1,0,1),(-1,0,1),(-1,0,-1)]
        ctrl = cmds.curve(name=f"{name}_CTRL", d=1, p=[(x*scale,y,z*scale) for x,y,z in pts])
        rotate_shape(ctrl, orientation)
    elif shape == "arrow":
        pts = [(0,0,2),(1,0,1),(0.5,0,1),(0.5,0,-2),(-0.5,0,-2),(-0.5,0,1),(-1,0,1),(0,0,2)]
        ctrl = cmds.curve(name=f"{name}_CTRL", d=1, p=[(x*scale,y,z*scale) for x,y,z in pts])
        rotate_shape(ctrl, orientation)
    elif shape == "cross":
        pts = [(0.5,0,2),(0.5,0,0.5),(2,0,0.5),(2,0,-0.5),(0.5,0,-0.5),(0.5,0,-2),
               (-0.5,0,-2),(-0.5,0,-0.5),(-2,0,-0.5),(-2,0,0.5),(-0.5,0,0.5),(-0.5,0,2),(0.5,0,2)]
        ctrl = cmds.curve(name=f"{name}_CTRL", d=1, p=[(x*scale,y,z*scale) for x,y,z in pts])
        rotate_shape(ctrl, orientation)
    elif shape == "star":
        pts = []
        for i in range(10):
            angle = i * (pi/5)
            r = 1 if i % 2 == 0 else 0.4
            pts.append((r*cos(angle), 0, r*sin(angle)))
        pts.append(pts[0])
        ctrl = cmds.curve(name=f"{name}_CTRL", d=1, p=[(x*scale,y,z*scale) for x,y,z in pts])
        rotate_shape(ctrl, orientation)
    else:
        ctrl = cmds.circle(name=f"{name}_CTRL", normal=[1, 0, 0], radius=scale)[0]

    shape_node = cmds.listRelatives(ctrl, shapes=True)[0]
    cmds.setAttr(f"{shape_node}.overrideEnabled", 1)
    cmds.setAttr(f"{shape_node}.overrideColor", color)

    offset = cmds.group(ctrl, name=f"{name}_OFFSET")
    grp = cmds.group(offset, name=f"{name}_GRP")
    cmds.xform(grp, ws=True, t=position)

    if orient_obj:
        rot = cmds.xform(orient_obj, q=True, ws=True, ro=True)
        cmds.xform(grp, ws=True, ro=rot)

    cmds.makeIdentity(grp, apply=True, t=1, r=1, s=1, n=0)

    if attributes:
        for attr in attributes:
            if not cmds.objExists(f"{ctrl}.{attr}"):
                cmds.addAttr(ctrl, ln=attr, at='double', k=True)

    return ctrl, offset, grp

def show_control_manager_ui():
    if cmds.window("ControlManagerWin", exists=True):
        cmds.deleteUI("ControlManagerWin")

    window = cmds.window("ControlManagerWin", title="CONTROL MANAGER V1 - ABNER SIALER", widthHeight=(320, 500))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    cmds.text(label="Control base name:")
    name_field = cmds.textField()

    cmds.text(label="Shape:")
    shape_menu = cmds.optionMenu()
    for s in ["circle", "square", "arrow", "cross", "star"]:
        cmds.menuItem(label=s)

    cmds.text(label="Orientation axis:")
    orientation_menu = cmds.optionMenu()
    for axis in ["x", "y", "z"]:
        cmds.menuItem(label=axis)

    cmds.text(label="Color:")
    color_menu = cmds.optionMenu()
    for color_label in color_names:
        cmds.menuItem(label=color_label)

    cmds.text(label="Scale:")
    scale_field = cmds.floatField(value=1.0)

    cmds.text(label="Custom attributes (comma separated):")
    attr_field = cmds.textField()

    cmds.separator(height=10, style='in')

    def create_controls_from_ui(*args):
        base_name = cmds.textField(name_field, q=True, text=True)
        shape = cmds.optionMenu(shape_menu, q=True, value=True)
        orientation = cmds.optionMenu(orientation_menu, q=True, value=True)
        color_label = cmds.optionMenu(color_menu, q=True, value=True)
        color = color_names[color_label]
        scale = cmds.floatField(scale_field, q=True, value=True)
        raw_attrs = cmds.textField(attr_field, q=True, text=True)
        attributes = [a.strip() for a in raw_attrs.split(",")] if raw_attrs else None

        selected = cmds.ls(selection=True)
        if not selected:
            cmds.warning("Select at least one object.")
            return

        for obj in selected:
            if not cmds.objExists(obj):
                continue
            pos = cmds.xform(obj, q=True, ws=True, t=True)
            full_name = f"{base_name}_{obj}"
            create_custom_control(
                name=full_name,
                position=pos,
                orient_obj=obj,
                color=color,
                shape=shape,
                orientation=orientation,
                scale=scale,
                attributes=attributes
            )

    cmds.button(label="CREATE CONTROL(S)", command=create_controls_from_ui, height=40, backgroundColor=(0.3, 0.6, 0.3))
    cmds.setParent('..')
    cmds.showWindow(window)

show_control_manager_ui()
