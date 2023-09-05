# Cryptic pocket mining in surface proteins of enveloped viruses

This repository contains code and data from the project "Assessment and application of the PocketMiner model for cryptic pocket discovery with the example of SARS-CoV-2 Spike and Ebola virus glycoproteins trimers"

**Contents:**
1. [Project summary](#sec1) </br>
2. [Structure of the repository](#sec2) </br>
3. [General guidelines on PocketMiner application to multimer envelope proteins](#sec3) </br>

<a name="sec1"></a>
## 1. Project summary

Structural investigation of the surface proteins of enveloped viruses (such as SARS-CoV-2, Ebola virus, HIV-1 and many other) is crucial for development of new treatments. One of the tasks in this field is discovery of cryptic pockets, which are recognised as prominent druggable sites. Such pockets open only in presence of a binding partner, hence they are usually invisible in experimental structures or classical MD simulations. Cryptic pockets can be discovered experimentally through co-crystallisation with a right binding partner or through special MD simulations. 

Recently a [PocketMiner deep learning model](https://www.nature.com/articles/s41467-023-36699-3) was developed and tested to predict locations of cryptic pocket opening using protein structure as an input. This model could be of interest to analyse viral surface proteins potentially identifying new druggable sites.
However, surface proteins are multimer assemblies, while the PocketMiner model was trained and tested using single-chain proteins of mostly globular-like shape. 

Therefore, the aim of this project was to assess the performance of PocketMiner model on class I surface proteins of enveloped viruses using the example of SARS-CoV-2 Spike (S) trimer, for which a detailed data on cryptic pockets and conformational dynamics is available. Next, the model was applied to investigate potential pocket sites in Ebola virus glycoprotein (GP).

<a name="sec2"></a>
## 2. Structure of the repository

The scheme below illustrates the workflow of structure processing with the example of SARS-CoV-2 Spike protein: 

<p align="center">
  <img src="/SARS_CoV_2_spike/data/workflow.jpg" width="800">
</p>

- `vis_PocketMiner.py` a Python script for PyMol to visualise a protein coloured by PocketMiner (PM) probabilities for each residue. Open PyMol, load PM output PDB file and execute the scripth in PyMol prompt as `run relative/path/to/vis_PocketMiner.py` (run `pwd` in promt to make sure that the working directory is the directory with loaded PDB file).
- `SARS_CoV_2_spike` contains data and code for the analysis of S protein structures. This folder contains 15 subfolders with trimer structures. Subfolders are named by PDB code and the state of RBD in each structure. Each subfolder contains original PDB file, processed versions of the file, PM output file, fpocket output directory. For 3 structures (6VXX, 7KNI, 6ZGE) there are also directories with randomised sequence structures prepared using [FASPR server](https://zhanggroup.org/FASPR/). Other files in the folder:
  -   `Spike_protein_structure_preparation_for_PocketMiner.ipynb` performs preparation of S trimer structures for PM processing and alignment of PocketMiner and fpocket outputs into matrices
  -   `Spike_protein_PocketMiner_visualisation.ipynb` performs visualisation and density-based clustering of PM predictions
  -   `Spike_protein_PocketMiner_data_analysis.ipynb` a more detailed analysis of PM predictions, their relation to presence of cavities detected with fpocket, dependence on RBD state with the focus on 3 known cryptic pockets of S protein
  -   `SARS_CoV_2_structure_analysis.Rmd` R markdown describing statistical analysis of PM predictions by S protein state and in relation to cavities detected with fpocket
  -   `data` folder contains matrices with PM and fpocket predictions, CSV tables for analysis in R (see `Spike_protein_PocketMiner_data_analysis.ipynb` for details). **See file** `Spike_data_combined.xlsx` for combined matrices containing fpocket and PM predictions for each chain in each structure. These matrices are colourcoded for convenience of visual inspection. `Spike_6VXX_DBSCAN_example.jpg` provides an example of DBSCAN clustering results on Spike protein structure with PM predictions.
  -   `fpocket_runs.sh` bash script launching fpocket runs
  -   `S_full_nogly.pdb` is a [reconstructed model of full Spike protein](https://www.sciencedirect.com/science/article/pii/S0969212622001800)
  -   `S_protein.fasta` is a reference S protein sequence. `Spike_sequences.fasta` contains S sequences from 15 analysed files. `Spike_sequences_aligned.fa` is an alignment of S sequences generated with MUSCLE algorithm in UGENE software.
- `Ebola_glycoprotein` contains files and code for the analysis of Ebola virus glycoprotein (GP) structures. There are 6 folders named by PDB codes containing files named in the same manner to those in `SARS_CoV_2_spike` directories. Other contents:
  -   `Ebola_glycoprotein_analysis.ipynb` performs structure preprocessing, extraction and alignment of PM predictions and density-based clustering
  -   `EG_PocketMiner_data.xlsx` contains a colourcoded matrix with aligned PM predictions for GP structures (`PocketMiner_data.csv` is a CSV version of this matrix)
  -   `fpocket_runs.sh` bash script launching fpocket runs
  -   `EG_protein.fasta` is a reference GP sequence. `EG_sequences.fasta` contains sequences from 6 analysed files. `EG_sequences_aligned.fa` is an alignment of GP sequences generated with MUSCLE algorithm in UGENE software.     

<a name="sec3"></a>
## 3. General guidelines on PocketMiner application to multimer envelope proteins

Overall, the assessment of PM model on 15 Spike protein structures demonstrates that the model retains some predictive power when applied to envelope protein trimers.
This allows PM application to Ebola GP structures to locate a potential cryptic pcoket site. 

A multimer pritein requires preprocessing to be a valid input for PM model. Follow instructions and code described in `Spike_protein_structure_preparation_for_PocketMiner.ipynb` and `Ebola_glycoprotein_analysis.ipynb` to perform such preprocessing for structures of interest.
In general, the steps are:

1. Download the PDB structure of a desired trimer. In case the structure is a biological assembly with several states (like GP structures), one could split the states in PyMol using `split_states file_name` command and resave this model.
2. Strip binding partners leaving only the target protein trimer (can be done in Chimera X or other molecular viewer) and save it as separate file.
3. Renumber the residues in trimer so that every residue has a unique identifyer (use code from one of the mentioned notebooks). In case the trimer file has repeating chain names, a manual chain renaming is required for unambiguous processing (see `Ebola_glycoprotein_analysis.ipynb`)
4. Clean disordered atoms (use code from one of the mentioned notebooks)
5. Rename all chains to A (could be done in PyMol as `select all` + `alter sele,chain='A'`). When saving the structure, UNK residues should be omitted (could be done in PyMol as `select not resn UNK` and saving selected atoms only)
6. The structure with single chain and renumbered residues can be then processed with [PocketMiner web-server](https://pocketminer.azurewebsites.net). PDB file containing assigned probabilities in the last column is then available for download and visualisation.

When choosing a structure for analysis and interpreting the results, the following points should be minded:

- **PM model was not trained on multimer proteins**. Even though assessment on S trimer structures suggests that the model produces reasonable predictions, the accuracy and general quality of predictions should be expected to drop compared to smaller single-chain proteins. Treat results critically.
- **The bigger is the structure the more noised and harder to interpret are the predictions**. PM predictions for S trimers have a complicated landscape of residues with pocket probabilities >0.5. At least 20% of such residues could not be related to known cryptic pcokets or conformationally flexible residues. Nevertheless, for a smaller GP structure the results seem to be more straightforward. **It may be beneficial to apply PM to individual protein domains** as PM model focuses on local environment of the residue when degenrating a prediction (though this approach was not tested in this work)
- **Use most complete structures**. The model was not directly trained on proteins with gaps longer than 4 residues. Even though it was shown that pcokets with missing loops still could be detected by the model, reliability of such predictions should be treated with caution.
- **It may be helpful to analyse several representative structures of the protein and compare results**. The alignment of results from several predcitions can be assisted by code in Python notebooks from this repository.
- When choosing the likely locations of cryptic pocket opening based on PM prediction, **the primary way to interpret the results is visual inspection**. Use code in 'Spike_protein_PocketMiner_visualisation.ipynb' or `vis_PocketMiner.py` (for PyMol visualisation) to visualise structures coloured by PM probabilities of the residues.
- **Take into account presence of cavities in a protein**. Run your structure through [fpocket](https://github.com/Discngine/fpocket/tree/master) tool. Then you see if the areas accumulating residues with high PM probabilities already have an opened pocket. If no opened pocket is detected, it could be an additional sign that this area is a true cryptic pocket site.
- **Density-based clustering can additionally assist in picking the likely cryptic pocket sites from PM predictions**. DBSCAN algorithm could assist in prioritising areas with most dense aggregation of the high probability residues (see last section of 'Spike_protein_PocketMiner_visualisation.ipynb' for details). DBSCAN requires manual tuning of `min_samples` and `eps` parameters, which may also be assisted by the code in the notebook. It is more informative on smaller structures than on large proteins.
