from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from sentence_transformers import util


#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


# Sentences we want sentence embeddings for
sentence1 = '''A mouse is a hand-held pointing device used to interact with a computer's graphical user interface (GUI). It typically consists of a small, palm-sized device with one or more buttons and a tracking mechanism, usually a ball or an optical sensor, that detects motion as the user moves the mouse across a flat surface.'''
sentence2 = '''A mouse is a handheld pointing device used to interact with a computer's graphical user interface.'''
sentences = [sentence1,sentence2]
# Load model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Tokenize sentences
encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

# Compute token embeddings
with torch.no_grad():
    model_output = model(**encoded_input)

# Perform pooling
sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

# Normalize embeddings
sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

print("Sentence embeddings:")
# print(sentence_embeddings)
cosine_scores = util.cos_sim(sentence_embeddings[0],sentence_embeddings[1])
print(cosine_scores)
