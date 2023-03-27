diacritics = ["č", "š", "ž", "ć", "ś", "ź", "đ", "Č", "Š", "Ž", "Ć", "Ś", "Ź", "Đ"]

with open("janes_ud_dev_empty.conllu", "r", encoding="utf-8") as rf:
    with open("janes_ud_dev_dediacritized_empty.conllu", "w", encoding="utf-8") as wf:
        for line in rf.readlines():
            if not line.startswith("#") and not line.startswith("\n"):
                split_line = line.split("\t")
                if any(ele in split_line[1] for ele in diacritics):
                    fixed_split_line = split_line[1].replace("č", "c")
                    fixed_split_line = fixed_split_line.replace("š", "s")
                    fixed_split_line = fixed_split_line.replace("ž", "z")
                    fixed_split_line = fixed_split_line.replace("ć", "c")
                    fixed_split_line = fixed_split_line.replace("ś", "s")
                    fixed_split_line = fixed_split_line.replace("ź", "z")
                    fixed_split_line = fixed_split_line.replace("đ", "dj")
                    fixed_split_line = fixed_split_line.replace("Č", "C")
                    fixed_split_line = fixed_split_line.replace("Š", "S")
                    fixed_split_line = fixed_split_line.replace("Ž", "Z")
                    fixed_split_line = fixed_split_line.replace("Ć", "C")
                    fixed_split_line = fixed_split_line.replace("Ś", "S")
                    fixed_split_line = fixed_split_line.replace("Ź", "Z")
                    fixed_split_line = fixed_split_line.replace("Đ", "Dj")

                    split_line[1] = fixed_split_line

                line_to_write = "\t".join(split_line)
            else:
                line_to_write = line
            wf.write(line_to_write)