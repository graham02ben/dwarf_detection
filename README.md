# dwarf_detection
For an input RA and dec, this code retrieves the data, and locates significant overdensities in stellar, galactic, and in both maps. In addition, it uses images to add another source of confidence.

The code will produce CMDs for all overdensities which match a certain CM criterion
By inputting the coordinates of the chosen overdensity, one can run an MCMC to retrieve data from the overdensity.

Code outputs: CMD compared to a field, radial profile, MCMC corner plot, local area location and zoomed-in density map.

For simplicity, code should be saved within one folder, with the corners_PAndAS11.txt saved too. The Isochrone folder should be saved within the main folder, and two empty folders should be created. One named 'DATA', one named 'Candidates'.

Minimal changes to the code are required, primarily the path to which the data is saved, extracted, and moved:
Functions:
  Line 22: This has to be your Downloads folder
  Line 26: Change the path of your 'DATA' folder, but KEEP "...\\ra{ra_value}\\dec{dec_value}\\" afterwards
  Line 120: Adjust so it's your download folders, however, KEEP "...\\ra{ra_value}\\"
  Line 121: This should be JUST your DATA folder
  Line 122: Same as above but keep "...\\ra{ra_value}\\"
  Line 124: Change to download folder but keep "\\ra{ra_value}\\dec{dec_value}\\"

Dwarf_Detection:
  Line 1518: Adjust the path of it to your 'Candidates' folder
