import conllu


with open("hr500k-test.conllu", "r", encoding="utf-8") as rf:
    with open("hr500k-test_srl.conllu", "w", encoding="utf-8") as wf:
        for sent in conllu.parse_incr(rf):
            for tok in sent:
                if isinstance(tok["misc"], dict) and ("SRL" in tok["misc"].keys()):
                    wf.write(sent.serialize())
                    break
