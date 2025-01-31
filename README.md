# Hi5: Robust 2D Hand Pose Estimation for Real-World Applications Using Synthetic Data Alone

## Dataset Download:
- Link: https://www.dropbox.com/scl/fo/cs5bdynig2a8jazpomul7/AFJ_f9mKHxlsrR60eGn0SRU?rlkey=tw1y19spyxtsca94pz6on2z1j&st=uduvogbm&dl=0


## Unity Game Engine Project



## 3D Hand Model used in this study:
- https://assetstore.unity.com/packages/3d/characters/humanoids/leap-motion-realistic-male-hands-109961


## Data Augmentation
- The `data_processing/` directory contains code for processing, and augmenting the synthetic data.


## Training Code
- For Training and Evaluation, please use ViTPose repository:
https://github.com/ViTAE-Transformer/ViTPose
- Please follow the training instructions from the repository.
- For using Hi5 and OneHand10k train and evaluation used in the paepr, see the config files in `config/` directory.
- To reproduce our results, add the content in the `config` files to `ViTPose/configs/hand/2d_kpt_sview_rgb_img/topdown_heatmap/`



