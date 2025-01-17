import json
import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class LLMIntegrator:
    def __init__(self):
        self.model_name = "distilbert-base-uncased"
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.context = {}

    def integrate_llm(self, context):
        self.context = context
        input_ids, attention_mask = self.prepare_input(context)
        outputs = self.model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predicted_class = torch.argmax(logits)
        return predicted_class

    def prepare_input(self, context):
        input_text = self.tokenizer.encode(context, return_tensors="pt")
        input_ids = input_text["input_ids"]
        attention_mask = input_text["attention_mask"]
        return input_ids, attention_mask

    def train_llm(self, dataset):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-5)
        for epoch in range(5):
            for batch in dataset:
                input_ids, attention_mask, labels = batch
                input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                print(f"Epoch {epoch+1}, Loss: {loss.item()}")

    def save_llm(self):
        torch.save(self.model.state_dict(), "llm_model.pth")

    def load_llm(self):
        self.model.load_state_dict(torch.load("llm_model.pth"))

    def get_context(self):
        return self.context

    def update_context(self, new_context):
        self.context = new_context