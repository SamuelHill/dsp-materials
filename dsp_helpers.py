#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename:    dsp_helpers.py
# @Author:      Samuel Hill

"""
General description of purpose.

More specific lorem ipsum dolor sit amet, consectetur adipiscing elit.
Quisque a lacus nulla. Vestibulum sodales eros ligula. Nullam euismod
libero magna.
"""

# IMPORTS


def round2(to_round):
    return round(to_round, 2)


def obital(prod1, prod2, prod1_energy, prod2_energy, gather_speed=8):
    power_prod1 = prod1 * (prod1_energy * gather_speed)
    power_prod2 = prod2 * (prod2_energy * gather_speed)
    total_energy = power_prod1 + power_prod2
    diverted_prod1 = (power_prod1 / total_energy) * 30
    diverted_prod2 = (power_prod2 / total_energy) * 30
    remaining_prod1 = (power_prod1 - diverted_prod1) / prod1_energy
    remaining_prod2 = (power_prod2 - diverted_prod2) / prod2_energy
    return remaining_prod1 * 60, remaining_prod2 * 60


def orbital_ice(fire_ice, hydrogen, gather_speed):
    return obital(fire_ice, hydrogen, 4.8, 9, gather_speed)


def orbital_gas(hydrogen, deuterium, gather_speed):
    return obital(hydrogen, deuterium, 9, 9, gather_speed)


def full_planet(planet_rate_minutes):
    return tuple(map(round2, tuple(rate * 40 for rate in planet_rate_minutes)))


if __name__ == '__main__':
    print(full_planet(orbital_ice(.63, .27, 12)))
    print(full_planet(orbital_ice(.78, .31, 12)))
    print(full_planet(orbital_gas(1.05, .04, 12)))
