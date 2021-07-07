import os
import json

important_parts = []
# Sorted by part of speech tags https://sites.google.com/site/partofspeechhelp/home#TOC-Part-of-Speech-Tags
word_dictionary = {}

stem_tags = ['NNP', 'PRP', 'NNPS', 'UH', 'PRP$']

json_object_counter = 0

for filename in os.listdir('sentences'):
    if 'json' in filename:
        with open('sentences/' + filename, encoding='utf-8') as f:
            lines = f.readlines()

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
                        compressed['words'][i] = (c['stem'], c['tag'])
                    else:
                        word_dictionary[c['tag']].add(c['form'])
                        compressed['words'][i] = (c['form'], c['tag'])

                important_parts.append(compressed)
                # Reset temp_string
                temp_string = ''
                if json_object_counter % 500 == 0:
                    print('Processed', json_object_counter, 'lines so far')
            else:
                temp_string += line
