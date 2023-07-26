from random import choice
from collections import defaultdict
from data_parser.parser import word_parser
from typing import Set, List, Dict

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

zhaoshi_vowel_dict = {}
with open('zhaoshi_vowel_dict.txt', 'r', encoding="utf-8") as f:
    for line in f:
        items = line.strip().split('\t')
        zhaoshi_vowel_dict[tuple(items[0].split())] = items[1].split()

zhaoshi_len_dict = {}
with open('zhaoshi_length_dict.txt', 'r', encoding="utf-8") as f:
    for line in f:
        items = line.strip().split('\t')
        zhaoshi_len_dict[int(items[0])] = items[1].split()
        
entry_word1 = None
entry_word2 = None
entry_word3 = None
entry_word4 = None
result_text = None


def generate_song():
    
    word1 = entry_word1.get() or ''
    word2 = entry_word2.get() or ''
    word3 = entry_word3.get() or ''
    word4 = entry_word4.get() or ''

    line1 = '{}，這{},'.format(word1, ''.join(gen_words_with_pattern(word1, [4, 4, 3])))
    line2 = '{}，我{},'.format(word2, ''.join(gen_words_with_pattern(word1, [4, 4, 3])))
    line3 = '{}，它{},'.format(word3, ''.join(gen_words_with_pattern(word1, [4, 5])))
    line4 = '{}，我自手持{}!'.format(word4, choice(get_zhaoshi_by_vowel(word4)[3]))
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, '\n'.join([line1, line2, line3, line4]))

def gen_words_with_pattern(word, breakdowns):
    z = get_zhaoshi_by_vowel(word)
    return [choice(z[b]) for b in breakdowns]


def get_zhaoshi_by_vowel(target_word):
    num_char = len(target_word)
    pinyins = word_parser(target_word)

    zhaoshi = defaultdict(list)

    target_vowel = pinyins[-1][1][-1]
    for k, v in zhaoshi_vowel_dict.items():
        if k[-1] == target_vowel:
            for word in v:
                word_pys = word_parser(word)
                if word[-1] != target_word[-1] \
                        and word not in zhaoshi[len(word)]:
                    zhaoshi[len(word)].append(word)
    return zhaoshi

def get_zhaoshi_by_len(len):
    return choice(zhaoshi_len_dict[len])

def main():
    global entry_word1, entry_word2, entry_word3, entry_word4, result_text
    
    root = tk.Tk()
    root.title("歌詞生成器")

  
    label_word1 = tk.Label(root, text="第一個關鍵詞:")
    entry_word1 = tk.Entry(root)

    label_word2 = tk.Label(root, text="第二個關鍵詞:")
    entry_word2 = tk.Entry(root)

    label_word3 = tk.Label(root, text="第三個關鍵詞:")
    entry_word3 = tk.Entry(root)

    label_word4 = tk.Label(root, text="一句詩句:")
    entry_word4 = tk.Entry(root)

    generate_button = tk.Button(root, text="生成詩歌", command=generate_song)

    
    result_text = ScrolledText(root, wrap=tk.WORD, width=50, height=10)

    
    label_word1.grid(row=0, column=0, padx=5, pady=5)
    entry_word1.grid(row=0, column=1, padx=5, pady=5)

    label_word2.grid(row=1, column=0, padx=5, pady=5)
    entry_word2.grid(row=1, column=1, padx=5, pady=5)

    label_word3.grid(row=2, column=0, padx=5, pady=5)
    entry_word3.grid(row=2, column=1, padx=5, pady=5)

    label_word4.grid(row=3, column=0, padx=5, pady=5)
    entry_word4.grid(row=3, column=1, padx=5, pady=5)
    
    generate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    result_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()