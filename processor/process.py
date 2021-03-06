import os
import json


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


madlibbed_sentences = []
# Sorted by part of speech tags https://web.archive.org/web/2/https://sites.google.com/site/partofspeechhelp/home#TOC-NNS
word_dictionary = {}

stem_tags = ['NNP', 'PRP', 'NNPS', 'UH', 'PRP$']

replacement_tags = ['NN', 'VBN', 'NNP', 'VB', 'VBD', 'NNS', 'PRP', 'VPB', 'VBG', 'RB', 'VBZ', 'NNPS', 'ADD', 'JJS', 'JJR', 'RBS', 'PRP$']

json_object_counter = 0

# The better way of doing this is to read all the files, then send them to their own thread for processing.
# The problem is that I'm lazy and I don't want to lol.
# This should only need to be run once to generate the two json files.

for filename in os.listdir('sentences'):
    if 'json' in filename:
        print('Loading', filename)
        with open('sentences/' + filename, encoding='utf-8') as f:
            lines = f.readlines()

        print('Processing', filename)
        temp_string = ''
        for line in lines:
            # these aren't proper json files, they have multiple top level blocks, so
            if line is '\n':
                json_object_counter += 1
                test = json.loads(temp_string)
                compressed = test['compression']
                words_by_id = {}
                for n in test['graph']['node']:
                    for w in n['word']:
                        if w['tag'] != 'ROOT':
                            id = w.pop('id')
                            words_by_id[id] = w
                del test

                for key, val in enumerate(compressed['edge']):
                    if 'words' not in compressed:
                        compressed['words'] = {}
                    if val['parent_id'] != -1:
                        compressed['words'][val['parent_id']] = words_by_id[val['parent_id']]
                    compressed['words'][val['child_id']] = words_by_id[val['child_id']]
                compressed.pop('edge')
                del words_by_id

                # Turn it into a list. We only used the dict so we didn't have to deal with repeats
                for i, c in compressed['words'].items():
                    if c['tag'] not in word_dictionary:
                        word_dictionary[c['tag']] = set()

                    # Some tags should use form, some should use stem
                    if c['tag'] in stem_tags:
                        word_dictionary[c['tag']].add(c['stem'])
                        word = c['stem']
                    else:
                        word_dictionary[c['tag']].add(c['form'])
                        word = c['form']

                    if c['tag'] in replacement_tags:
                        compressed['text'] = compressed['text'].replace(word, '[[' + c['tag'] + ']]')

                madlibbed_sentences.append(compressed.pop('text'))
                # Reset temp_string
                temp_string = ''
                if json_object_counter % 500 == 0:
                    print('Processed', json_object_counter, 'objects so far')
            else:
                temp_string += line

if not os.path.exists('processed'):
    os.makedirs('processed')

print('Writing sentences to processed/sentences.json.gz')
with open('processed/sentences.json.gz', 'wb') as f:
    f.write(gzip.compress(bytes(json.dumps(madlibbed_sentences, ensure_ascii=False).encode('utf-8'))))
print('Writing dictionary to processed/dictionary.json.gz')
with open('processed/dictionary.json.gz', 'wb') as f:
    f.write(gzip.compress(bytes(json.dumps(word_dictionary, default=set_default, ensure_ascii=False).encode('utf-8'))))

print('Please load file by using the following blurb')
print('with open("processed/dictionary.json.gz", "rb") as f:')
print('\t values = json.loads(gzip.decompress(f.read()))')
