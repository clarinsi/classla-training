import conllu
import random

# read suk sents
with open("conllu/dev/SUK_ud_dev.conllu", "r", encoding="utf-8") as suk_file:
    suk_sents = conllu.parse(suk_file.read())

# read janes sents
with open("conllu/dev/janes_ud_dev.conllu", "r", encoding="utf-8") as janes_file:
    janes_sents = conllu.parse(janes_file.read())

# prepare list of documents in janes
janes_sents_docs = []

# get janes docs
for sent in janes_sents:
    if "newdoc id" in sent.metadata.keys():
        doc = []
        doc.append(sent)
        for next_sent in janes_sents[janes_sents.index(sent) + 1:]:
            if "newdoc id" in next_sent.metadata.keys():
                break
            doc.append(next_sent)
        janes_sents_docs.append(doc)

# randomly shuffle the order of the documents in janes
random.seed(4802)
random.shuffle(janes_sents_docs)

# prepare list of sents in combined training dataset
combined_sents = []

# write the suk sentences into the combined list
for suk_sent in suk_sents:
    combined_sents.append(suk_sent)

# we need to have exactly 4.7 times the number of janes sentences in the combined dataset
# this is achieved by first writing the janes sentences four times into the combined list, then writing an additional
# 0.7 times the number of janes sentences
janes_oversampled = []
for i in range(4):
    for doc in janes_sents_docs:
        for sent in doc:
            janes_oversampled.append(sent)

for i in range(int(len(janes_sents_docs) * 0.7)):
    for sent in janes_sents_docs[i]:
        janes_oversampled.append(sent)

# check the sizes
suk_tokens = 0
for sent in suk_sents:
    for tok in sent:
        suk_tokens += 1

janes_oversampled_tokens = 0
for sent in janes_oversampled:
    for tok in sent:
        janes_oversampled_tokens += 1


print("suk_sents tokens: ", suk_tokens)
print("% of whole: ", suk_tokens/(suk_tokens+janes_oversampled_tokens))
print("janes_oversampled tokens: ", janes_oversampled_tokens)
print("% of whole: ", janes_oversampled_tokens/(suk_tokens+janes_oversampled_tokens))

# merge and write to file
for janes_sent in janes_oversampled:
    combined_sents.append(janes_sent)

with open("conllu/dev/combined_ud_dev.conllu", "w", encoding="utf-8") as combined_file:
    for sent in combined_sents:
        combined_file.write(sent.serialize())

