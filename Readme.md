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

2. Then you must enter to AISY_Framework:
    ```
    cd AISY_Framework
    ```
3. Create a Python environment using conda (The Python version is very important):
   ```
   conda create --name DLSCAenv python=3.8
   ```
4. Activate de environment:
    ```
   conda sctivate DLSCAenv
   ``` 
5. **Important Step** Install the requirements of this project (NOT the AISY-framework requirements) delete the AISY-framework requirements and paste this requirements.txt -> [code/requirements.txt](/code/requirements.txt)

6. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
7. dfs