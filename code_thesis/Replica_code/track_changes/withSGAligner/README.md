`3DSSG_MOD`: contains the code to get the DSSGs associated to the 3RScan dataset

`sgaligner_MOD_3RScan`: contains the code to process the 3RScan dataset. The final step is to run `sgaligner_MOD_3RScan\src\inference\sgaligner\inference_align_reg__runTerminal.py`

`sgaligner_MOD_Replica`: contains the code to process the Replica dataset. First of all, one needs to get the checkpoint to be used with Replica (use `sgaligner_MOD_Replica\src\inference\sgaligner\GAIA_modify_ckp_POINTS.py`). Execute the preprocessing in `sgaligner_MOD_Replica/preprocessing/replica`. The final step will be to run `sgaligner_MOD_Replica_alignPCD\src\inference\sgaligner\inference_align_reg.py`
