# predict.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertTokenizer, BertForSequenceClassification
import torch.nn.functional as F

# Load config manually
# from transformers import BertConfig
# config = BertConfig.from_pretrained("toxic_bert_model")

# Load model and tokenizer ONCE (global load)
# Use correct path to local folder
tokenizer = BertTokenizer.from_pretrained("toxic_bert_model")
model = BertForSequenceClassification.from_pretrained("toxic_bert_model")

model.eval()

labels = ['non-toxic', 'toxic']

def predict_comment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)
        pred_label = torch.argmax(probs, dim=1).item()
    return {
        "label": labels[pred_label],
        "probability": round(probs[0][pred_label].item(), 4)
    }
