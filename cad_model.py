"""Needs cadquery master (14/02/2022)
"""

import cadquery as cq

# parameters
rotation_angle = 90

height_gas = 0.1*1e2
height_flibe = 1*1e2
thickness_inner_tank_wall = 0.002*1e2
thickness_sweep_gas = 0.005*1e2

flibe_thickness = 0.5*1e2

inner_radius_lead = 0.1*1e2
lead_thickness = 0.05*1e2
height_lead = 0.6*1e2 + height_gas


# construction
height_tank = height_flibe + 2*(2*thickness_inner_tank_wall + thickness_sweep_gas) + height_gas


lead_inner = (
    cq.Workplane("XY")
    .workplane(offset=height_tank - height_lead/2 + lead_thickness)
    .cylinder(height_lead, inner_radius_lead, angle=rotation_angle)
    )


lead = (
    cq.Workplane("XY")
    .workplane(offset=height_tank - height_lead/2)
    .cylinder(height_lead, inner_radius_lead + lead_thickness, angle=rotation_angle)
    .cut(lead_inner)
    )

gas = (
    cq.Workplane("XY").workplane(offset=height_tank/2 + height_flibe/2)
    .cylinder(height_gas, flibe_thickness, angle=rotation_angle)
    )


height_flibe_cutter = height_lead + 2*thickness_inner_tank_wall + thickness_sweep_gas
thickness_flibe_cutter = inner_radius_lead + lead_thickness + 2*thickness_inner_tank_wall + thickness_sweep_gas
flibe_cutter_1 = (
    cq.Workplane("XY").workplane(offset=height_tank - height_lead/2 - thickness_inner_tank_wall - thickness_sweep_gas/2)
    .cylinder(height_flibe_cutter, thickness_flibe_cutter, angle=rotation_angle)
)

thickness_flibe_cutter2 = 1.2 + 2*thickness_inner_tank_wall + thickness_sweep_gas
flibe_cutter_2 = (
    cq.Workplane("XY").workplane(offset=height_tank/2 - 2*thickness_inner_tank_wall)
    .cylinder(height_flibe + height_gas, thickness_flibe_cutter2, angle=rotation_angle)
)


flibe = (
    cq.Workplane("XY").workplane(offset=height_tank/2)
    .cylinder(height_flibe + height_gas, flibe_thickness, angle=rotation_angle)
    .cut(flibe_cutter_1)
    .cut(flibe_cutter_2)
    )


inner_tank_wall = (
    flibe.shell(thickness_inner_tank_wall, kind="intersection")
)

liner_gas = (
    inner_tank_wall
    .union(flibe)
    .shell(thickness_sweep_gas, kind="intersection")
)

outer_tank_wall = (
    liner_gas
    .union(flibe)
    .union(inner_tank_wall)
    .shell(thickness_inner_tank_wall, kind="intersection")
)


cutter_x_zero = (
    cq.Workplane("XZ")
    .workplane(offset=500/2)    
    .box(500, 500, 500)
)

cutter_y_zero = (
    cq.Workplane("ZY")
    .workplane(offset=500/2)    
    .box(500, 500, 500)
)

flibe = flibe.cut(gas)

inner_tank_wall = inner_tank_wall.cut(cutter_x_zero).cut(cutter_y_zero)
liner_gas = liner_gas.cut(cutter_x_zero).cut(cutter_y_zero)
outer_tank_wall = outer_tank_wall.cut(cutter_x_zero).cut(cutter_y_zero)

cq.exporters.export(inner_tank_wall, 'inner_tank_wall.stl')
cq.exporters.export(outer_tank_wall, 'outer_tank_wall.stl')
cq.exporters.export(lead, 'lead.stl')
cq.exporters.export(flibe, 'flibe.stl')
cq.exporters.export(cutter_y_zero, 'cutter_x_zero.stl')