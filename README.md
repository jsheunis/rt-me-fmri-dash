# rt-me-fMRI - Interactive data visualization

This repository is contains derivative measures and interactive visualizations of the `rt-me-fMRI` dataset:
real-time multi-echo functional magnetic resonance imaging. *more information to be added*

It is built with the Plotly Dash framework in an effort to make scientific data accompanying a study more **accessible**, **interactive**, **useful** and **open**.

...
*more information to be added*
...

## Installation and use

In order to run the app in your local browser, you will need to:

- Download this GitHub repository, which contains all required code and data
- Set up a local Python environment and install several Python packages.
- Run the app locally

## Python setup

I use miniconda3 (Python 3.8) to set up my virtual environments. Once miniconda3 is installed, run the following to create a virtual environment, after inserting an appropriate environment name:

```
conda create -n [insert-environment-name-here] python
``` 

Once the environment is created, activate the environment as follows:

```
conda activate [insert-environment-name-here]
``` 

Now navigate to your extracted or cloned repository:

```
cd [path/to/folder/rt-me-fmri]
``` 

Then install the required Python packages:

```
pip install requirements.txt
``` 

## Run the app

Once the environment is active and all required packages are installed, run the following from the repo directory:

```
python index.py
``` 

This should start the app, which is accessible in your browser at this address:
[http://127.0.0.1:8050/](http://127.0.0.1:8050/)
