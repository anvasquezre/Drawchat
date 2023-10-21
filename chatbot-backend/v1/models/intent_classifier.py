from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

#loads the model in memory
INTENT_CLASSIFIER = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli", from_pt=True)


def predict(text,labels):
    
    output = INTENT_CLASSIFIER(text,labels, multi_label=False)
    return output