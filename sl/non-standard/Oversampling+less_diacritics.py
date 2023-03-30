import conllu
import random
import copy


def dediacritize(sentence):
    diacr_chars = ["č", "š", "ž", "ć", "ś", "ź", "đ", "Č", "Š", "Ž", "Ć", "Ś", "Ź", "Đ"]
    no_diacr_chars = ["c", "s", "z", "c", "s", "z", "dj", "C", "S", "Z", "C", "S", "Z", "Dj"]

    for tok in sentence:
        if any(ele in tok["form"] for ele in diacr_chars):
            for orig, changed in zip(diacr_chars, no_diacr_chars):
                tok["form"] = tok["form"].replace(orig, changed)


def half_dediacritize(sentence):
    diacr_chars = ["č", "š", "ž", "ć", "ś", "ź", "đ", "Č", "Š", "Ž", "Ć", "Ś", "Ź", "Đ"]
    no_diacr_chars = ["c", "s", "z", "c", "s", "z", "dj", "C", "S", "Z", "C", "S", "Z", "Dj"]
    rand = random.random()

    for tok in sentence:
        if any(ele in tok["form"] for ele in diacr_chars) and rand > 0.5:
            for orig, changed in zip(diacr_chars, no_diacr_chars):
                tok["form"] = tok["form"].replace(orig, changed)

def count_diacritics(sentences):
    diacr_chars = ["č", "š", "ž", "ć", "ś", "ź", "đ", "Č", "Š", "Ž", "Ć", "Ś", "Ź", "Đ"]
    tok_count = 0
    for sent in sentences:
        for tok in sent:
            if any(ele in tok["form"] for ele in diacr_chars):
                tok_count += 1

    print("No. of diacritics in janes_oversampled: ", tok_count)


# read suk sents
with open("conllu/train/SUK_ud_train.conllu", "r", encoding="utf-8") as suk_file:
    suk_sents = conllu.parse(suk_file.read())

# read janes sents
with open("conllu/train/janes_ud_train.conllu", "r", encoding="utf-8") as janes_file:
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

# to dediacritize, we first add two janes repetitions with diacritics
janes_oversampled = []
for i in range(2):
    for doc in janes_sents_docs:
        for sent in doc:
            janes_oversampled.append(sent)

# then we add one without diacritics
for doc in janes_sents_docs:
    for sent in doc:
        modified_sent = copy.deepcopy(sent)
        dediacritize(modified_sent)
        janes_oversampled.append(modified_sent)

# and another with a 50% chance of having diacritics dropped for every token
for doc in janes_sents_docs:
    for sent in doc:
        modified_sent = copy.deepcopy(sent)
        half_dediacritize(modified_sent)
        janes_oversampled.append(modified_sent)

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

#count_diacritics(janes_oversampled)

print("suk_sents tokens: ", suk_tokens)
print("% of whole: ", suk_tokens/(suk_tokens+janes_oversampled_tokens))
print("janes_oversampled tokens: ", janes_oversampled_tokens)
print("% of whole: ", janes_oversampled_tokens/(suk_tokens+janes_oversampled_tokens))

# merge and write to file
for janes_sent in janes_oversampled:
    combined_sents.append(janes_sent)

with open("conllu/train/combined+dediacritized_ud_train.conllu", "w", encoding="utf-8") as combined_file:
    for sent in combined_sents:
        combined_file.write(sent.serialize())

