SD-DNA-PAINT
==========

DNA-PAINT (DNA point accumulation for imaging in nanoscale topography) is a powerful single-molecule localization microscopy technique with an image precision below 5 nm. We recently develloped the multicolor approach spectral demixinge (SD)-DNA-PAINT that is based on spectrally overlapping fluorophores that are excited by a single laser line and a simple dichroic-based emission splitter to image short and long wavelength components of the emission on two sides of the same camera [1]. In order to use the emission from both channels we develloped an very precisse intensity-weighted multichannel registration procedure based on the intrinsic localization pairs. This method significantly increases the resolution from SD-DNA-PAINT and other spectral demixing aproaches (SD-dSTORM [5]).

The included Python script performs the intensity-weighted multichannel registration procedure as decribed in Gimber et al. 2021 [1]:
  - Correction of chromatic errors
  - Multichannel registration
  - Intensity-weighting of localizations from different channels

Briefly, offset values between short/long channel localization pairs are binned into a 2D matrix and the median from all
localization within each bin is used as the local offset value for the correction. Further details are provided in the manuscript.

The program was used for the the following publications:
  - Gimber et al. 2021, biRxiv Simultaneous multicolor DNA-PAINT without sequential fluid exchange using spectral demixing. [1]


Instructions
-------
A detailled workflow is provided in the supplemantary of the publication.

Short workflow:
1) Localization of single molecules by ThunderSTORM (tested) or rapidSTORM (tested). Other file formats may work but need to be converted individually. 
2) Pairing and filtering of the localizations:  It is recommended to used the SD-Mixer2 from Georgi Tadeus for pairing and color-filtering of the localizations: https://github.com/gtadeus/sdmixer2/wiki. SD Mixer2 requires the rapidSTORM file format but localization tables can also be converted from the ThunderSTORM .csv file format via: https://github.com/ngimber/Converter_ThunderSTORM_SDmixer. 
3) Intensity-weighted multichannel registration procedure can be run on the 'filter_out.txt' files from SD Mixer2. 
   - Python version: https://github.com/ngimber/SD-DNA-PAINT/blob/main/intensity-weighted_multichannel_registration.py 
   - Prebuilt version for windows: https://github.com/ngimber/SD-DNA-PAINT/tree/main/intensity-weighted_multichannel_registrationv1.0.2_Win-64bit   
   Users can chose the following parameters:
      - Bin Size: Defines the accuraccy of the correction matrix. Values between 1 and 10 nm work well for medium (10 nm) to dense (1 nm) structures.   
      - "1: Weighted both channels by intensity" was used in the publication, but other methods can be chosen as well:
            1: Weight both channels by intensity.
            2: Use only short wavelength channel localizations.
            3: Use only long wavelength channel localizations.
            4: Use the brightest localization (decide pairwise).
            5: Use the brightest channel.         
4) Rendering can be done after intensity-weighted multichannel registration via SD-Mixer2 or ThunderSTORM.


References
-------
[1] Gimber, N., et al., Simultaneous multicolor DNA-PAINT without sequential fluid exchange using spectral demixing. biRxiv, 2021. https://doi.org/10.1101/2021.11.19.469218

[2] Tadeus, G., et al SDmixer—a versatile software tool for spectral demixing of multicolor single molecule localization data., 2015 Methods Appl. Fluoresc. 3 037001

[3] Ovesny, M., et al., ThunderSTORM: a comprehensive ImageJ plug-in for PALM and STORM data analysis and super-resolution imaging. Bioinformatics, 2014. 30(16): p. 2389-90. 

[4] Wolter et al., rapidSTORM: accurate, fast open-source software for localization microscopy. Nature Methods  9, 1040–1041 (2012). https://doi.org/10.1038/nmeth.2224

[5] Lampe A, et al., Multi-color direct STORM with red emitting carbocyanines (2012), Biology of the Cell 104(4): 229-237.

