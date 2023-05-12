import conllu
import random

# read hr sents
with open("/home/luka/Documents/Programming/PycharmProject/git/classla-training/hr/standard/conllu/hr500k-train.conllu", "r", encoding="utf-8") as hr_file:
    hr_sents = conllu.parse(hr_file.read())

# read sr sents
with open("sr_set-ud-train.conllu", "r", encoding="utf-8") as sr_file:
    sr_sents = conllu.parse(sr_file.read())

# prepare list of documents in sr
sr_sents_docs = []

# get sr docs
for sent in sr_sents:
    if "newdoc id" in sent.metadata.keys():
        doc = []
        doc.append(sent)
        for next_sent in sr_sents[sr_sents.index(sent) + 1:]:
            if "newdoc id" in next_sent.metadata.keys():
                break
            doc.append(next_sent)
        sr_sents_docs.append(doc)

# randomly shuffle the order of the documents in sr
random.seed(51155)
random.shuffle(sr_sents_docs)

# prepare list of sents in combined training dataset
combined_sents = []

# write the hr sentences into the combined list
for hr_sent in hr_sents:
    combined_sents.append(hr_sent)

# we need to have exactly 5.4 times the number of sr sentences in the combined dataset
# this is achieved by first writing the sr sentences five times into the combined list, then writing an additional
# 0.4 times the number of sr sentences
sr_oversampled = []
for i in range(5):
    for doc in sr_sents_docs:
        for sent in doc:
            sr_oversampled.append(sent)

for i in range(int(len(sr_sents_docs) * 0.4)):
    for sent in sr_sents_docs[i]:
        sr_oversampled.append(sent)

# check the sizes
hr_tokens = 0
for sent in hr_sents:
    for tok in sent:
        hr_tokens += 1

sr_oversampled_tokens = 0
for sent in sr_oversampled:
    for tok in sent:
        sr_oversampled_tokens += 1


print("hr_sents tokens: ", hr_tokens)
print("% of whole: ", hr_tokens/(hr_tokens+sr_oversampled_tokens))
print("sr_oversampled tokens: ", sr_oversampled_tokens)
print("% of whole: ", sr_oversampled_tokens/(hr_tokens+sr_oversampled_tokens))

# merge and write to file
for sr_sent in sr_oversampled:
    combined_sents.append(sr_sent)

with open("pos/sr_standard_train.conllu", "w", encoding="utf-8") as combined_file:
    for sent in combined_sents:
        combined_file.write(sent.serialize())

