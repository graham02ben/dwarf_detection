# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 19:19:27 2026

@author: bboyg
"""

import numpy as np
import matplotlib.pyplot as plt

def create_stellar_significance_map(self, mode="stars", significance_threshold=3.0):
    """
    This creates a number map of the data inputted. It bins stellar sources 
    with a pixel size of 0.01 deg. This can be adjusted in '__init__'. 
    Using an equation from Walsh 09, can create a significance map and areas
    that have a sigma > 3 compared to the background is highlighted.

    """
    # Select data based on mode
    if mode == "stars":
        ra, dec = self.ra_star_data, self.dec_star_data
        map_attr = ("xs", "ys", "xbins", "ybins", "significance_maps")
        title = "Star Significance Map"
    
    elif mode == "galaxies":
        ra, dec = self.ra_galaxy_data, self.dec_galaxy_data
        map_attr = ("xg", "yg", "xbing", "ybing", "significance_mapg")
        title = "Galaxy Significance Map"

    elif mode == "both":
        ra, dec = self.ra_data, self.dec_data
        map_attr = ("xsg", "ysg", "xbinsg", "ybinsg", "significance_mapsg")
        title = "Star + Galaxy Significance Map"

    else:
        raise ValueError("mode must be 'stars', 'galaxies', or 'both'")

    # Create histogram bins
    xbins = np.arange(np.min(ra), np.max(ra), self.size)
    ybins = np.arange(np.min(dec), np.max(dec), self.size)

    # 2D histogram
    immap, xedges, yedges = np.histogram2d(ra, dec, bins=(xbins, ybins))

    # Significance map
    sigmap = (immap - np.mean(immap)) / np.std(immap)

    # Significant pixels
    xsel, ysel = np.where(sigmap > significance_threshold)

    # Store results in the appropriate attributes
    setattr(self, map_attr[0], xsel)
    setattr(self, map_attr[1], ysel)
    setattr(self, map_attr[2], xedges)
    setattr(self, map_attr[3], yedges)
    setattr(self, map_attr[4], sigmap)

    # Plot
    plt.imshow(sigmap.T, origin='lower',
               extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
               cmap='plasma', interpolation='gaussian', aspect='auto')
    plt.colorbar()
    plt.scatter(xedges[xsel] + self.size/2,
                yedges[ysel] + self.size/2,
                marker='o', s=3, edgecolors='w')
    plt.title(title)
    plt.xlabel("Right Ascension (deg)")
    plt.ylabel("Declination (deg)")
    plt.show()
        
    return xsel, ysel, sigmap, xbins, ybins
        
def create_significance_map(telescope_image, xbins, ybins, contaimination_cut = 1.0, significance_threshold = 5.0):
    """
    This uses the telescope image and creates a significance map of it. 
    It first takes values above 1 sigma and removes them from the image
    (These are the most bright objects so to avoid contamination, they are removed)
    The mask is applied to the image and another significance map is created,
    and those values above 5 sigma are highlighted. These are saved as Telecoords

    Returns
    -------
    Telecoords, IPB_masked, significant_coords_RA, significant_coords_Dec

    """
    IPB = (telescope_image - np.mean(telescope_image)) / np.std(telescope_image)
    height, width = telescope_image.shape[:2]
        
    x_values = np.arange(width)  # Array of column indices
    y_values = np.arange(height)  # Array of row indices
    xx, yy = np.meshgrid(x_values, y_values)
        
    x_flat, y_flat = xx.flatten(), yy.flatten()
        
    # Remove brightest contamination
    significance_mask = (IPB[x_flat, y_flat] < contaimination_cut)
    significance_mask = significance_mask.reshape((height, width))
    masked_img = telescope_image * significance_mask
    IPB_masked = (masked_img - np.mean(masked_img)) / np.std(masked_img)
        
    # Create a mask based on significance threshold
    sig_mask = IPB_masked[x_flat, y_flat] > significance_threshold
    sig_mask = sig_mask.reshape((height, width))
    significant_coords = np.argwhere(sig_mask)
        
    RA_min, RA_max = xbins[0], xbins[-1]
    Dec_min, Dec_max = ybins[0], ybins[-1]
        
    # Convert pixel indices to sky coordinates
    significant_coords_RA = RA_min + (significant_coords[:, 1] / width) * (RA_max - RA_min)
    significant_coords_Dec = Dec_min + (significant_coords[:, 0] / height) * (Dec_max - Dec_min)
        
    telecoords = np.column_stack((significant_coords_RA, significant_coords_Dec))
    IPB_masked = IPB_masked
    significant_coords_RA = significant_coords_RA
    significant_coords_Dec = significant_coords_Dec

    return telecoords, IPB_masked, significant_coords_RA, significant_coords_Dec