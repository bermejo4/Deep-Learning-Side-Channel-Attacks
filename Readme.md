# DEEP LEARNING SIDE CHANNEL ATTACKS
--------
--------

## DATASETS PREPROCESSING PROCESS:

![code_flowchart.png](/doc/images/code_flowchart.png)

--------

## AISY FRAMEWORK INSTALLATION:

1. You must clone the repository from: https://github.com/AISyLab/AISY_Framework
    ```
    git clone https://github.com/AISyLab/AISY_Framework.git
    ```

2. Create a Python environment using conda (Python version is very important):
   ```
   conda create --name DLSCAenv python=3.8
   ```
3. Activate de environment:
    ```
   conda activate DLSCAenv
   ``` 
4. Then, enter to AISY_Framework:
    ```
    cd AISY_Framework
    ```
5. **Important Step** Install the requirements of this project (NOT the AISY-framework requirements) delete the AISY-framework requirements and paste this requirements.txt -> [code/requirements.txt](/code/requirements.txt). These are the main differences, but with the old requirements, the installation doesn't work because some libs are deprecated: ![diff requirements](/doc/images/requirements_diff.png)

6. Go to the same directory where is the requirements.txt file and install it with this command:
   ```
   pip install -r requirements.txt
   ```
7. To test it you can enter to AISY_Framework folder and run:
   ```
   flask run
   ```