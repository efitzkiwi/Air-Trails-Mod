import os
import json
import utils

import copy

pa_path = utils.pa_dir()

mod_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

unit_list_path = "/pa/units/unit_list.json"

unit_list = utils.load_base_json(unit_list_path)

air_trail_path = '/pa/effects/specs/rainbow_trail.pfx'
space_trail_path = '/pa/effects/specs/orbital_trail.pfx'

# above water trail
air_trail = utils.load_mod_json(air_trail_path)
space_trail = utils.load_mod_json(space_trail_path)

base_air = copy.deepcopy(air_trail)
base_space = copy.deepcopy(space_trail)

# base offset entry
fx_offset = {
    'type':'idle',
    'bone': 'bone_root',
    'filename':'',
    'offset':[0, 0, 0],
    'orientation': [0, 0, 0]
}

for unit in unit_list['units']:
    # skip the units which are not air
    if '/pa/units/air/' not in unit: continue
    
    mod_air_unit = os.path.join(mod_path, unit[1:])
    pa_air_unit = os.path.join(pa_path, unit[1:])

    # reset our trail
    air_trail = copy.deepcopy(base_air)

    # check if we have a air_unit in the listed location
    if os.path.exists(pa_air_unit):
        # check if the current unit has base spec of a flying air unit
        # pa/units/air/base_flyer
        # load air_unit json for manipulation
        air_unit = json.load(open(pa_air_unit))
        if '/pa/units/air/base_flyer/' not in air_unit.get('base_spec',''): continue
        if not air_unit.get('mesh_bounds'): continue
        
        print 'Updating: ', os.path.basename(pa_air_unit)

        bounds = air_unit.get('mesh_bounds', [0, 0, 0])
        
        # create mod folder if it does not exist
        if not os.path.exists(os.path.dirname(mod_air_unit)):
           os.makedirs(os.path.dirname(mod_air_unit))

        # change our trail effect filename
        fx_offset['filename'] = air_trail_path
        
        # get offset list from the actual air_unit json
        #    if it doesn't exist already, return empty array to append to
        fx_offsets = air_unit.get('fx_offsets', [])
        # add our custom offset
        fx_offsets.append(fx_offset)

        # override air_unit fx_offsets array
        air_unit['fx_offsets'] = fx_offsets

        # write changes to file
        json.dump(air_unit, open(mod_air_unit, 'w'), indent=4)
