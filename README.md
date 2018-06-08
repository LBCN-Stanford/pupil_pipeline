# pupil_pipeline hi

## About
Hello! This is a pipeline to pre-process and visualize pupil diameter data. Pupil data is first checked for quality (missing data, outliers). A plot of the raw data is saved, and descriptive statistics are calculated. Outliers are removed, and blinks are then filled in using a cubic spline interpolation. The pupil data is then optionally normalized. After this, the pupil data is then epoched according to events and conditions. There are a number of options here including the duration, and various types of baseline correction. Finally, the pupil data is plotted. This pipeline also includes code to combine data from multiple participants or blocks. This code was originally written for Laboratory of Behavioral and Cognitive Neuroscience at Stanford University.

## Setting up
1. Download python 3.6 from anaconda from this [link](https://www.anaconda.com/download/)
2. Clone this repository.
3. Put data in a convenient folder, this is especially important if you plan to run multiple files at the same time. 
4. Change behavioral data into the events format 

### Events format
Behavioral data is used to epoch the pupil data. For this to work, the pupil pipeline requires this data to be of a specific format which is described in this section. 
The behavioral file should be a MATLAB (.mat) file containing a variable named first, and another variable named events. first should be a float marking the time of the first onset of the behavioral data (in seconds). This is aligned to the first event in the eye tracking data. events is the same variable that is outputted by the ECoG preprocessing pipeline. To see what the events variable should look like, check out the template file in this 'examples/events.mat'. If instead you collected your data in python, you can use the classes defined in events_python.py 

## Parameters
This section describes the ways you can set the options for the pipeline. Parameters are kept in python (.py) files, and are passed as an argument when running the pipeline. The default parameters are kept in parameters_default.py. You can see the available options in this file, and instructions of how they work are in the code comments. To set your own parameters, I suggest making a copy of the default file, changing the contents, and passing the new file as an argument to the pipeline (details below). You will probably want a separate parameters file for each task that you have. 

## Running the pipeline
1. Open terminal (mac, linux) or command prompt (windows)
2. cd into the pipeline
3. `python pupil_pipline.py <parameters>`, where `<parameters>` is replaced with the name of the parameters file. You can also leave it empty to run the pipeline with the default parameters. 

## Outputs
After running the pipeline, there will be a new folder created with the outputs of the pipeline. This folder will be in the same folder as the folder containing the pupil data files. 

## Merging
To merge multiple files you need to have all the 'epoched' files in the same folder. To help do this quickly you can try 
```python
python gather.py
```
This will ask you to select a folder. Then it looks for all the files with both 'epoched' and '.mat' in all the subfolders of the selected folder and copies them into a new folder called Gathered.

Running the merge code is just like pipeline
```python
python merge.py <parameters>
```
Parameters for merge can be specified in the same file.

The outputs are saved into the folder containing all of the epoched files. 

Please reach out if you have any questions about the pipeline!
