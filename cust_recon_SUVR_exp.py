#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 10:55:40 2024

@author: catherinescott
"""

# this code loops through the SUVr csv files created for different recons and plots the SUVR by iteration


import pandas as pd
from glob import glob
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

rois = ['frontal',
        'parietal',
        'occipital',
        'temporal',
        'insula',
        'precuneus',
        'antmidcingulate',
        'postcingulate',
        'hippocampus',
        'caudate',
        'putamen',
        'thalamus',
        'composite']


root_folder = '/Users/catherinescott/Documents/python_IO_files/PET_analysis/cust_recon_experiments/'

itr_options = ['4','8','12','16','20']
filt_options = ['2p0','0p0']
psf_options = ['on','']
pvc_options = ['on','']
t0_options = ['0','40']
t1_options = ['2','50']

# #all_recons = [['itr','Filt','psf','t0','t1']]
# all_recons = [['Filt','psf','pvc','t0','t1']]
# #for iter_i in range(len(itr_options)):
# for filt_i in range(len(filt_options)):
#     for psf_i in range(len(psf_options)):
#         for pvc_i in range(len(pvc_options)):
#             for t_i in range(len(t0_options)):
#                 next_recon = [filt_options[filt_i],psf_options[psf_i],pvc_options[pvc_i],t0_options[t_i],t1_options[t_i]]
#                 all_recons.append(next_recon)


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
    
    
    
    corrections = ['no_corr','PVC','PSF']
    
    for corr in corrections:
        print('filter: '+str(smoothing)+' , time: '+str(t0s)+'-'+str(t1s)+' , correction: '+corr )
        #define image
        fig, axs = plt.subplots(3, 5)

        fig.suptitle('filter: '+str(smoothing)+' , time: '+str(t0s)+'-'+str(t1s)+' , correction: '+corr, fontsize=8)
        axs = axs.flatten()
        DF_all_itr = pd. DataFrame() 
        
        for iter_i in range(len(itr_options)):
            
            itr = itr_options[iter_i]
            # no PSF, no PVC
            DF =  pd. DataFrame() 
            #amagamate the different studies into 1 data frame with all subjects
            filepath_template= root_folder+'/*/'+corr+'/ses-baseline_'+t0s+'*min-f'+smoothing+'mm-pct-niftypet-itr'+itr+'*_suvr_*.csv'
            
            files_to_amal = glob(filepath_template)
            #print(files_to_amal)
            DF = pd.concat((pd.read_csv(f) for f in files_to_amal), ignore_index=True)
            
            out_fig_dir = root_folder+'/figures/'+corr
            out_csv_dir = root_folder+'/csv/'+corr
            if not os.path.isdir(out_fig_dir):
                os.makedirs(out_fig_dir)
            if not os.path.isdir(out_csv_dir):
                os.makedirs(out_csv_dir)
                
            DF.to_csv(out_csv_dir+'/SUVR_'+frame+'-f'+smoothing+'mm-itr'+itr+'-'+corr+'.csv')
            DF.insert(1,"Iterations",[int(itr)]*len(DF.index), True)
            DF.drop(['session','exclude'], axis=1, inplace=True)
            
            if len(DF_all_itr.index)==0:
                DF_all_itr =DF
            else:
                DF_all_itr= pd.concat([DF_all_itr,DF])
                #pd.DataFrame().append([DF_all_itr,DF])
        DF_all_itr.to_csv(out_csv_dir+'/SUVR_'+frame+'-f'+smoothing+'mm-itrALL-'+corr+'.csv')
        subjs = DF_all_itr['subject'].unique()
        
        for subj in subjs:
            DF_subj=DF_all_itr.loc[DF_all_itr['subject'] == subj]
            for iter_roi in range(len(rois)):
                plot_arr = DF_subj.iloc[:,[1,iter_roi+2]].values
                axs[iter_roi].plot(plot_arr[:,0],plot_arr[:,1])
                axs[iter_roi].set_xlabel('Iterations', fontsize=6)
                axs[iter_roi].set_ylabel('SUVR', fontsize=6)
                axs[iter_roi].set_title(rois[iter_roi], fontsize=8)
                axs[iter_roi].tick_params(axis='both', which='major', labelsize=6)
                axs[iter_roi].tick_params(axis='both', which='minor', labelsize=6)
                axs[iter_roi].xaxis.set_minor_locator(MultipleLocator(2))
                axs[iter_roi].grid(which='major', linestyle='-')
                axs[iter_roi].grid(which='minor', linestyle='--')
        #plt.xticks(fontsize=6)
        #plt.yticks(fontsize=6)       
        fig.tight_layout() 
        plt.savefig(out_fig_dir+'/SUVR_'+frame+'-f'+smoothing+'mm-itrALL-'+corr+'.pdf') 
        plt.show()
                   
                    
            
            
            
    
            
    # # no PSF, PVC 
    # DF_PVC =  pd. DataFrame() 
    # # PSF, no PVC  
    # DF_PSF = pd. DataFrame() 


    #         # no PSF, no PVC
    #         next_recon = [t0_options[t_i],t1_options[t_i],filt_options[filt_i],'','']
    #         all_recons.append(next_recon)
    #         # no PSF, PVC           
    #         next_recon = [t0_options[t_i],t1_options[t_i],filt_options[filt_i],'','on']
    #         all_recons.append(next_recon)                
    #         # PSF, no PVC           
    #         next_recon = [t0_options[t_i],t1_options[t_i],filt_options[filt_i],'on','off']
     #       all_recons.append(next_recon) 