from mcparseface import *
REMOVED = ['www', 'http', 'com']


def prepredoc(text):
    lst = text.split()
    new_lst = []
    for x in lst:
        remove=False
        for c in '=:/-@':
            if c in x:
                remove=True
                break

        for w in REMOVED:
            if w in x.lower():
                remove=True
                break

        if not remove:
            new_lst.append(x)
    return ' '.join(new_lst)


if __name__ == '__main__':
    for i in range(2000, 2002):
        for j in range(1, 13):
            raw = json.load(open('enron_{}_{}'.format(i, j)))
            wrangled = [prepredoc(x) for x in raw]
            json.dump(pos_tag(wrangled, verbose=True), open('tagged_{}_{}.json'.format(i,j),'w'))