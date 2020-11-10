# Car-Dataset-Classification
> 【CS_T0828_HW1】HW1 for NCTU CS Selected Topics in Visual Recognition using Deep Learning.

Before knowing how to use these codes, let's briefly see what these files do.

## File Introduction
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
