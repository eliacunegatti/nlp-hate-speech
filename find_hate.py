from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split 
import time
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import transformers
from transformers import AutoModel, BertTokenizerFast
from sklearn.metrics import accuracy_score
import glob
import os
class BERT_Arch(nn.Module):
    
    def __init__(self, bert):
      
      super(BERT_Arch, self).__init__()

      self.bert = bert 
      
      # dropout layer
      self.dropout = nn.Dropout(0.1)
      
      # relu activation function
      self.relu =  nn.ReLU()

      # dense layer 1
      self.fc1 = nn.Linear(768,512)
      
      # dense layer 2 (Output layer)
      self.fc2 = nn.Linear(512,2)

      #softmax activation function
      self.softmax = nn.LogSoftmax(dim=1)

    #define the forward pass
    def forward(self, sent_id, mask):

      #pass the inputs to the model  
      _, cls_hs = self.bert(sent_id, attention_mask=mask,return_dict=False)
      
      x = self.fc1(cls_hs)

      x = self.relu(x)

      x = self.dropout(x)

      # output layer
      x = self.fc2(x)
      
      # apply softmax activation
      x = self.softmax(x)

      return x
bert = AutoModel.from_pretrained('bert-base-uncased')

# Load the BERT tokenizer
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased',return_dict=False)
folder_path = "clean_twitter_data/"
my_list = os.listdir('clean_twitter_data')

for item in my_list:
    if item == ".DS_Store":
        my_list.remove(item)
for filename in my_list:
    folder_name = folder_path + filename +"/"
    print(folder_name)
    for hast in glob.glob(os.path.join(folder_name,'*.csv')):
        try:
          df = pd.read_csv(hast, sep=",",header=None)
          df[0] = df[0].str.replace('[^\w\s]','')

          corpus = []
          for i in range(len(df)):
              text = df[0].iloc[i]
              corpus.append(text)

          # tokenize and encode sequences in the test set
          tokens_test = tokenizer.batch_encode_plus(
              corpus,
              max_length = 25,
              pad_to_max_length=True,
              truncation=True
          )



          test_seq = torch.tensor(tokens_test['input_ids'])
          test_mask = torch.tensor(tokens_test['attention_mask'])




          device = torch.device("cpu")

          print(device)

          path = 'model.pt'
          model = BERT_Arch(bert)

          # push the model to GPU
          model = model.to(device)

          model = torch.load(path,map_location=torch.device('cpu'))


          with torch.no_grad():
            preds = model(test_seq.to(device), test_mask.to(device))
            preds = preds.detach().cpu().numpy()

          preds = np.argmax(preds, axis = 1)

          print(preds)
          c =0

          for item in preds:
            if item == 1:
                c+=1
          tot = float(c / len(df))
          name = os.path.basename(hast)
          name = name.replace(".csv","")

          with open(("results/"+filename+'.csv'), 'a') as filehandle:
            filehandle.write('%s,%d,%f,%d \n' % (name,c,tot,len(preds)))  
        except:
          pass
      

