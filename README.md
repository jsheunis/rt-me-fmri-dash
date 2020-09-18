# rt-me-fMRI - Interactive data visualization

This repository contains derivative measures and interactive visualizations of the `rt-me-fMRI` dataset:
real-time multi-echo functional magnetic resonance imaging. *more information to be added*

It is built with the Plotly Dash framework in an effort to make scientific data accompanying a study more **accessible**, **interactive**, **useful** and **open**.

...
*more information to be added*
...

## Installation and use

In order to run the app in your local browser, you will need to:

1. Download this GitHub repository, which contains all required code.
2. Download the required data, which is currently only possible via a secure download link.
3. Set up a local Python environment and install several Python packages.
4. Run the app locally

## 1. Download code

If you have `git` installed locally, you can clone the repository using your preferred method.

If not, you can click and the green `Code` button above and select the `Download ZIP` option.
Unzip the file and place the `rt-me-fmri-dash` directory with all its contents in a sensible location.


## 2. Download data

If you have not received it yet, please request a download link from the repository owner.

The link will download a zipped file named `rt-me-fmri-data` to your machine.
Unzip the file and place the `rt-me-fmri-data` directory with all its contents in the same location as the `rt-me-fmri-dash` directory.
***It is very important that they are located on the same level.***  

## 3. Python setup

The Dash app requires several Python packages to be installed.
It is highly recommended to set up a virtual environment in order to manage the Python environment and in which to install required packages.
Instructions for miniconda3 (Python 3.8) are given here, but you are free to use whichever virtual environment manager you prefer.

Once miniconda3 is installed, run the following from your terminal to create a virtual Python environment.
Remember to first insert an appropriate environment name:

```
conda create -n [insert-environment-name-here] python
``` 

Once the environment is created, activate the environment as follows:

```
conda activate [insert-environment-name-here]
``` 

Now navigate to your extracted or cloned `rt-me-fmri-dash` directory:

```
cd [path/to/directory/rt-me-fmri-dash]
``` 

Then install the required Python packages as follows:

```
pip install requirements.txt
``` 

## Run the app

Once the environment is active and all required packages are installed, run the following from the `rt-me-fmri-dash` directory:

```
python index.py
``` 

This should start the app, which is accessible in your browser at this address:
[http://127.0.0.1:8050/](http://127.0.0.1:8050/)
