from os import walk
import os
from datetime import datetime

PRED_RESULT_PATH = '/content/drive/My Drive/CV/hw1/pytorch_90'
TEST_DIR = '/content/drive/My Drive/CV/hw1/Data/testing_data/testing_data'
# switch the model to evaluation mode to make dropout and batch norm work in eval mode
model_B.eval()
# transforms for the input image
loader = transforms.Compose([transforms.Resize((400, 400)),
                             transforms.ToTensor(),
                             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

filenames = []
for root, dirs, files in walk(TEST_DIR):
    for file in files:
        filenames.append(file)
filenames.sort()

now = datetime.now()

with open(PRED_RESULT_PATH + '/' + now.strftime("%H:%M:%S") + '_pytorch90_pred.csv', 'w+') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['id', 'label'])
    havePredicted = 0
    for file in filenames:
        if file.split('.')[-1] != 'jpg':
            continue
        img_path = os.path.join(TEST_DIR, file)
        image = Image.open(img_path)
        image_arr = np.array(image)
        if image_arr.shape != (400, 400, 3):
            print(file)
            image_arr = np.array(image.convert('RGB'))
        print(image_arr.shape)
        image = Image.fromarray(image_arr)
        image = loader(image).float()
        image = torch.autograd.Variable(image, requires_grad=True)
        image = image.unsqueeze(0)
        image = image.cuda()
        output = model_B(image)
        conf, predicted = torch.max(output.data, 1)
        label_name = labeldict.yNum_to_yName_dict[int(classes[predicted.item()])]

        havePredicted += 1

        img_id = file.split('.')[0]

        print('Have predicted {} items, pred label: {} => {}'.format(havePredicted, classes[predicted.item()],
                                                                     label_name))
        writer.writerow([img_id, label_name])
