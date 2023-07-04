import torch

if torch.cuda.is_available():
    print("CUDA is available. PyTorch is using GPU.")
else:
    print("CUDA is not available. PyTorch is using CPU.")
