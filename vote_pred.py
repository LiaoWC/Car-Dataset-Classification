# === Rules ===
# Prefix of file name is "s + number + _": the number is the prediction's weight.
# Prefix "na_" means it doesn't has score record. We give it a weight 60.
# We will read all valid predictions and let them vote for every id's label.
# When one label is voted, it'll get the voter's weight to the power of a constant as the score the voter gives.
# The constant can be set below.

import os
import csv
import datetime

# Constants
#########################################
PREDICTS_FOR_VOTING_PATH = ""
IF_SKIP_FIRST_LINE = True
PRED_WEIGHT_PARAM = 3
#########################################


if PREDICTS_FOR_VOTING_PATH == "":
    print("Error: Please set the path to the prediction voting files.")
    exit()


# Judge if filename valid
# Return -1 if invalid or failed to read; otherwise, return its score (It'll be viewed as weight.)
def valid_pred_filename(filename):
    score_str = filename.split('_')[0]
    if score_str:
        if score_str == 'na':
            return 60
        else:
            score_num = score_str[1:]
            if score_str[0] == 's' and score_num.isdigit() == True:
                return int(score_num)
    return -1


# [[label, score], ...] => [[label, total_score], [nex label, next label's total_score], ...]
def pred_result_scores(pred_list):
    pred_list.sort()
    uniq_pred_list = []
    cur_label = ''
    cur_scores = 0
    for i in range(0, len(pred_list)):
        if cur_label != pred_list[i][0] and cur_label != '':
            uniq_pred_list.append([cur_scores, cur_label])
            cur_scores = 0
        cur_scores += pow(pred_list[i][1], PRED_WEIGHT_PARAM)
        cur_label = pred_list[i][0]
    if cur_scores > 0:
        uniq_pred_list.append([cur_scores, cur_label])
    uniq_pred_list.sort(reverse=True)
    return uniq_pred_list[0][1]


# Read predicts and make it be a dict
predicts = {}
for root, dirs, files in os.walk(PREDICTS_FOR_VOTING_PATH):
    for file in files:
        # only valid prefix file can be counted
        score = valid_pred_filename(file)
        if score > -1:
            print("Reading {} (score: {})".format(file, score))
            id_label_dict = {}
            with open(os.path.join(root, file), 'r') as csvfile:
                reader = csv.reader(csvfile)
                have_skip_first = False if IF_SKIP_FIRST_LINE else True
                for row in reader:
                    #
                    if not have_skip_first:
                        have_skip_first = True
                        continue
                    #
                    [img_id, label] = row
                    id_label_dict[img_id] = label
            predicts[file] = [score, id_label_dict]
            print("+++ Done. Totally got {} rows. +++".format(len(id_label_dict)))

# Take one as the base
base_key = next(iter(predicts))
base_id_label_dict = predicts[base_key][1]
now = datetime.datetime.now()
with open(os.path.join(PREDICTS_FOR_VOTING_PATH, now.strftime("%Y-%d-%H:%M") + "_voted.csv"), 'w+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "label"])
    for img_id in base_id_label_dict:
        score_and_pred_list = []
        for pred_file in predicts:
            [score, id_label_dict] = predicts[pred_file]
            score_and_pred_list.append([id_label_dict[img_id], score])
        writer.writerow([img_id, pred_result_scores(score_and_pred_list)])
print("All done!")
