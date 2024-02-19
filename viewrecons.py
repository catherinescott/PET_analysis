#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 16:57:49 2023

@author: catherinescott
"""

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from glob import glob


phase = 'early'

if phase=='early':
    desc = '0p0to2p0min'
    disp_min = 0
    disp_max = 2
else:
    desc = '40p0to50p0min'
    disp_min = 0
    disp_max = 4

def show_slices(slices,slice_names):
   """ Function to display row of image slices """

   fig, axes = plt.subplots(1, len(slices)) 
   for i, slice in enumerate(slices):
       axes[i].imshow(slice.T, cmap="hot", origin="lower", vmin=disp_min,vmax=disp_max) #cmap'gray'
       axes[i].title.set_text(slice_names[i])
       


data_path = '/Users/catherinescott/Documents/SUVR_spreadsheets/cust_recon_experiments/01-034-AMYLOID/PSF/'


for z_slice in range(40,80,10):
    slices = []
    slice_names = []
    for itr in range(4,22,2):
        
    
    
        im_name = 'sub-*-'+desc+'-f0p0mm-pct-niftypet-itr'+str(itr)+'_psf.nii.gz'
        
        filename = glob(data_path+ im_name)
        if len(filename)==0:
             print('File missing for: '+im_name+', skip!')
        else:
            img = nib.load(filename[0])
            
            img_data = img.get_fdata()
            
            #z_slice = 64 #about halfway through
            
            slice_0 = img_data[int((img_data.shape[0]/4)):int(((img_data.shape[0]/4)+(img_data.shape[0]/2))), int((img_data.shape[0]/4)):int((img_data.shape[0]/4)+(img_data.shape[0]/2)), z_slice]
            slices.append(slice_0)
            slice_names.append('itr-'+str(itr))
    
            
        
    show_slices(slices,slice_names)    
    plt.suptitle(phase+"- slice "+str(z_slice))
    plt.savefig(data_path+"/"+phase+"-slice "+str(z_slice)+".pdf", format="pdf", bbox_inches="tight")

     
