# Following are the terminal commands used in this study with the config files
To run this, please add the corresponding config files in the `config/` directory in ViTPose repository.

## Train

bash tools/dist\_train.sh configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/hi5/ViTPose\_small\_hi5\_all\_256x192.py 4 \--cfg-options model.pretrained=weights/small\_pretrained.pth \--seed 0

### Train from checkpoint

bash tools/dist\_train.sh configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/hi5/ViTPose\_small\_hi5\_all\_256x192.py 4 \--cfg-options resume\_from=work\_dirs/ViTPose\_small\_hi5\_all\_256x192/epoch\_50.pth model.pretrained=weights/small\_pretrained.pth \--seed 0 

## Test

bash tools/dist\_test.sh ViTPose/configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/hi5/ViTPose\_small\_hi5\_all\_256x192.py ViTPose/work\_dir/ViTPose\_small\_hi5\_all\_256x192\_500k/best\_AUC\_epoch\_48.pth 4

### Test Hi5-L

bash tools/dist\_test.sh /scratch/mhasan9/hi5/ViTPose/configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/hi5/ViTPose\_small\_hi5\_all\_256x192.py /scratch/mhasan9/hi5/ViTPose/work\_dirs/ViTPose\_small\_hi5\_all\_256x192\_500k/epoch\_49.pth 4

### Test Hi5-M

bash tools/dist\_test.sh /scratch/mhasan9/hi5/ViTPose/configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/hi5/ViTPose\_small\_hi5\_all\_256x192.py /scratch/mhasan9/hi5/ViTPose/work\_dirs/ViTPose\_small\_hi5\_all\_256x192\_100k/best\_AUC\_epoch\_125.pth 4



### Test Hi5-S

bash tools/dist\_test.sh /scratch/mhasan9/hi5/ViTPose/configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/hi5/ViTPose\_small\_hi5\_all\_256x192.py /scratch/mhasan9/hi5/ViTPose/work\_dirs/ViTPose\_small\_hi5\_all\_256x192\_10k/best\_AUC\_epoch\_179.pth 4

### Test OneHand10k

bash tools/dist\_test.sh  /scratch/mhasan9/hi5/ViTPose/configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/onehand10k/ViTPose\_small\_onehand10k\_all\_256x182.py /scratch/mhasan9/hi5/ViTPose/work\_dirs/ViTPose\_small\_onehand10k\_all\_256x182/best\_AUC\_epoch\_399.pth 4

### Test OneHand10k on Mediapipe, 11k

bash tools/dist\_test.sh  /scratch/mhasan9/hi5/ViTPose/configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/onehand10k/ViTPose\_small\_onehand10k\_all\_256x182\_11k.py /scratch/mhasan9/hi5/ViTPose/work\_dirs/ViTPose\_small\_onehand10k\_all\_256x182/best\_AUC\_epoch\_399.pth 4  


## Test Hi5L on Mediapipe

bash tools/dist\_test.sh /scratch/mhasan9/hi5/ViTPose/configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/hi5/ViTPose\_small\_hi5\_all\_256x192\_11k.py /scratch/mhasan9/hi5/ViTPose/work\_dirs/ViTPose\_small\_hi5\_all\_256x192\_500k/epoch\_49.pth 4  


## Demo

### OneHand10k

python demo/top\_down\_img\_demo.py /scratch/mhasan9/hi5/ViTPose/configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/onehand10k/ViTPose\_small\_onehand10k\_all\_256x182.py /scratch/mhasan9/hi5/ViTPose/work\_dirs/ViTPose\_small\_onehand10k\_all\_256x182/best\_AUC\_epoch\_399.pth \--img-root /scratch/mhasan9/hi5/data/onehand10k/ \--json-file /scratch/mhasan9/hi5/data/onehand10k/annotations/onehand10k\_test.json \--out-img-root vis\_results\_onehand10k

### Hi5-L

python demo/top\_down\_img\_demo.py /scratch/mhasan9/hi5/ViTPose/configs/hand/2d\_kpt\_sview\_rgb\_img/topdown\_heatmap/hi5/ViTPose\_small\_hi5\_all\_256x192.py /scratch/mhasan9/hi5/ViTPose/work\_dirs/ViTPose\_small\_hi5\_all\_256x192\_500k/epoch\_49.pth  \--img-root /scratch/mhasan9/hi5/data/onehand10k/ \--json-file /scratch/mhasan9/hi5/data/onehand10k/annotations/onehand10k\_test.json \--out-img-root vis\_results\_hi5

