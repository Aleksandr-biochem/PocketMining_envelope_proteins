# Cryptic pocket mining in surface proteins of enveloped viruses

This repository contains code and data from the project "Assessment and application of the PocketMiner model for cryptic pocket discovery with the example of SARS-CoV-2 Spike and Ebola virus glycoproteins trimers"

**Contents:**
1. [Project summary](#sec1) </br>
2. [Structure of the repository](#sec2) </br>
3. [General guidelines on PocketMiner application to multimer envelope proteins](#sec3) </br>

<a name="sec1"></a>
## 1. Project summary

Structural characterisation and investigation of the surface proteins of enveloped viruses (such as SARS-CoV-2, Ebola virus, HIV-1 and many other) is crucial for development of new treatments. One of the tasks in this field is discovery of cryptic pockets, pockets which only open in presence of a binding partner. Such pockets represent prominent druggable sites, however they are usually invisible in experimental structures or classical MD simulations. Cryptic pockets can be discovered experimentally through co-crystallisation with a right inding partner or through special MD simulations. 

Recently [PocketMiner deep learning model](https://www.nature.com/articles/s41467-023-36699-3) was developed and shown to predict locations of cryptic pocket opening using protein structure as an input. This model could be of interest to analyse surface proteins of enveloped proteins potentially identifying new druggable sites.
However, surface proteins are multimer assemblies, while the model was trained and tested using single-chain proteins of mostly globular shape. 

Therefore, the aim of this project was to assess the performance of PocketMiner model on class I surface proteins of enveloped viruses using the example of SARS-CoV-2 Spike trimer, for which a detailed data on cryptic pockets and conformational dynamics is available. Next, the model was applied to investigate potential pockets sites in Ebola virus glycoprotein.

<a name="sec2"></a>
## 2. Structure of the repository

- `vis_PocketMiner.py` a Python script for PyMol to visualise the protein coloured by PocketMiner (PM) probabilities for each residue. Open PyMol, load PM output pdb file
- `SARS_CoV_2_spike` contains data and code for the analysis of Spike protein structures. This folder contains 15 subfolders with files for trimer structures. Subfolders are named by PDB code and the state of RBD in this structure. Each subfolder contains original PDB file, processed versions of the file, PM output file, fpocket output directory. For 3 structures (6VXX, 7KNI, 6ZGE) there are also directories with randomised sequence structures prepared using FASPR server. Other files in the folder:
  -   `Spike_protein_structure_preparation_for_PocketMiner.ipynb` performs preparation of Spike trimer structures downloaded from PDB for PM processing and also describes alignment of PocketMiner and fpocket outputs into matrices
  -   `Spike_protein_PocketMiner_visualisation.ipynb` performs visualisation and density-based clustering of PM predictions
  -   `Spike_protein_PocketMiner_data_analysis.ipynb` a more detailed analysis of PM predictions, their relation to presence of cavities detected with fpocket, dependence on RBD state and with the focus on 3 known cryptic pockets of Spike protein
  -   `SARS_CoV_2_structure_analysis.Rmd` R markdown describing statistical analysis of PM predictions by state of the S protein and in relation to cavities detected with fpocket
  -   `data` folder contains matrices with PM and fpocket predictions, CSV tables for analysis in R (`Spike_protein_PocketMiner_data_analysis.ipynb`). **See file** `Spike_data_combined.xlsx` for combined matrices with fpocket and PM predictions for each chain in each structure. The matrices are coloured by PM/fpocket values for convenience of visual inspection.
  -   `fpocket_runs.sh` bash script launching fpocket runs
  -   `S_full_nogly.pdb` is a [reconstructed model of full Spike protein](https://www.sciencedirect.com/science/article/pii/S0969212622001800)
  -   `S_protein.fasta` is a reference Spike protein sequence. `Spike_sequences.fasta` contains sequences from analysed files. `Spike_sequences_aligned.fa` alignment of Spike sequences generated with MUSCLE algorithm in UGENE.
- `Ebola_glycoprotein` contains files and code from the analysis of Ebola virus glycoprotein (GP) structures. There are 6 folders named by PDB codes and containing files named in the same manner to those in `SARS_CoV_2_spike` directories
  -   `Ebola_glycoprotein_analysis.ipynb` performs structure preprocessing, extraction and alignment of PM predictions and density-based clustering
  -   `EG_PocketMiner_data.xlsx` contains a matrix with aligned PM predictions for GP structures. Cells are coloured by PM probabilities of the corresponding residues (`PocketMiner_data.csv` is a CSV version of this matrix)
  -   `fpocket_runs.sh` bash script launching fpocket runs
  -   `EG_protein.fasta` is a reference GP sequence. `EG_sequences.fasta` contains sequences from analysed files. `EG_sequences_aligned.fa` alignment of GP sequences generated with MUSCLE algorithm in UGENE.     

<a name="sec3"></a>
## 3. General guidelines on PocketMiner application to multimer envelope proteins

Overall, assessment of PM model on 15 Spike protein structures demonstrates that the model retains at least some predictive power when applied to envelope protein trimers.
This allows to apply model to Ebola GP structures and locate potential cryptic pcoket site. 

A multimer pritein needs to be preprocessed to be an input for PM model. Follow instructions and code described in `Spike_protein_structure_preparation_for_PocketMiner.ipynb` and `Ebola_glycoprotein_analysis.ipynb` to do that.
In general, the steps are:

1. Download the PDB structure of a desired trimer. In case a structure is a biological assembly with several states (like GP structures), one could split the states in PyMol using `split_states file_name` command and resave this file.
2. Strip binding partner leaving only the target protein trimer. Save it as separate file.
3. Renumber the residues in trimer so that every residue has a unique identifyer (use code from one of the notebooks). In case the trimer file has repeating chain names, it may require manual chain renaming for unambiguous processing (see `Ebola_glycoprotein_analysis.ipynb`)
4. Clean disordered atoms if any (use code from one of the notebooks)
5. Rename all chains to A (could be done in PyMol as `select all` + `alter sele,chain='A'`). When saving the structure, it is recomended to omit UNK residues if any (could be done in PyMol as `select not resn UNK` and saving selected atoms only)
6. Prepared structure can be then processed with [PocketMiner web-server](https://pocketminer.azurewebsites.net). One can save output pdb file containing assigned probabilities in the last column.

When choosing a structure for analysis and interpreting teh results, the following points should be used:

- The bigger is the structure the harder are results to interpret
- The model was not directly trained on proteins with gaps longer than 4 residues. Therefore using the most complete structure is beneficial
- It may be helpful to analyse several representative structures of the protein and compare results
- When choosing the likely locations of cryptic pocket opening based on Pm prediction, the primary way to interpret the results is visual. Use code in 'Spike_protein_PocketMiner_visualisation.ipynb' to visualise structures coloured by PM probabilities of the residues or `vis_PocketMiner.py` for PyMol visualisation.
- Selection of likely cryptic pocket locations may be assisted by [fpocket](https://github.com/Discngine/fpocket/tree/master). Run your structure through fpocket and see if there are areas accumulation many residues with high probability and also no contacting volume. Those may be the real cryptic pocket locations.
- One may also try density-based clustering with DBSCAN algorithm to prioritise areas with most dense aggregation of the high probability residues (see last section of 'Spike_protein_PocketMiner_visualisation.ipynb' for details). DBSCAN requires manual tuning of `min_samples` and `eps` parameters, which may also be assisted by the code in the notebook.
