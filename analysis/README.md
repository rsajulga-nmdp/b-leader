This repository contains the code used to create Tables 1, 2, and 4 for the associated manuscript: 

*Assessment of HLA-B Genetic Variation with an HLA-B Leader Tool and Implications in Clinical Transplantation*

The data contains sequences and metadata for the subjects is absent but available on request.

# Setup

To begin, ensure that you have Python3 installed. To check, issue this command to verify your python version:
```
python --version
```

If Python3 is not installed, please download it from [here](https://www.python.org/downloads/).

If Python3 is readily available, set up your virtual environment by running these commands:
```
python3 -m venv venv
source venv/bin/activate
```

Pip is the package installer for Python. It comes pre-packaged with Python. This will be used to install our requirements as such:
```
pip install --upgrade pip
pip install -r requirements.txt
```

Once the virtual environment is created, activated, and installed with requirement dependencies, you should make the environment available for Jupyter notebooks via an IPython kernel. To do so, run the following:
```
python -m ipykernel install --user --name=analysis_env
```

Once finished, you'll be available to select the Kernel within your Jupyter notebook on the menu bar: **Kernel** > **Change kernel** > *analysis_env*

# Data Preparation

Data analyzed by `leader_analysis.ipynb` needs to be in .fasta format. For example:
```
\>id|project|method|source|Homozygous1|allele_string
AAACCCTTTGGG
\>id|project|method|source|Homozygous2|allele_string
AAACCCTTTGGG
```

Create your own directory for data `mkdir data/` and place your input files (in .fasta or HML format [.xml])

## HML to .fasta

If using [HML](https://bioinformatics.bethematchclinical.org/hla-resources/hml/) files, the following scripts are helpful.

### HML to Sequences
To convert from HML files to sequences, use hml2seq.jar ([source](https://github.com/nmdp-bioinformatics/hml-to-sequence)). For example, if you create a subfolder `hml_files` within `data` to contain your HML files, then use the following command to create a `data/hla_sequences.txt` output:
`java -jar src/hml2seq.jar data/hml_files/ data/hla_sequences.txt`

Then, you must convert those sequence files into .fasta files using hla2fa.jar ([source](https://github.com/nmdp-bioinformatics/hla-to-fasta)). 
```
java -jar src/hla2fa.jar data/hla_sequences.txt
```

### Sequences to .fasta
You will then have sequences for each locus in the root directory. You may organize your sequences using the following commands:
```
mkdir data/sequences/
mv hla_sequences_* data/sequences/
```

If using the commands listed above, your input file will now be located at `data/sequences/hla_sequences_B.fasta` and ready for analysis through `leader_analysis.ipynb`.