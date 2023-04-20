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


def partially_dediacritize(sentence):
    diacr_chars = ["č", "š", "ž", "ć", "ś", "ź", "đ", "Č", "Š", "Ž", "Ć", "Ś", "Ź", "Đ"]
    no_diacr_chars = ["c", "s", "z", "c", "s", "z", "dj", "C", "S", "Z", "C", "S", "Z", "Dj"]
    rand = random.random()

    for tok in sentence:
        if any(ele in tok["form"] for ele in diacr_chars) and rand < 0.15:
            for orig, changed in zip(diacr_chars, no_diacr_chars):
                tok["form"] = tok["form"].replace(orig, changed)


def count_diacritics(sentences):
    diacr_chars = ["č", "š", "ž", "ć", "ś", "ź", "đ", "Č", "Š", "Ž", "Ć", "Ś", "Ź", "Đ"]
    tok_count = 0
    for sent in sentences:
        for tok in sent:
            if any(ele in tok["form"] for ele in diacr_chars):
                tok_count += 1

    return tok_count


# read hr500k sents
with open("conllu/hr500k-dev.conllu", "r", encoding="utf-8") as hr500k_file:
    hr500k_sents = conllu.parse(hr500k_file.read())

# read reldi sents
with open("conllu/reldi-normtagner-hr-dev.conllu", "r", encoding="utf-8") as reldi_file:
    reldi_sents = conllu.parse(reldi_file.read())

# prepare list of documents in reldi
reldi_sents_docs = []

# get reldi docs
for sent in reldi_sents:
    if "newdoc id" in sent.metadata.keys():
        doc = []
        doc.append(sent)
        for next_sent in reldi_sents[reldi_sents.index(sent) + 1:]:
            if "newdoc id" in next_sent.metadata.keys():
                break
            doc.append(next_sent)
        reldi_sents_docs.append(doc)

# randomly shuffle the order of the documents in reldi
random.seed(3522)
random.shuffle(reldi_sents_docs)

print("No. of diacritics in reldi: ", count_diacritics(reldi_sents))
print("No. of diacritics in hr500k: ", count_diacritics(hr500k_sents))

# prepare list of sents in combined dataset
combined_sents = []

# write the hr500k sentences into the combined list
for hr500k_sent in hr500k_sents:
    combined_sents.append(hr500k_sent)

# We first add three reldi repetitions with diacritics
reldi_oversampled = []
for i in range(3):
    for doc in reldi_sents_docs:
        for sent in doc:
            reldi_oversampled.append(sent)

# then we add two without diacritics
for i in range(2):
    for doc in reldi_sents_docs:
        for sent in doc:
            modified_sent = copy.deepcopy(sent)
            dediacritize(modified_sent)
            reldi_oversampled.append(modified_sent)

"""# and another with a 15% chance of having diacritics dropped for every token
for doc in reldi_sents_docs:
    for sent in doc:
        modified_sent = copy.deepcopy(sent)
        partially_dediacritize(modified_sent)
        reldi_oversampled.append(modified_sent)"""

# at the end, one half of a repetition to achieve the 1:1 ratio of standard:non-standard data
for i in range(int(len(reldi_sents_docs) * 0.5)):
    for sent in reldi_sents_docs[i]:
        reldi_oversampled.append(sent)

# check the sizes
hr500k_tokens = 0
for sent in hr500k_sents:
    for tok in sent:
        hr500k_tokens += 1

reldi_oversampled_tokens = 0
for sent in reldi_oversampled:
    for tok in sent:
        reldi_oversampled_tokens += 1

print("No. of diacritics in reldi_oversampled: ", count_diacritics(reldi_oversampled))

print("hr500k_sents tokens: ", hr500k_tokens)
print("% of whole: ", hr500k_tokens/(hr500k_tokens+reldi_oversampled_tokens))
print("reldi_oversampled tokens: ", reldi_oversampled_tokens)
print("% of whole: ", reldi_oversampled_tokens/(hr500k_tokens+reldi_oversampled_tokens))

# merge and write to file
for reldi_sent in reldi_oversampled:
    combined_sents.append(reldi_sent)

with open("conllu/hr_combined_dev.conllu", "w", encoding="utf-8") as combined_file:
    for sent in combined_sents:
        combined_file.write(sent.serialize())

