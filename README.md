# Car-Dataset-Classification
> 【CS_T0828_HW1】HW1 for NCTU CS Selected Topics in Visual Recognition using Deep Learning.

### Outline
- [Introduction](#Introduction) 
- [Methodology](#Methodology)
- [File Introduction](#File-Introduction)
- [How to use the code?](#Procedure) 

## Introduction

We are provided 11185 images as training data, and we have to classify 5000 car images into 196 classes. In this competetion, I have tried Keras and Pytorch frameworks. Finally, I pass the baseline and get 0.92840 score.

## Methodology

### Data Pre-processing

- Split training data into training and validation data.
- Create 196 class directory for training, validation and testing data.
- Make imgaes be square by adding zero-padding. (Optional) I've made two dataset one with zero-padding and the other one doesn't.
- Save all images in their classes' directories.

E.g.  
Before zero-padding:
![](https://i.imgur.com/O1JpC0C.png)

After zero-padding
![](https://i.imgur.com/9nWJdF4.png)


New image structure
![](https://i.imgur.com/gt3OkDX.jpg)

### Model Architecture

I used two frameworks—Pytorch and Keras.

The pytorch verion finally got more than 0.91 score.

As for keras version, although models I used in Keras to train never have test accuary more than 0.82, I still use some of them as voters. Voting by not only strong models but also weak models make the final predicted result has more than 0.92 score, which is better than any single model predicted result.

Model arch. in pytorch:

- Pretrained ResNet34
- 1*FC layer (output layer; 196 units)

In Keras, I have tried the following to produce weak learners.

- Pretrained ResNet50/152/101V2, DenseNet201.
- 1*GlobalAveragePooling2D
- 1~4 dense layers with 2048 or 1024 units, using ReLU as activation function
- Output layer (FC layer with 196 units)

### Hyperparameters

Pytorch version:

- Image (height, width) = (400, 400)
- Batch size: 32
- Epoch number: 10
- Learning rate: 0.01
- Optimizer: SGD with momentum 0.9
- Use learning rate scheduler. (Reduce on plateau.)

Keras version:

- Image (height, width) = (224, 224) but also have tried other pairs.
- Batch size: 32 or 16 mainly.
- Epoch number: 10~100
- Learning rate: have tried 0.01, 0.001, 0.0001, 0.0001 and others.
- Has used Adam and SGD with momentum 0.9 as the optimizer.

P.S.

- I've tried using zero-padding images and non-zero-padding images to train Keras and Pytorch models. Best model I've tried use non-zero-padding images.

### Data augmentation

Pytorch version:

- Horizontal flip
- Rotation

Keras version:

- Rotation
- Horizontal flip
- Shift width/height
- Shear
- Preprocessing functions of pretraied models

### Voting

The voting listens to all weak learners' opinions. Gather strong and weak predictions and make a final predictions.

Each prediction has a voting weight "w". When we predicting a car, if a prediction votes for a label, then the label gets "w to the power of 3" scores. The label with highest scores will be the car's final label.

For example, if there are:

- a prediction file "A" with 80 percent accuary scores
- a prediction file "B" with 60 percent accuary scores
- a prediction file "C" with 60 percent accuary scores

We are deciding the final label of a car with id "XXX", and:

- Prediction file "A" votes for label "2".
- Prediction file "B" votes for label "1".
- Prediction file "C" votes for label "1".

Then, labels obtain scores like the following:

- Label "2" get s80*80*80 = 512000 scores.
- Label "2" gets 60*60*60 + 60*60*60 = 432000 scores.

Label "2" gets highest scores and therefore it's choosed for the final label of the car with id "XXX".

After voting for all testing data, we will get a final prediction csv file.

By doing voting, my final test score is 0.92840, which is better than the strongest learner's prediction.







































## File Introduction
Before knowing how to use these codes, let's briefly see what these files do.
- `resize_to_square.py`: for making images become squares using zero-padding.
- `side_lengths_distribution.py`: used for observing shapes of images.
- `split_train_valid_save.py`: Split into train and valid directories from existed class-directories.
- `vote_pred.py`: Make existed valid predictions vote for labels.
- `train_valid_predict.ipynb`: Modeling, training, predicting , and parts of data preprocessing are here.
- `functions.py`: store functions which are used by above file.

## Procedure

Steps to utilize this repo to predict in this competetion:
1. [Download](#Download)
2. [Image preprocessing](#Image-preprocessing)
3. [Train and predict](#Train-and-predict)
4. [Make submission](#Make-submission)


### Download
Dowload training and testing data:
[https://www.kaggle.com/c/cs-t0828-2020-hw1/data](https://www.kaggle.com/c/cs-t0828-2020-hw1/data)
Clone codes here:
```
git clone https://github.com/LiaoWC/Car-Dataset-Classification
```
You can use google colab or other resources or even use your own GPUs.

### Image preprocessing
1. You can run side_lengths_distribution.py first. It will show you the width and height information of training data.
2. Set and run all the code blocks in `train_valid_predict.ipynb` before `Extra functions`.
3. Run the block `"Classify training data and save them in their class's directories"` in `train_valid_predict.ipynb` (in Extra functions) to make every image of training data to be save in a directory whose name is its class name.
4. Run `split_train_valid_save.py` to split and save training data and validation data. Here you can do twice, for setting `SAVE_AS_SQUARE=True` and the other one setting `SAVE_AS_SQUARE=False`. If `SAVE_AS_SQUARE` is set `True`, the image will be saved as a square image by using zero-padding.
5. Run `resize_to_square.py` and set its path to your testing data directory. It'll help you also transform the testing data into square images. (Help you make your testing data consistent with your training/validation data.)

In these steps, you have to set the constants for your environment(e.g. data path).

### Train and predict

The code about training and predicting in `train_valid_predict.ipynb` are separted into two parts. One uses Keras and the other one uses Pytorch. You can follow the blocks and adjust the parameters to train and predict. The final prediction will be saved as a csv file.

### Make submission

I use voting to decide the final prediction. Details are in the file `vote_pred.py`. Rename your csv prediction file to have prefix "sXX_". "XX" here means a accuracy percentage score. If your give it a prefix "na_", the system will view it as score 60.  I design a power weight which is for weighting the prediction between different prediction. After set the correct path and run `vote_pred.py`, you'll got a finally prediction.

Submit the prediction csv file to competetion page on Kaggle and you'll see your test score.
Everyone can submit no more than six times a day.



## Reference
- https://github.com/h2chen/tensorflow-render
- https://www.kaggle.com/deepbear/pytorch-car-classifier-90-accuracy
- https://towardsdatascience.com/deep-cars-transfer-learning-with-pytorch-3e7541212e85






↓↓↓ training data's height and width distribution ↓↓↓
![](https://i.imgur.com/MkS1ahP.png)
