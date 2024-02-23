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


def show_slices(slices,slice_names,im_max_disp):
   """ Function to display row of image slices """

   fig, axes = plt.subplots(1, len(slices)) 
   for i, slice in enumerate(slices):
       axes[i].imshow(slice.T, cmap="hot", origin="lower", vmin=disp_min,vmax=im_max_disp) #cmap'gray'
       axes[i].title.set_text(slice_names[i])
       
rootdatapath='/Users/catherinescott/Documents/python_IO_files/PET_analysis/cust_recon_experiments/act_conc'
phases = ['early','late']
corrections = ['no_corr','PSF']
subjects=['01-014-AMYLOIDPET','01-034-AMYLOID', '01-042','10015124','10024822','AVID2001','AVID2002','AVID2004']
filt_options = ['2p0','0p0']

for phase in phases:
    for corr in corrections:
        for filt in filt_options:
            for subj in subjects:
        
                if phase=='early':
                    desc = '0p0to2p0min'
                    disp_min = 0
                    #disp_max = 20000
                else:
                    desc = '40p0to*min'
                    disp_min = 0
                    #disp_max = 15000
                    
                    
                    
                data_path = rootdatapath+'/'+subj+'/'+corr
                
                
                for z_slice in range(50,55,10):#(40,80,10):
                    slices = []
                    slice_names = []
                    im_slice_count  =0
                    for itr in range(4,22,4):
                    
                        im_name = 'sub-'+subj+'*'+desc+'-f'+filt+'mm-pct-niftypet-itr'+str(itr)+'*.nii.gz'
                        
                        filename = glob(data_path+ '/'+im_name)
                        if len(filename)==0:
                             print('File missing for: '+im_name+', skip!')
                        else:
                            img = nib.load(filename[0])
                            
                            img_data = img.get_fdata()
                            if im_slice_count==0:
                                im_max_disp=0.2*np.max(img_data)
                            #z_slice = 64 #about halfway through
                            
                            slice_0 = img_data[int((img_data.shape[0]/4)):int(((img_data.shape[0]/4)+(img_data.shape[0]/2))), int((img_data.shape[0]/4)):int((img_data.shape[0]/4)+(img_data.shape[0]/2)), z_slice]
                            slices.append(slice_0)
                            slice_names.append('itr-'+str(itr))
                    
                            
                    #im_max_disp=0.3*np.max(img_data)    
                    show_slices(slices,slice_names,im_max_disp)    
                    plt.suptitle(phase+"- slice "+str(z_slice))
                    figpath=rootdatapath+'/'+corr+'/figures/'+subj
                    if not os.path.isdir(figpath):
                        os.makedirs(figpath)
                        
                    #need a better name!
                    plt.savefig(figpath+"/"+phase+"_f"+filt+"-slice "+str(z_slice)+".pdf", format="pdf", bbox_inches="tight", dpi=1000)
                    plt.close()
                     
