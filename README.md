# OC_Finder
<a href="https://github.com/marktext/marktext/releases/latest">
   <img src="https://img.shields.io/badge/OC_Finder-v1.0.0-green">
   <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Mac%20-green">
   <img src="https://img.shields.io/badge/Language-python3-green">
   <img src="https://img.shields.io/badge/dependencies-tested-green">
   <img src="https://img.shields.io/badge/licence-GNU-green">
</a>       


OF_Finder is a computational tool using deep learning for osteoclast segmentation, classification, and counting.

Copyright (C) 2021 Xiao Wang*, Mizuho Kittaka*, Yilin He, Yiwei Zhang, Yasuyoshi Ueki, Daisuke Kihara, and Purdue University. 

License: GPL v3 for academic use. (For commercial use, please contact us for different licensing.)

Contact: Daisuke Kihara (dkihara@purdue.edu)

## Citation:
Xiao Wang*, Mizuho Kittaka*, Yilin He, Yiwei Zhang, Yasuyoshi Ueki & Daisuke Kihara. OC_Finder: A deep learning-based software for osteoclast segmentation, classification, and counting. (2021).

```
@article{wang2021oc_finder,   
  title={OC_Finder: A deep learning-based software for osteoclast segmentation, classification, and counting},   
  author={Xiao Wang*, Mizuho Kittaka*, Yilin He, Yiwei Zhang, Yasuyoshi Ueki, and Daisuke Kihara},    
  journal={},    
  year={2021}    
}   
```

## Training Dataset: [!]()
## Introduction

Osteoclasts are multinucleated cells that exclusively resorb bone matrix proteins and minerals on the bone surface. They differentiate from monocyte/macrophage-lineage cells in the presence of osteoclastogenic cytokines such as receptor activator of nuclear factor-kB ligand (RANKL) and are stained positive for tartrate-resistant acid phosphatase (TRAP). In vitro, osteoclast formation assay is commonly used to assess the capacity of osteoclast precursor cells for differentiating into osteoclasts, where the number of TRAP-positive multinucleated cells are counted as osteoclasts. Osteoclasts are manually identified on cell culture dishes by human eyes, which is a labor-intensive process. Moreover, the manual procedure is not necessarily objective and brings the lack of reproducibility. To accelerate the process and reduce the workload for counting the number of osteoclasts, here we developed OC_Finder, a fully automated system for identifying osteoclasts in microscopic images. OC_Finder consists of segmentation and classification steps. For segmentation, the Otsu’s binarization method was combined with morphological opening and the watershed algorithm. For classification, we used convolutional neural networks. OC_Finder detected osteoclasts differentiated from wild-type and Sh3bp2KI/+ precursor cells at a 95.37% accuracy for segmentation and at a 96.04% accuracy for classification. Furthermore, the number of osteoclasts classified by OC_Finder was at the same accuracy level with manual counting by a human expert. Together, successful development of OC_Finder suggests that deep learning is a useful tool to perform prompt and accurate classification and detection of specific cell types in microscopic images with no bias。

## Overall Protocol
```
1) Segment the input micrscopy image by watershed algorithm;
2) Filter out small cells;
3) Locate the input candidate image for classification;
4) Trained deep learning model make classifications for candidate cell images;
5) Output the detection results.
```
<p align="center">
  <img src="figures/framework.jpeg" alt="framework" width="90%">
</p> 

### Network Architecture
<p align="center">
  <img src="figures/network.jpeg" alt="framework" width="90%">
</p> 

## Pre-required software
Python 3 : https://www.python.org/downloads/    
pdb2vol (for generating simulated maps): https://situs.biomachina.org/fguide.html   
Pymol(for visualization): https://pymol.org/2/        

## Installation  
### 1. [`Install git`](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) 
### 2. Clone the repository in your computer 
```
git clone https://github.com/kiharalab/OC_Finder && cd OC_Finder
```

### 3. Build dependencies.   
You have two options to install dependency on your computer:
#### 3.1 Install with pip and python(Ver 3.6.9).
##### 3.1.1[`install pip`](https://pip.pypa.io/en/stable/installing/).
##### 3.1.2  Install dependency in command line.
```
pip3 install -r requirement.txt --user
```
If you encounter any errors, you can install each library one by one:
```
pip3 install Pillow==6.2.2
pip3 install numpy==1.18.2
pip3 install pandas==1.0.3
pip3 install opencv-python==4.1.2.30
pip3 install matplotlib==3.2.1
pip3 install torch==1.1.0
```

#### 3.2 Install with anaconda
##### 3.2.1 [`install conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html). 
##### 3.2.2 Install dependency in command line
```
conda create -n OC_Finder python=3.6.9
conda activate OC_Finder
pip install -r requirement.txt 
```
Each time when you want to run my code, simply activate the environment by
```
conda activate OC_Finder
conda deactivate(If you want to exit) 
```

## Usage

