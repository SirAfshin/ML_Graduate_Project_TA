# Participants
- Ahmadreza Horobi
- Mohammad Barati Dehaghi

# Phase 3 
This phase consist of testing robustness of the already trained models in phase 1 with DDN and AutoAttack.
All .pth and .py files are saved on google drive.

# Phase 1 
## Update 
The code has been changed so it can test resnet50 architecrute.

## ML_Graduate_Project_TA
This repository contains the code related to the image project for the advanced machine course taught by Dr. Seyedin.

### Dependencies

To install dependences on google colab use code bellow:
```python
import warnings
warnings.filterwarnings('ignore')
!pip install -q git+https://github.com/RobustBench/robustbench.git@2d630bc9e8d1cf50d46a4dda65fd36850e3ef769
```
make sure to run this code twice for it to work!

### Usage
Before running the code you need to store all .pth files in the address bellow:
instead of * use the name of your model, you should change it inside test.py as well.
```python
model_path_drive  = '/content/drive/MyDrive/ML_VIsion/RobustBench_test/*.pth'

```
After that you need to bring all your resnet.py architectures to the directory your code is in and move them in folder models, then modify the import inside the code.
```python
from models.resnet import ResNet50

```
Then you can run the code using this line of code in google colab.
```python
!python test.py

```

## Keep in mind
The code was meant to run on google colab so if you want to run it locally you need to change it yourself!
