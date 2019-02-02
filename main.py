from cropper import *
from Classifier import *
import csv

Lable_List = ["Unknown","Mobile","Pant","TShirt"]
#uncomment to create csv for testing data
'''
for i in range(1,4):
    for j in range(5):
        x = Image_Crop("Testing/test"+str(i)+str(j)+".jpg")
        total_list=x.Edge_detection()
        total_list.append(Lable_List[i])
        Item = [total_list]
        print(total_list)
        with open('Testing1.csv', 'a') as f:
            writer = csv.writer(f)
            for row in Item:
                writer.writerow(row)
        f.close()
        '''
#uncomment to generate csv file for training data
'''
for i in range(1,4):
    for j in range(20):
        x = Image_Crop("Training/train"+str(i)+str(j)+".jpg")
        total_list=x.Edge_detection()
        total_list.append(Lable_List[i-1])
        Item = [total_list]
        print(total_list)
        with open('Training1.csv', 'a') as f:
            writer = csv.writer(f)
            for row in Item:
                writer.writerow(row)
        f.close()
        '''
x = Image_Crop("Testing/test12.jpg")
total_list=x.Edge_detection()
total_list.append(Lable_List[0])
with open('unknown.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(total_list)
f.close()
random_tree()
