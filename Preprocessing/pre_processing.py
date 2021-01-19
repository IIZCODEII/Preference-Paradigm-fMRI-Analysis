import gzip, shutil
import time
import yaml
import glob
from nipype.interfaces.matlab import MatlabCommand
from nipype.interfaces.spm import SliceTiming, Realign, Coregister, Normalize12
from nipype.interfaces.fsl import TOPUP


tasks = ['Houses','Food','Faces','Paintings']

runs = ['ap','pa']


paths_func = 'ses-19/func/sub-01_ses-19_task-Preference{}_dir-{}_bold.nii.gz'

paths_anat = 'ses-19/anat/sub-01_ses-00_anat_sub-01_ses-00_T1w.nii'




t1 = time.time()
print('* '*3 + 'fMRI Preprocessing Computation' + ' *'*3 + '\n' )

for task in tasks:
    
    print('\t Processing Subject 1 Task {}'.format(task))
    
    for run in runs:

    	func_data_raw = 'ses-19/func/sub-01_ses-19_task-Preference{}_dir-{}_bold.nii.gz'.format(task,run)

    	func_data_cor = func_data_raw[:-4] + '_corrected' + func_data_raw[-4:]
    	a_func = func_data_cor[:12] +'a'+ func_data_cor[12:]
        r_func = a_func[:12] +'r'+ a_func[12:]
    	w_func = w_func[:12] +'w'+ w_func[12:]

    	print('\t \t RUN {}'.format(run))
  
		
		# Distorsion Correction
		print('\t \t \t % Distorsion Correction - FSL TOPUP') 
    	topup = TOPUP()
    	topup.inputs.in_file = func_data_raw
	 	topup.inputs.encoding_file = "topup_encoding_ap.txt" if  run == 'ap' else "topup_encoding_pa.txt"
	 	topup.inputs.output_type = "NIFTI_GZ"
	 	topup.cmdline
	 	res = topup.run()

        print('\t \t - {}'.format(func_data[20:]))

        
        
        
        # Slice Timing
        print('\t \t \t % Slice Timing Correction - SPM')
        st = SliceTiming()
        st.inputs.in_files = func_data_cor
        st.inputs.num_slices = n_slices
        st.inputs.time_repetition = t_r
        st.inputs.time_acquisition = t_r - t_r/n_slices
        st.inputs.slice_order = slice_ordering
        st.inputs.ref_slice = 1
        st.run()

        # Realignement (Motion Correction)
        print('\t \t \t % Realignement Motion Correction - SPM')
        realign = Realign()
        realign.inputs.in_files = a_func
        realign.inputs.register_to_mean = True
        realign.run() 
        
        
        # Coregistration
        print('\t \t \t % Coregistration - SPM')
        coreg = Coregister()
        coreg.inputs.target = paths_anat
        coreg.inputs.source = r_func
        coreg.out_prefix ='w'
        coreg.run() 


        # Spatial Normalization
        print('\t \t \t % Spatial Normalization - SPM')
        norm12 = spm.Normalize12()
		norm12.inputs.tpm = 'MNI.nii'
		norm12.inputs.apply_to_files = w_func
		norm12.run()





    

t2 = time.time()

print('Done Successfully in {} minutes !'.format((t2-t1)/60))

