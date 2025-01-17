# In the name of Allah
# Author : Alireza Abdollapourrostam
# ML Graduate
import logging
import argparse
from robustbench import load_cifar10, load_model
from robustbench.data import load_cifar100

# from models.resnet_addpool import ResNet50 # importing resnet50 model and change every model to resnet50
# from models.resnet_nobatch import ResNet50 # importing resnet50 model and change every model to resnet50
# from models.resnet_nopool import ResNet50 # importing resnet50 model and change every model to resnet50
from models.resnet_standard import ResNet50 # importing resnet50 model and change every model to resnet50


# I should note that to run this script, it is necessary to create a model folder and a state_dict inside it.
from utils import *

# define required paths on google drive

# model_path_drive = "/content/drive/MyDrive/ML_VIsion/RobustBench_test/resnet_addpool.pth"
# model_path_drive = "/content/drive/MyDrive/ML_VIsion/RobustBench_test/resnet_nobatch.pth"
# model_path_drive = "/content/drive/MyDrive/ML_VIsion/RobustBench_test/resnet_nopool.pth"
model_path_drive = "/content/drive/MyDrive/ML_VIsion/RobustBench_test/resnet_standard.pth"
result_path = '/content/drive/MyDrive/ML_VIsion/RobustBench_test/results/cifar10/results.log'

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Please Create a folder named results in the root directory of the project for saving the results in results.log
file_handler = logging.FileHandler(result_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
file_handler.stream.write('##########################################################3\n')
file_handler.flush()

######### parser #############
parser = argparse.ArgumentParser()

parser.add_argument("--sample", type=int, help="number of samples", default=100)
parser.add_argument("--bs", default=100, type=int, help="batch size")
parser.add_argument("--model",default="ResNet50",type=str,help="model name")
args = parser.parse_args()
n_examples = args.sample
batch_size = n_examples

def create_CIFAR10_loader(n_examples = n_examples ,batch_size = batch_size, shuffle=True):
    
    images, labels = load_cifar10(n_examples=n_examples, data_dir='data/torchvision')
    test_dataset = torch.utils.data.TensorDataset(images, labels)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=shuffle)
    
    
    return test_loader

def cifar10_test(device, model_name: str = 'ResNet50',batch_size = batch_size, n_examples = n_examples,checkpoint_type: str='pth'):
    batch_size = batch_size
    os.makedirs(os.path.join('data', 'torchvision'), exist_ok=True)
    os.makedirs(os.path.join('results', 'cifar10'), exist_ok=True)

    n_examples = n_examples
    images, labels = load_cifar10(n_examples=n_examples, data_dir='data/torchvision')
    test_dataset = torch.utils.data.TensorDataset(images, labels)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    if  checkpoint_type == 'pth':
        if model_name == 'ResNet50' :
            model = ResNet50()
            model = nn.DataParallel(model)
            checkpoint = torch.load(model_path_drive)
            model.load_state_dict(checkpoint['net'])
            model = normalize_model(model, mean = (.4914, 0.4822, 0.4465), std = (0.2023, 0.1994, 0.2010))
        # elif model_name == 'vgg' :
        #     model = vgg16_bn(pretrained=True)
        #     model = normalize_model(model, mean = (.4914, 0.4822, 0.4465), std = (0.2471, 0.2435, 0.2616))
            
        else:
            raise ValueError(f"Model {model_name} not found")
    
    elif  checkpoint_type == 'pt':
        if model_name == 'ResNet50':
            model = ResNet50()
            model = nn.DataParallel(model) # note that please check the repo, if it uses the Dataprallel use this line!
            model.load_state_dict(torch.load(r"ckpth.pth"))
            model = normalize_model(model, mean = (.4914, 0.4822, 0.4465), std = (0.2023, 0.1994, 0.2010))
        # elif model_name == 'vgg':
        #     model = vgg16_bn(pretrained=True)
        #     model = nn.DataParallel(model) # note that please check the repo, if it uses the Dataprallel use this line!
        #     model.load_state_dict(torch.load(r"ckpth.pth"))
        #     model = normalize_model(model, mean = (.4914, 0.4822, 0.4465), std = (0.2471, 0.2435, 0.2616))
            
        else:
            raise ValueError(f"Model {model_name} not found")
        
    
    torch.cuda.empty_cache()
    accuracy_orig = clean_accuracy(model.to(device), images.to(device), labels.to(device),batch_size=batch_size, device=device)
    print(f"Accuracy of {model_name} model: {accuracy_orig}")
    logger.info(f"Accuracy of {model_name} model: {accuracy_orig}")
    requires_grad_(model, False)
    
    return model, test_loader


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(f"device is :{device}")


def main(args = args):
    model, test_loader = cifar10_test(device, model_name=args.model,checkpoint_type='pth')



if __name__ == '__main__':
    main(args = args)
    