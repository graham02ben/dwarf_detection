# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:03:32 2026

@author: bboyg
"""

import numpy as np
import matplotlib.pyplot as plt

from astropy.coordinates import get_icrs_coordinates

def process_data(ra_data, dec_data, size, candidate_coords, three_arcmin = 0.05):
    Map, xBin, yBin = np.histogram2d(ra_data, dec_data,
                                     bins=(np.arange(np.min(ra_data), np.max(ra_data), size),
                                           np.arange(np.min(dec_data), np.max(dec_data), size)),
                                     )
    # Create a significance map
    significance_map = (Map - np.mean(Map)) / np.std(Map)
        
    #setting zoomed in boundaries
    x_min_zoom = candidate_coords.ra.deg - three_arcmin
    x_max_zoom = candidate_coords.ra.deg + three_arcmin
    y_min_zoom = candidate_coords.dec.deg - three_arcmin
    y_max_zoom = candidate_coords.dec.deg + three_arcmin
    
    return xBin, yBin, significance_map, x_min_zoom, x_max_zoom, y_min_zoom, y_max_zoom

def Pandas(ra_data, dec_data, size, candidate_coords, x0m33, y0m33):
    """
    Plots the location of the candidate on a map with respect to M33 and surround dwarf galaxies.
    The PAndAS survey is highlighted as well. 
    In addition, a zoomed in density plot is made to see the overdensity clearly
    on a significance map

    Returns
    -------
    Zoomed in density map and location of candidate with repsect to M33

    """
    xBin, yBin, significance_map, x_min_zoom, x_max_zoom, y_min_zoom, y_max_zoom = process_data(ra_data, dec_data, size, candidate_coords)
    
    # Plotting zoomed in desnity map
    fig, ax_map = plt.subplots(1, 2, figsize = (11,4))
    ax = ax_map[0].imshow(significance_map.T, origin='lower',
                                 extent=[xBin[0], xBin[-1], yBin[0], yBin[-1]],
                                 cmap='plasma', interpolation='gaussian',
                                 aspect='auto')
    fig.colorbar(ax, ax = ax_map[0])
    ax_map[0].set_title('Zoomed: Star and Galaxy')
    ax_map[0].set_xlabel('Right Ascension (deg)')
    ax_map[0].set_ylabel('Declination (deg)')

    ax_map[0].set_xlim(x_min_zoom, x_max_zoom)
    ax_map[0].set_ylim(y_min_zoom, y_max_zoom)

    #===================================================================
    # PAndAS FOOTPRINT
    #===================================================================
    c_m33 = get_icrs_coordinates("M33")
    c_p1  = get_icrs_coordinates("Pisces I")
    c_a22 = get_icrs_coordinates("Andromeda XXII")
    c_a16 = get_icrs_coordinates("Andromeda XVI")
    c_a11 = get_icrs_coordinates("Andromeda XI")
    c_a12 = get_icrs_coordinates("Andromeda XII")
    c_a13 = get_icrs_coordinates("Andromeda XIII")
    c_a14 = get_icrs_coordinates("Andromeda XIV")
    c_a2  = get_icrs_coordinates("Andromeda II")
        
    # Read the field positions from NM file
    r = np.genfromtxt('corners_PAndAS11.txt', dtype=None, names='RA,Dec', usecols=(0,1))
   
    circle1 = plt.Circle((c_m33.ra.deg, c_m33.dec.deg), 10, facecolor='None', edgecolor='0.5', ls='--')
    lin = plt.plot(r['RA'],r['Dec'],color='k',label='PAndAS')

    ax_map[1].set_xlim(30,5)
    ax_map[1].set_ylim(21,34)
    ax_map[1].set_xlabel('RA (deg)')
    ax_map[1].set_ylabel('Dec (deg)')
    
    # Pisc VII
    ra1, dec1 = 20.419, 26.391 # P7
    #Overdensity
    ra2, dec2 = x0m33[0], y0m33[0]        
    ax_map[1].add_patch(circle1)
    #Add points and labels for the dwarf
    ax_map[1].scatter([ra1],[dec1], marker = '*', s = 300, c = 'mediumpurple', edgecolor='k')
    ax_map[1].scatter([ra2],[dec2], marker = '*', s = 300, c = 'mediumpurple', edgecolor='k')
    ax_map[1].scatter(c_m33.ra.deg, c_m33.dec.deg, marker = 'o', s = 100, c = 'k')
    ax_map[1].scatter(c_a22.ra.deg, c_a22.dec.deg, marker = '*', s = 300, c = 'mediumpurple',edgecolor='k',zorder=100)
    ax_map[1].scatter(c_a16.ra.deg, c_a16.dec.deg, marker = 'o', s = 50, c = 'thistle',edgecolor='k')
    ax_map[1].scatter(c_a11.ra.deg, c_a11.dec.deg, marker = 'o', s = 50, c = 'thistle',edgecolor='k')
    ax_map[1].scatter(c_a12.ra.deg, c_a12.dec.deg, marker = 'o', s = 50, c = 'thistle',edgecolor='k')
    ax_map[1].scatter(c_a13.ra.deg, c_a13.dec.deg, marker = 'o', s = 50, c = 'thistle',edgecolor='k')
    ax_map[1].scatter(c_a14.ra.deg, c_a14.dec.deg, marker = 'o', s = 50, c = 'thistle',edgecolor='k')
    ax_map[1].scatter(c_a2.ra.deg, c_a2.dec.deg, marker = '*', s = 200, c = 'mediumpurple',edgecolor='k')
    ax_map[1].scatter(c_p1.ra.deg, c_p1.dec.deg, marker = '*', s = 200, c = 'mediumpurple',edgecolor='k')
    ax_map[1].set_title('Location of Candidate around M33')
    ax_map[1].text(ra2 - 0.5, dec2 + 0.25 , "Cand", fontsize =12)
    ax_map[1].text(25, 31, "M33" ,fontsize = 12)
    ax_map[1].text(21, 28, "And XXII/Tri I", fontsize = 12)
    ax_map[1].text(19.5, 26.2, "Pisces VII/Tri III", fontsize = 12)
    ax_map[1].text(15, 22.2, "Pisces I", fontsize = 12)
    ax_map[1].text(25, 32, "PAndAS footprint", c = '0.5')
    
    return fig
    
    
def zoom(ra_data, dec_data, size, candidate_coords):
    """
    Zoomed in significance map of the star and galaxy sources of the overdensity. 
    Zoomed in with radius of three arcminutes,

    Returns
    -------
    Zoom significance map.

    """
    xBin, yBin, significance_map, x_min_zoom, x_max_zoom, y_min_zoom, y_max_zoom = process_data(ra_data, dec_data, size, candidate_coords)
    
    fig, ax_zoom = plt.subplots(1, 1)
    ax = ax_zoom.imshow(significance_map.T, origin='lower',
                                 extent=[xBin[0], xBin[-1], yBin[0], yBin[-1]],
                                 cmap='plasma', interpolation='gaussian',
                                 aspect='auto')
    fig.colorbar(ax, ax = ax_zoom)
    #self.ax_zoom.set_title('Zoomed: Star and Galaxy')
    ax_zoom.set_xlabel('RA (deg)', fontsize = 12)
    ax_zoom.set_ylabel('dec (deg)', fontsize = 12)
    ax_zoom.invert_xaxis()

    ax_zoom.set_xlim(x_min_zoom, x_max_zoom)
    ax_zoom.set_ylim(y_min_zoom, y_max_zoom)
    
    return fig