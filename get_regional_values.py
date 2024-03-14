#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 15:17:07 2024

@author: catherinescott
"""

#reads in PET recon and parcellation, groups parcellation labels into whole cerebellum and cerebellar GM
#outputs a csv file of regional values

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from glob import glob
import pandas as pd
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

def extract_regional_values(image, parcellation, labels):
    idx = labels_to_index(parcellation, labels)
    regional_values = np.mean(image[idx, ], axis=0)
    return regional_values


def labels_to_index(parcellation, labels):
    parcellation = np.squeeze(parcellation)
    idx = np.zeros(parcellation.shape, dtype='bool')
    for i in range(len(labels)):
        idx = np.logical_or(idx, parcellation == labels[i])
    return idx


subjects = ['01-014-AMYLOIDPET','01-034-AMYLOID', '01-042','10015124','10024822','AVID2001','AVID2002','AVID2004']
rootpath='/Users/catherinescott/Documents/python_IO_files/PET_analysis/cust_recon_experiments/act_conc/'


#define regions
label_groups={
    'frontal' : [105, 106, 113, 114, 119, 120, 121, 122, 125, 126,
                 137, 138, 141, 142, 143, 144, 147, 148, 151, 152,
                 153, 154, 163, 164, 165, 166, 179, 180, 183, 184,
                 187, 188, 191, 192, 193, 194, 205, 206],
    'parietal' : [107, 108, 149, 150, 175, 176, 177, 178, 199, 200, 195, 196],
    'precuneus' : [169, 170],
    'occipital' : [109, 110, 115, 116, 129, 130, 135, 136, 145,
                   146, 157, 158, 161, 162, 197, 198],
    'temporal' : [117, 118, 123, 124, 133, 134, 155, 156, 171, 172,
                  181, 182, 185, 186, 201, 202, 203, 204, 207, 208],
    'antmidcingulate' : [101, 102, 139, 140],
    'postcingulate' : [167, 168],
    'insula' : [103, 104, 173, 174],
    'composite' : [101,102,105,106,107,108,119,120,121,122,125,126,137,
                   138,139,140,141,142,143,144,147,148,153,154,155,156,
                   163,164,165,166,167,168,169,170,175,176,179,180,181,
                   182,185,186,187,188,191,192,193,194,195,196,199,200,
                   201,202,203,204,205,206],
    'hippocampus' : [48, 49],
    'caudate' : [37, 38],
    'putamen' : [58, 59],
    'thalamus': [60, 61],
    'gm_cereb': [39,40],
    'cereb': [39,40,41,42]
}

label_names = list(label_groups.keys())


itr_options = ['4','8','12','16','20']
filt_options = ['2p0','0p0']
psf_options = ['on','']
pvc_options = ['on','']
t0_options = ['0','40']
t1_options = ['2','50']


all_recons = [['t0','t1','Filt']]
for t_i in range(len(t0_options)):
    for filt_i in range(len(filt_options)):
        
        next_recon = [t0_options[t_i],t1_options[t_i],filt_options[filt_i]]
        all_recons.append(next_recon)



for recon in range(1,len(all_recons)):

    #iterations = int(all_recons[recon][0]) #4
    smoothing =  (all_recons[recon][2]) #4.
    #PSF_model = all_recons[recon][2]
    #PVC_model = all_recons[recon][3] #'on'
    t0s = (all_recons[recon][0])
    t1s = (all_recons[recon][1])
    
    if int(t0s) >=20:
        frame = 'late'
    else:
        frame = 'early'
        
    print('Running: ')
    
    
    
    corrections = ['no_corr','PSF'] #PVC deleted as has different FOV
    
    for corr in corrections:
        print('filter: '+str(smoothing)+' , time: '+str(t0s)+'-'+str(t1s)+' , correction: '+corr )

        #set up save paths
        corrpath = rootpath+corr
        corrpath_csv = corrpath+'/csv'
        corrpath_fig = corrpath+'/figures'
        if not os.path.isdir(corrpath_csv):
            os.makedirs(corrpath_csv)
        if not os.path.isdir(corrpath_fig):
            os.makedirs(corrpath_fig)    
            
        DF_all_itr = pd.DataFrame(columns=[['Subject','Iterations']+label_names])
        DF_all_itr_outpath = corrpath_csv+'/actconc_'+frame+'-f'+smoothing+'mm-itrALL-'+corr+'.csv'
        row_idx = 0
        
        #define image
        fig, axs = plt.subplots(3, 5)
        fig.suptitle('filter: '+str(smoothing)+' , time: '+str(t0s)+'-'+str(t1s)+' , correction: '+corr, fontsize=8)
        axs = axs.flatten()
        
        #check whether csv file alrady exists
        if os.path.isfile(DF_all_itr_outpath):
            #if it exists already then load it in
            DF_all_itr=pd.read_csv(DF_all_itr_outpath)
            #otherwise create the csv file from the images
        else:
            
            for iter_i in range(len(itr_options)):
                
                
                for subject in subjects:
                    
                    print('Subject:'+subject)
                    subj_list = [subject,itr_options[iter_i]]
                    
                    subjpath = rootpath+subject
                    parcellation_path = glob(subjpath+'/sub-'+subject+'_*-labels*'+str(t0s)+'p*to*p*min*.nii.gz')
                    print('parcellation_path: '+parcellation_path[0])
                    
                    # load parcellation
                    parcellation_img = nib.load(parcellation_path[0])                
                    parcellation_img_data = parcellation_img.get_fdata()
                    
                    #load PET image
                    PET_path = glob(subjpath+'/'+corr+'/sub-'+subject+'_ses-baseline_desc-static-'+str(t0s)+'p*to*p*min-f'+smoothing+'mm-pct-niftypet-itr'+itr_options[iter_i]+'*.nii.gz')
                    print('PET_path: '+PET_path[0])
                    if len(PET_path)==0:
                         print('File missing, skip!')
                    else:
                        #get PET image
                        PET_img = nib.load(PET_path[0])                
                        PET_img_data = PET_img.get_fdata()
        
                        for roi_name,labels in label_groups.items():
                            #print('ROI name: '+roi_name)
                            suv_data = extract_regional_values(PET_img_data,parcellation_img_data,labels)
                            subj_list = subj_list+[str(suv_data)]
                            #print('value: '+str((suv_data)))
                        DF_all_itr.loc[row_idx]=subj_list 
                        row_idx = row_idx+1
            DF_all_itr.to_csv(DF_all_itr_outpath)
            
        # create te plots
        subjs = DF_all_itr['Subject'].unique()
        
        for subj in subjs:
            DF_subj=DF_all_itr.loc[DF_all_itr['Subject'] == subj]
            for iter_roi in range(len(label_names)):
                plot_arr = DF_subj.iloc[:,[2,iter_roi+3]].values
                axs[iter_roi].plot(plot_arr[:,0],plot_arr[:,1], linewidth=1.0)
                axs[iter_roi].set_xlabel('Iterations', fontsize=6)
                axs[iter_roi].set_ylabel('Activity conc', fontsize=6)
                axs[iter_roi].set_title(label_names[iter_roi], fontsize=8)
                axs[iter_roi].tick_params(axis='both', which='major', labelsize=6)
                axs[iter_roi].tick_params(axis='both', which='minor', labelsize=6)
                axs[iter_roi].xaxis.set_minor_locator(MultipleLocator(2))
                axs[iter_roi].grid(which='major', linestyle='-')
                axs[iter_roi].grid(which='minor', linestyle='--')
        #plt.xticks(fontsize=6)
        #plt.yticks(fontsize=6)       
        fig.tight_layout() 
        plt.savefig(corrpath_fig+'/actconc_'+frame+'-f'+smoothing+'mm-itrALL-'+corr+'_abs.pdf') 
        plt.show()
        
        #define image
        fig, axs = plt.subplots(3, 5)
        fig.suptitle('filter: '+str(smoothing)+' , time: '+str(t0s)+'-'+str(t1s)+' , correction: '+corr, fontsize=8)
        axs = axs.flatten()
        
        #added percent recovery relative to last iteration (assuming full recovery at last iteration)
        for subj in subjs:
            DF_subj=DF_all_itr.loc[DF_all_itr['Subject'] == subj]
            #print('subject: '+subj)
            for iter_roi in range(len(label_names)):
                #print('region: '+label_names[iter_roi])
                plot_arr = DF_subj.iloc[:,[2,iter_roi+3]].values
                pct_recovery = (100*(plot_arr[:,1]/(plot_arr[len(plot_arr)-1,1])))
                axs[iter_roi].plot(plot_arr[:,0],pct_recovery, linewidth=1.0)
                axs[iter_roi].set_xlabel('Iterations', fontsize=6)
                axs[iter_roi].set_ylabel('% recovery', fontsize=6)
                axs[iter_roi].set_title(label_names[iter_roi], fontsize=8)
                axs[iter_roi].tick_params(axis='both', which='major', labelsize=6)
                axs[iter_roi].tick_params(axis='both', which='minor', labelsize=6)
                axs[iter_roi].xaxis.set_minor_locator(MultipleLocator(2))
                axs[iter_roi].grid(which='major', linestyle='-')
                axs[iter_roi].grid(which='minor', linestyle='--')
                if corr=='no_corr':
                    convergence_criteria = 95.
                    if max(plot_arr[:,1])== (plot_arr[len(plot_arr)-1,1]):
                        # first element just greater than 98
                        res = next(x for x, val in enumerate(pct_recovery)
                                      if val > convergence_criteria)
     
                        # printing result
                        print ('Subject: '+subj+', Region: '+label_names[iter_roi]+', Iteration (> '+str(convergence_criteria)+'%): '+ str(plot_arr[res,0]))
                    else:
                        # first element just greater than 0.6 
                        res = next(x for x, val in enumerate(pct_recovery)
                                      if val < 100+(100-convergence_criteria))
     
                        # printing result
                        print ('Subject: '+subj+', Region: '+label_names[iter_roi]+', Iteration (< '+str(100+(100-convergence_criteria))+'%): '+ str(plot_arr[res,0]))  
                        
        #plt.xticks(fontsize=6)
        #plt.yticks(fontsize=6)       
        fig.tight_layout() 
        plt.savefig(corrpath_fig+'/actconc_'+frame+'-f'+smoothing+'mm-itrALL-'+corr+'_percent.pdf') 
        plt.show()        
        
        
        
        
        
        