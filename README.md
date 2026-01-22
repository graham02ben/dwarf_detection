# dwarf_detection
For an input RA and dec, this code retrieves the data and locates significant overdensities in stellar, galactic, and both maps. In addition, it uses images to add another source of confidence.

The code will produce CMDs for all overdensities which match a certain CM criterion
By inputting the coordinates of the chosen overdensity, one can run an MCMC to retrieve data from the overdensity.

Code outputs: CMD compared to a field, radial profile, MCMC corner plot, local area location and zoomed-in density map.

For simplicity, the code should be saved within one folder, with the corners_PAndAS11.txt saved too. The Isochrone folder should be saved within the main folder, and two empty folders should be created. One named 'DATA', one named 'Candidates'.
