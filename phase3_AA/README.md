# Auto Attack
The AA_ResNet50_standard.ipynb has the code for the standard version of Resnet50( without any changes).
- First you must download the Auto Attack folder.
- Then open the eval.py file, which is located at the following address:
```
/content/auto-attack/autoattack/examples/eval.py
```
- In line 15, you need to import your desired model
```python
from resnet import *
```
- There are 4 resnet50 models you can use 
  1. ResNet50_standard -> Resnet50 model without change
  2. ResNet50_addpool -> Resnet50 model with extra pooling layer
  3. ResNet50_nopool -> Resnet50 model without pooling layers
  4. ResNet50_nobatch -> Resnet50 model without batch normalization layers

- Change the 20, 21, and 22 lines like bellow
``` 
parser.add_argument('--norm', type=str, default='Linf')
parser.add_argument('--epsilon', type=float, default=8./255.)
parser.add_argument('--model', type=str, default='./model_test.pt')
```

  • (20) Norm `L2` nad `Linf` are used in this project (use each one at need)

  • (21) Change epsilon value here

  • (22) Add location of saved model .pth file

- Write the following codes in lines 35 to 44
```
  ckpt = torch.load(args.model)
     model.load_state_dict(ckpt)
     model.cuda()
     model.eval()

     # load data
     transform_list = [transforms.ToTensor()]
     transform_chain = transforms.Compose(transform_list)
     item = datasets.CIFAR10(root=args.data_dir, train=False, transform=transform_chain, download=True)
     test_loader = data.DataLoader(item, batch_size=1000, shuffle=False, num_workers=0)
```
# Result table 
![image](https://github.com/SirAfshin/ML_Graduate_Project_TA/assets/137779903/f1f839c3-f411-44b0-9c79-03bb6ecc9589)
# Chart AA_L2
![AA-l2-chart](https://github.com/SirAfshin/ML_Graduate_Project_TA/assets/137779903/a7f779eb-13b9-4a5a-96ed-9c2c5b521cbf)
# Chart AA_Linf
![AA-Linf-chart](https://github.com/SirAfshin/ML_Graduate_Project_TA/assets/137779903/f0c0b1e2-1134-484d-8eea-c7d23bce4ed5)
