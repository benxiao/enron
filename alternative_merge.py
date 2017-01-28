NOUN_TYPES = ('NN','NNS','NNP','NNPS')


def merge_words(sent_components):
    result = []
    phrase = []
    for (w, t) in sent_components:
        if t in NOUN_TYPES:
            phrase.append((w, t))

        elif w == 'of' and phrase and all([t in NOUN_TYPES for (_, t) in phrase]):
            phrase.append((w, t))

        elif not phrase and t == 'JJ':
            phrase.append((w, t))

        elif len(phrase) == 1 and phrase[-1][1] == 'JJ' and t == 'JJ':
            phrase.clear()
            phrase.append((w, t))

        elif phrase and t not in NOUN_TYPES:
            if phrase[-1][1] not in NOUN_TYPES:
                result.extend(phrase)
            else:
                result.append(('_'.join(w for (w, _) in phrase), 'NN'))
            phrase.clear()
            result.append((w, t))

        else:
            result.append((w, t))

    if phrase and phrase[-1][1] in NOUN_TYPES:
        result.append(('_'.join(w for w, _ in phrase), 'NN'))
    else:
        result.extend(phrase)

    return result