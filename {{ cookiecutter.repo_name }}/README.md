{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

Project Organization
------------

    ├── LICENSE
    ├── snakefile          <- snakefile with workflow automation utils
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `_` delimited description, e.g.
    │                         `1.0_am_initial_data_exploration.ipynb`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions
        │   ├── predict_model.py
        │   └── train_model.py
        │
        ├── visualization  <- Scripts to create exploratory and results oriented visualizations
        │   └── visualize.py
        └──workflow.py     <- Script for running airflow
        

# Model ID: 12345678
---
## Metadata:
Model Name          : Business Development Go/Get  
Current Epicycle    : 1  
Business Owner      : Travis Shearer  
Product Ops         : Danielle Maddux  
ML Ops              : Austin Madert  
Content Refs        : CRM_001.CRM_00003  

---
### HAD Analysis

#### Key Hypotheses         : 'document here'  
#### Key Assumptions        : 'document here'  
#### Data Set Limitations   : 'document here'   

---
### Business Understanding

#### Business Requirements : <link to business requirements doc>

##### Your Text Here.
---
### Data Understanding/Sourcing

#### Data Sources       :  'document/link here'          
#### Data Acquisition   :  'document/link here' 
  
##### Your Text Here.
---
### Data Preparation

#### Data Preparation   : 'document/link here'   
#### Training Record    : 'document/link here'  
#### Train/Dev/Test Split    : Training = 14,000; Dev = 0; Test = 1,0000   
  
##### Your Text Here.
---
#### Feature Engineering

#### Metadata Tables        : 'i.e. metadata_project'
#### Engineered Features    :  'document/link here' 

##### Your Text Here.

---
### Modeling

#### Model Type     : 'document/link here' 
    
##### Your Text Here.

---
### Evaluation

#### Target Metric  : 'document/link here' 
#### Known Bias     : 'document/link here' 

##### Your Text Here. 

---
### Product Ops Considerations

#### Production CommitID        : 1213232319prnfpf3109-hf30fj1039j0  
#### Reporting/Visualization    : <link to script here>  

##### """ Document context as to how user interprets model outputs for decision-making purposes """ (probably ownder by Product Ops)

---
### Maintenance
Not applicable.  

---
### Next Steps
Your Text Here.


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
