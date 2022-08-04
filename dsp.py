#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename:    dsp.py
# @Author:      Samuel Hill

"""
Dyson Sphere Program production optimizer

Attributes:
    assembler (dict): counters for assemblers
    byproducts (dict): counters for byproducts
    chemical_plant (dict): counters for chemical plants
    materials (dict): counters for raw materials
    matrix_lab (dict): counters for matrix labs
    particle_collider (dict): counters for particle colliders
    ray_receiver (dict): counters for ray receivers
    refinery (dict): counters for refineries
    smelter (dict): counters for smelters
"""

from argparse import ArgumentParser
from math import ceil as ceiling
from sys import argv
from dsp_recipes import recipes, use_rares


# Deuterium can be a base material, but I haven't tapped a Gas giant yet
materials = {
    'iron':    0, 'copper':   0, 'stone':     0, 'coal':       0,
    'silicon': 0, 'titanium': 0, 'water':     0, 'sulfur':     0,
    'crude':   0, 'hydrogen': 0, 'fire_ice':  0, 'kimberlite': 0,
    'fractal': 0, 'optical':  0, 'spiniform': 0, 'unipolar':   0}
byproducts = {'hydrogen': 0}  # it's always hydrogen...
smelter = {
    'magnet':          0, 'iron_ingot': 0, 'steel':   0, 'copper_ingot':   0,
    'titanium_ingot':  0, 'bricks':     0, 'glass':   0, 'silicon_ingot':  0,
    'silicon_crystal': 0, 'graphite':   0, 'crystal': 0, 'titanium_steel': 0}
assembler = {
    'magnetic_coil':      0, 'electric_motor':  0, 'gears':          0,
    'electric_turbine':   0, 'super_mag_ring':  0, 'prism':          0,
    'photon_combiner':    0, 'plasm_exciter':   0, 'circuit':        0,
    'titanium_crystal':   0, 'graviton_lens':   0, 'processor':      0,
    'casamir_crystal':    0, 'titanium_glass':  0, 'plane_filter':   0,
    'particle_container': 0, 'deuteron_fuel':   0, 'quantum_chip':   0,
    'particle_broadband': 0, 'microcrystaline': 0, 'foundations':    0,
    'hydrogen_fuel':      0, 'antimatter_fuel': 0, 'annihilation':   0,
    'reinforced_thrust':  0, 'thruster':        0, 'space_warper':   0,
    'logistics_vessel':   0, 'logistics_drone': 0, 'solar_sail':     0,
    'sphere_component':   0, 'frame_material':  0, 'carrier_rocket': 0}
refinery = {'refined_oil': 0}
chemical_plant = {'plastic':  0, 'organic_crystal': 0,
                  'graphene': 0, 'carbon_nanotube': 0}
particle_collider = {'strange_matter': 0, 'deuterium': 0, 'antimatter': 0}
ray_receiver = {'critical_photon': 0}
matrix_lab = {'blue_matrix':   0, 'red_matrix':   0, 'yellow_matrix':   0,
              'purple_matrix': 0, 'green_matrix': 0, 'universe_matrix': 0}


def backtrack(product, goal, ignore_byproduct):
    """Simple recursive method to flesh out the number of products needed
    for each ingredient to match the goal production rate.

    Args:
        product (str): name of recipe to produce
        goal (int): rate per minute desired for production
        ignore_byproduct (bool): whether to ignore the creation of byproducts
    """
    if product in recipes.keys():
        multiplier = goal / recipes[product][0]
        update_products(product, multiplier * recipes[product][0])
        if len(recipes[product]) == 3 and not ignore_byproduct:
            byproducts['hydrogen'] += multiplier * recipes[product][2]
        elif len(recipes[product]) == 1:
            return
        for ingredient in recipes[product][1].items():
            if ingredient[0] in materials:
                update_products(ingredient[0], multiplier * ingredient[1])
            else:
                backtrack(ingredient[0], multiplier * ingredient[1],
                          ignore_byproduct)


def parse_args():
    """ArgumentParser helper to make command line input easier, allows
    for selection of products, goal rate, whether you want to ignore
    byproducts, and the use of rares (with the ability to select subsets)

    Returns:
        tuple: arguments to backtrack
    """
    parser = ArgumentParser(description='Run backtrack with goal.')
    parser.add_argument('-p', '--product', type=str)
    parser.add_argument('-g', '--goal', type=int)
    parser.add_argument('-i', '--ignore_byproduct', action='store_true')
    parser.add_argument('-r', '--use_rares', type=str)
    _, *args = argv
    args = parser.parse_args(args)
    if args.use_rares:
        if args.use_rares == 'all':
            use_rares()
        else:
            use_rares(args.use_rares.split(','))
    ignore = False
    if args.ignore_byproduct:
        ignore = True
    return (args.product, args.goal, ignore)


def update_products(product, num_needed):
    """Backtracking helper, updates a given product to its respective factory
    dict. Not needed if this is refactored to have all recipes in one large
    counter dict, but the separation of factory dicts makes pretty printing
    easier.

    Args:
        product (str): recipe/ingredient
        num_needed (int): production rate needed
    """
    if product in smelter:
        smelter[product] += num_needed
    elif product in refinery:
        refinery[product] += num_needed
    elif product in chemical_plant:
        chemical_plant[product] += num_needed
    elif product in particle_collider:
        particle_collider[product] += num_needed
    elif product in ray_receiver:
        ray_receiver[product] += num_needed
    elif product in assembler:
        assembler[product] += num_needed
    elif product in matrix_lab:
        matrix_lab[product] += num_needed
    else:
        materials[product] += num_needed


def simplify(factory, factory_name):
    """Pretty print helper to process the contents of each factory dict

    Args:
        factory (dict): one of the factory dictionaries such as smelter
        factory_name (str): Pretty name of factory (for printing)

    Returns:
        str: Pretty print ready string with no 0 outputs and an approximate
            total number of factories of a given type needed
    """
    outstring = ''
    total_factories = 0
    for recipe in factory:
        if factory[recipe] > 0:
            num_factories = factory[recipe]/recipes[recipe][0]
            outstring += f'\t{recipe}: {num_factories}\n'
            total_factories += ceiling(num_factories)
    if outstring != '':
        outstring = f'{factory_name}:\n{outstring}'
        outstring += f'\tTotal factories ~: {total_factories}\n\n'
    return outstring


def pretty_print():
    """Pretty print the counters of materials and recipes, and simplify
    the recipes down to the number of factories needed.
    """
    materials_string = ''
    for material in materials:
        if materials[material] > 0:
            materials_string += f'\t{material}: {materials[material]}\n'
    if materials_string != '':
        materials_string = f'Raw Materials:\n{materials_string}\n'
    byproduct_string = ''
    if byproducts['hydrogen'] > 0:
        hydrogen = byproducts['hydrogen']
        byproduct_string = f'Byproducts:\n\thydrogen: {hydrogen}\n\n'
    print(f'{materials_string}{byproduct_string}'
          f'{simplify(smelter, "Smelter")}'
          f'{simplify(refinery, "Refinery")}'
          f'{simplify(chemical_plant, "Chemical Plant")}'
          f'{simplify(particle_collider, "Particle Collider")}'
          f'{simplify(ray_receiver, "Ray Receiver")}'
          f'{simplify(assembler, "Assembler")}'
          f'{simplify(matrix_lab, "Matrix Lab")}')


if __name__ == '__main__':
    backtrack(*parse_args())
    pretty_print()
