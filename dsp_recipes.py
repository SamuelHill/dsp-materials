#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename:    dsp_recipes.py
# @Author:      Samuel Hill

"""
Dyson Sphere Program recipes, see
    https://dsp-wiki.com/images/d/d9/Recipe_Quick_Reference.jpg
for a quick guide to all recipe rates (non-building)

Attributes:
    recipes (dict): Dictionary of recipe names ('recipe_name') paired with
        tuples of size 1-3, with the form;
                (r0, {'ingredient_1': r1, ...}, br)
        where r0 is the production rate (in items per minute) of the recipe,
        r1 - rn are the consumtion rates associated with each ingredient,
        br is the byproduct rate - which can be omitted when not needed,
        'recipe_name' and associated 'ingredient_1' - '..._n' are replaced with
        the appropriate item names. Item names are simplified titles to ID each
        recipe/ingredient uniquely while not being overly verbose. Rates are in
        items per minute with Assemblers assuming the use of Mk III.
"""

from pprint import pprint

recipes = {
    'magnet':             (40,    {'iron':               40}),
    'iron_ingot':         (60,    {'iron':               60}),
    'steel':              (20,    {'iron_ingot':         60}),
    'copper_ingot':       (60,    {'copper':             60}),
    'titanium_ingot':     (30,    {'titanium':           60}),
    'bricks':             (60,    {'stone':              60}),
    'glass':              (30,    {'stone':              60}),
    'silicon_ingot':      (30,    {'silicon':            60}),
    'silicon_crystal':    (30,    {'silicon_ingot':      60}),
    'graphite':           (30,    {'coal':               60}),
    'crystal':            (30,    {'graphite':           30}),
    'titanium_steel':     (20,    {'titanium_ingot':     20,
                                   'steel':              20,
                                   'sulfur':             40}),
    'refined_oil':        (30,    {'crude':              30}, 15),
    # Not a good deal IMO
    # 'graphite2': (15, {'refined_oil': 15, 'hydrogen': 30}, 45),
    'plastic':            (20,    {'refined_oil':        40,
                                   'graphite':           20}),
    'organic_crystal':    (10,    {'plastic':            20,
                                   'refined_oil':        10,
                                   'graphite':           10}),
    'graphene':           (60,    {'fire_ice':           60}, 30),
    'carbon_nanotube':    (30,    {'graphene':           45,
                                   'titanium_ingot':     15}),
    'strange_matter':     (7.5,   {'particle_container': 15,
                                   'iron_ingot':         15,
                                   'deuterium':          75}),
    # if no frac or deut soruce
    # 'deuterium':          (60,    {'hydrogen':           120}),
    'antimatter':         (60,    {'critical_photon':    60}, 60),
    # No regular ray receivers, only boosted
    # 'critical_photon': (8),
    'critical_photon':    (16,    {'graviton_lens':      0.25}),
    'gears':              (90,    {'iron_ingot':         90}),
    'magnetic_coil':      (180,   {'magnet':             180,
                                   'copper_ingot':       90}),
    'electric_motor':     (45,    {'magnetic_coil':      45,
                                   'gears':              45,
                                   'iron_ingot':         90}),
    'electric_turbine':   (45,    {'electric_motor':     90,
                                   'magnetic_coil':      90}),
    'super_mag_ring':     (30,    {'electric_turbine':   60,
                                   'magnet':             90,
                                   'graphite':           30}),
    'prism':              (90,    {'glass':              135}),
    'plasm_exciter':      (45,    {'prism':              90,
                                   'magnetic_coil':      180}),
    'photon_combiner':    (30,    {'prism':              60,
                                   'circuit':            30}),
    'titanium_crystal':   (22.5,  {'titanium_ingot':     67.5,
                                   'organic_crystal':    22.5}),
    'casamir_crystal':    (22.5,  {'titanium_crystal':   22.5,
                                   'graphene':           45,
                                   'hydrogen':           270}),
    'titanium_glass':     (36,    {'glass':              36,
                                   'titanium_ingot':     36,
                                   'water':              36}),
    'plane_filter':       (7.5,   {'titanium_glass':     15,
                                   'casamir_crystal':    7.5}),
    'hydrogen_fuel':      (30,    {'titanium_ingot':     15,
                                   'hydrogen':           150}),
    'deuteron_fuel':      (15,    {'titanium_steel':     7.5,
                                   'super_mag_ring':     7.5,
                                   'deuterium':          150}),
    'antimatter_fuel':    (7.5,   {'titanium_steel':     3.75,
                                   'annihilation':       3.75,
                                   'hydrogen':           45,
                                   'antimatter':         45}),
    'foundations':        (90,    {'bricks':             270,
                                   'steel':              90}),
    'circuit':            (180,   {'iron_ingot':         180,
                                   'copper_ingot':       90}),
    'microcrystaline':    (45,    {'silicon_ingot':      90,
                                   'copper_ingot':       45}),
    'processor':          (30,    {'circuit':            60,
                                   'microcrystaline':    60}),
    'quantum_chip':       (15,    {'processor':          30,
                                   'plane_filter':       30}),
    'particle_container': (22.5,  {'electric_turbine':   45,
                                   'graphene':           45,
                                   'copper_ingot':       45}),
    'annihilation':       (4.5,   {'particle_container': 4.5,
                                   'processor':          4.5}),
    # 12 not 15?
    'graviton_lens':      (15,    {'crystal':            60,
                                   'strange_matter':     15}),
    'space_warper':       (9,     {'graviton_lens':      9}),
    # Unsure...
    # 'space_warper':       (72,     {'green_matrix':      9}),
    'particle_broadband': (11.25, {'carbon_nanotube':    22.5,
                                   'silicon_crystal':    22.5,
                                   'plastic':            11.25}),
    'thruster':           (22.5,  {'copper_ingot':       67.5,
                                   'steel':              45}),
    'reinforced_thrust':  (15,    {'titanium_steel':     75,
                                   'electric_turbine':   75}),
    'logistics_drone':    (22.5,  {'iron_ingot':         112.5,
                                   'processor':          45,
                                   'thruster':           45}),
    'logistics_vessel':   (15,    {'titanium_steel':     150,
                                   'processor':          150,
                                   'reinforced_thrust':  30}),
    'solar_sail':         (45,    {'graphene':           22.5,
                                   'photon_combiner':    22.5}),
    'frame_material':     (15,    {'carbon_nanotube':    60,
                                   'titanium_steel':     15,
                                   'silicon_ingot':      15}),
    'sphere_component':   (11.25, {'frame_material':     33.75,
                                   'solar_sail':         33.75,
                                   'processor':          33.75}),
    'carrier_rocket':     (15,    {'sphere_component':   30,
                                   'deuteron_fuel':      60,
                                   'quantum_chip':       30}),
    'blue_matrix':        (20,    {'magnetic_coil':      20,
                                   'circuit':            20}),
    'red_matrix':         (10,    {'graphite':           20,
                                   'hydrogen':           20}),
    'yellow_matrix':      (7.5,   {'crystal':            7.5,
                                   'titanium_crystal':   7.5}),
    'purple_matrix':      (6,     {'processor':          12,
                                   'particle_broadband': 6}),
    'green_matrix':       (5,     {'graviton_lens':      2.5,
                                   'quantum_chip':       2.5}),
    'universe_matrix':    (4,     {'blue_matrix':        4,
                                   'red_matrix':         4,
                                   'yellow_matrix':      4,
                                   'purple_matrix':      4,
                                   'green_matrix':       4,
                                   'antimatter':         4})
    }


def use_rares(rare_list=None):
    """Replaces recipes with an equivalent recipe using rare items instead.

    Args:
        rare_list (list, optional): List of the rare items to be used for
            replacement. Default to all.
    """
    if not rare_list:
        rare_list = ['kimberlite', 'spiniform', 'optical',
                     'fractal', 'unipolar']
    if 'kimberlite' in rare_list:
        recipes['crystal'] = (80, {'kimberlite': 40})
    if 'spiniform' in rare_list:
        recipes['carbon_nanotube'] = (30, {'spiniform': 30})
    if 'optical' in rare_list:
        recipes['photon_combiner'] = (30, {'optical': 30,
                                           'circuit': 30})
        recipes['casamir_crystal'] = (22.5, {'optical': 90,
                                             'graphene': 45,
                                             'hydrogen': 270})
    if 'fractal' in rare_list:
        recipes['silicon_crystal'] = (120, {'fractal': 60})
    if 'unipolar' in rare_list:
        recipes['particle_container'] = (22.5, {'unipolar': 225,
                                                'copper_ingot': 45})


if __name__ == '__main__':
    pprint(recipes)
    print('OR, with rares...')
    use_rares()
    pprint(recipes)
