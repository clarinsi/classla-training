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


# read hr sents
with open("../hr500k-dev.conllu", "r", encoding="utf-8") as hr_file:
    hr_sents = conllu.parse(hr_file.read())

# read sr sents
with open("../sr_set-ud-dev.conllu", "r", encoding="utf-8") as sr_file:
    sr_sents = conllu.parse(sr_file.read())

# prepare list of documents in hr
hr_sents_docs = []

# get hr docs
for sent in hr_sents:
    if "newdoc id" in sent.metadata.keys() and not sent.metadata["sent_id"].startswith("set"):
        doc = []
        doc.append(sent)
        for next_sent in hr_sents[hr_sents.index(sent) + 1:]:
            if "newdoc id" in next_sent.metadata.keys():
                break
            doc.append(next_sent)
        hr_sents_docs.append(doc)

# randomly shuffle the order of the documents in hr
random.seed(341)
random.shuffle(hr_sents_docs)

# prepare list of sents in combined standard training dataset
combined_standard_sents = []

# write the sr sentences into the combined list
for sr_sent in sr_sents:
    combined_standard_sents.append(sr_sent)

# we need to have exactly 0.22 times the number of hr sentences in the combined dataset
hr_undersampled = []
for i in range(int(len(hr_sents_docs) * 0.22)):
    for sent in hr_sents_docs[i]:
        hr_undersampled.append(sent)

# check the sizes
sr_tokens = 0
for sent in sr_sents:
    for tok in sent:
        sr_tokens += 1

hr_undersampled_tokens = 0
for sent in hr_undersampled:
    for tok in sent:
        hr_undersampled_tokens += 1


print("sr_sents tokens: ", sr_tokens)
print("% of whole: ", sr_tokens/(sr_tokens+hr_undersampled_tokens))
print("hr_undersampled tokens: ", hr_undersampled_tokens)
print("% of whole: ", hr_undersampled_tokens/(sr_tokens+hr_undersampled_tokens))

# merge
for hr_sent in hr_undersampled:
    combined_standard_sents.append(hr_sent)

# open non-standard train file
with open("../reldi-normtagner-sr-train.conllu", "r", encoding="utf-8") as nonst_file:
    nonst_sents = conllu.parse(nonst_file.read())

# get non-standard docs
nonst_sents_docs = []
for sent in nonst_sents:
    if "newdoc id" in sent.metadata.keys():
        doc = []
        doc.append(sent)
        for next_sent in nonst_sents[nonst_sents.index(sent) + 1:]:
            if "newdoc id" in next_sent.metadata.keys():
                break
            doc.append(next_sent)
        nonst_sents_docs.append(doc)

# prepare final combined list
combined_sents = []
nonst_oversampled = []

# write the standard sents to the list
for st_sent in combined_standard_sents:
    combined_sents.append(st_sent)

# first we add one repetition with diacritics
for doc in nonst_sents_docs:
    for sent in doc:
        nonst_oversampled.append(sent)

# next, one without diacritics
for doc in nonst_sents_docs:
    for sent in doc:
        modified_sent = copy.deepcopy(sent)
        dediacritize(modified_sent)
        nonst_oversampled.append(modified_sent)

# check the sizes
standard_tokens = 0
for sent in combined_standard_sents:
    for tok in sent:
        standard_tokens += 1

nonst_oversampled_tokens = 0
for sent in nonst_oversampled:
    for tok in sent:
        nonst_oversampled_tokens += 1

print("standard tokens: ", standard_tokens)
print("% of whole: ", standard_tokens/(standard_tokens+nonst_oversampled_tokens))
print("nonstandard oversampled tokens: ", nonst_oversampled_tokens)
print("% of whole: ", nonst_oversampled_tokens/(standard_tokens+nonst_oversampled_tokens))

# write the non-standard sents to the final list
for sent in nonst_oversampled:
    combined_sents.append(sent)

with open("sr-nonst_tagger_dev.conllu", "w", encoding="utf-8") as write_file:
    for sent in combined_sents:
        write_file.write(sent.serialize())

