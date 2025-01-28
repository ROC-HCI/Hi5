This repository has all the code required to take the dataset and csv data from Unity and break them down into train, test, valid groups. It does all data augmentation and turns data into COCO format.
The code in the repository prepares the data for training stage.
Update: It automatically packages the data and uploads it to google drive so that it can be accessed by the linux computer that use to train the model.


Pipeline uses the scripts in the order of (through data_process.bat):
augment_cf -> Does all data augmentation (imports augment_types) (augment in helper folder can be useful with debugging).
sample_train_test -> Takes all data and breaks them down into train, test, valid.
csv2coco -> Converts csv into coco format. Dataset is readt for training after this.

Optional:
visualize - For visualisation (might need to run multiples times of the process).
init.bat - Cleans the folder where all data is stored locally.