SD-DNA-PAINT
==========

DNA-PAINT (DNA point accumulation for imaging in nanoscale topography) is a powrful single-molecule localization microscopy technique with an image precision below 5nm. We recently develloped the multicolor approach spectral demixinge (SD)-DNA-PAINT that is based on spectrally overlapping fluorophores that are excited by a single laser line and a simple dichroic-based emission splitter to image short and long wavelength components of the emission on two sides of the same camera [1].

The included Python script performs the intensity-weighted multichannel registration procedure decribed in Gimber et al. 2021 [1]:
- Correction of chromatic errors
- Multichannel registration
- Intensity-weighting of localizations from different channels

Further details are provided in the manuscript.


The script was used for the the following publications:

Gimber et al. 2021, biRxiv Simultaneous multicolor DNA-PAINT without sequential fluid exchange using spectral demixing. [1]


Instruction
-------
I used the SD-Mixer2 from Georgi Tadeus for pairing and color-filtering of the localizations: https://github.com/gtadeus/sdmixer2/wiki.
SD Mixer2 uses the rapidSTORM file format but localization tables that have the ThunderSTORM .csv file format can be converted via: https://github.com/ngimber/Converter_ThunderSTORM_SDmixer. Rendering can be done after running the intensity-weighted multichannel registration procedure via SD-Mixer2 or ThunderSTORM.



References
-------
[1] Gimber, N., et al., Simultaneous multicolor DNA-PAINT without sequential fluid exchange using spectral demixing. biRxiv, 2021. https://doi.org/10.1101/2021.11.19.469218

add Georgis references 

[3] Ovesny, M., et al., ThunderSTORM: a comprehensive ImageJ plug-in for PALM and STORM data analysis and super-resolution imaging. Bioinformatics, 2014. 30(16): p. 2389-90. 

[4] Wolter et al., rapidSTORM: accurate, fast open-source software for localization microscopy. Nature Methods  9, 1040–1041 (2012). https://doi.org/10.1038/nmeth.2224

