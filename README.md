# Hi5: Robust 2D Hand Pose Estimation for Real-World Applications Using Synthetic Data Alone

## Dataset Download:
- Link: https://www.dropbox.com/scl/fo/cs5bdynig2a8jazpomul7/AFJ_f9mKHxlsrR60eGn0SRU?rlkey=tw1y19spyxtsca94pz6on2z1j&st=uduvogbm&dl=0


## Unity Game Engine Project
- Same dropbox link above
- Doesn't contain the hand models
- For game engine project setup, please follow `unity-setup-guide.md`


## Data Augmentation
- The `data_processing/` directory contains code for processing, and augmenting the synthetic data.


## Training Code
- For Training and Evaluation, please use ViTPose repository:
https://github.com/ViTAE-Transformer/ViTPose
- Please follow the training and evaluation instructions from the repository.
- To reproduce our results, add the content in the `config` files to `ViTPose/configs/hand/2d_kpt_sview_rgb_img/topdown_heatmap/`
- Exact command line arguments used in this study can be seen in `terminal commands.md` file.
- Trained checkpoints in Dropbox

## Other datasets
- OneHand10K: https://www.yangangwang.com/papers/WANG-MCC-2018-10.html
- 11k hands: https://sites.google.com/view/11khands

