@echo off

@REM cd /d C:/Users/HCI-Beast1/Desktop/hi5_data/Hand-Tracking/
cd /d D:/hi5_data/Hand-Tracking/

python augment_cf.py
python sample_train_test.py
python csv2coco.py

@REM echo Press y to visualize images, or any other key to exit.
@REM set /p input=
@REM if /i %input%==y (
@REM 	python visualize.py
@REM )

@REM @REM Zip the image folders and upload them to Google Drive
@REM 7z a -tzip "G:\My Drive\Hi5\GoogleDrive\test.zip" "D:\hi5_data\data\test"
@REM 7z a -tzip "G:\My Drive\Hi5\GoogleDrive\train.zip" "D:\hi5_data\data\train"

@REM @REM Copy the annotation files to Google Drive
@REM copy "D:\hi5_data\data\person_keypoints_test.json" "G:\My Drive\Hi5\GoogleDrive\person_keypoints_test.json"
@REM copy "D:\hi5_data\data\person_keypoints_train.json" "G:\My Drive\Hi5\GoogleDrive\person_keypoints_train.json"

@REM Zip the image folders locally
@REM 7z a -tzip "D:\hi5_data\data\test.zip" "D:\hi5_data\data\test"
@REM 7z a -tzip "D:\hi5_data\data\train.zip" "D:\hi5_data\data\train"

pause