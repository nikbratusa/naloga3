import numpy as np
import glob
import os.path
from transliterate import translit
from collections import Counter
import math

#funkcija za ustvarjanje trojk iz prejšnje naloge
def kmers(s, k=3):
    for i in range(len(s) - k + 1):
        yield s[i:i + k]
    return s

#funckija ki vrne v koliko dokumentih je trojka
def pojavitevTrojke(trojka, t):
    count = 0
    for k in t.keys():
        for i in t[k]:
            if i == trojka:
                count += 1;
                break
    return count

def prepare_data_matrix():
    """
    Return data in a matrix (2D numpy array), where each row contains triplets
    for a language. Columns should be the 100 most common triplets
    according to the idf measure.
    """
    # create matrix X and list of languages
    # ...

    data = {}

    #ponovimo postopek iz 2. naloge, ker pridobimo deklaracije iz 20 izbranih jezikov ter te deklaracije filtriramo.
    for file_name in glob.glob("izbraniJeziki/*"):
        name = os.path.splitext(os.path.basename(file_name))[0]
        text = " ".join([line.strip() for line in open(file_name, "rt", encoding="utf8").readlines()])
        text = text.lower()
        data[name] = text

    # ker sta grški in ruski jezik v različnih pisavah, moramo ta dva spremeniti v latinico, kar storimo s pomočjo transliterate
    data['grk'] = translit(data['grk'], 'el', reversed=True)
    data['rus'] = translit(data['rus'], 'ru', reversed=True)

    # sprav se sprehodim cez vse deklaracije in si shranim vse znake, ki niso črke
    removeChars = []

    for text in data.values():
        for c in text:
            if not c.isalpha() and c not in removeChars:
                removeChars.append(c)

    # iz tega lista odstranim presledek, saj jih bom ohranil,
    removeChars.remove(" ")
    k = list(data.keys())
    count = 0

    for text2 in data.values():
        for r in removeChars:
            text2 = text2.replace(r, "")
            # tukaj odstrani vse presledke, ki jih je več kot eden in znake za novo vrstico
            text2 = " ".join(text2.split())
        data[k[count]] = text2
        count += 1

    languages = list(data.keys())
    #ko imamo deklaracije prebrane in filtrirane v spremenljivki data, ustvarimo trojke

    #ustvarimo frekvence trojk v posameznem besedilo in samo katere trojke so v posameznem besedilu
    trojkeFrekvence = {k: Counter(kmers(data[k], 3)) for k in data.keys()}
    trojkeJeziki = {k: set(kmers(data[k], 3)) for k in data.keys()}


    print(trojkeFrekvence["rus"])
    print(trojkeFrekvence["rus"].keys())
    print(trojkeFrekvence["rus"]["ja "])


    #sprehodimo se cez vse trojke v vseh jezikih in ustvarimo list vseh trojk, ki obstajajo brez ponavljanja
    trojkeList = []

    for k in trojkeJeziki.keys():
        for t in trojkeJeziki[k]:
            if t not in trojkeList:
                trojkeList.append(t)

    #ta list dodamo kot ključe slovarja in vsaki trojki dodamo vrednost 0, ki jo bom potem nadomestila vrednost idf
    trojkeSlovar = {t: 0 for t in trojkeList}

    #nato se sprehodimo cez vse trojke in za vsako izračunamo idf ter shranimo pod vrednost ključa(trojke) slovarja
    for t in trojkeSlovar.keys():
        pojavitve = pojavitevTrojke(t,trojkeJeziki)
        #print ("trojka %s se pojavi %d" % (t,pojavitve))
        idf = math.log(20/pojavitve)
        trojkeSlovar[t] = idf

    #potem uredimo slovar po vrednosti od najnižjih do največjih in vzamemo samo prvih 100 vrednosti, ki imajo najmanjši idf kar pomeni, da so to najpogostejše trojke
    trojkeSorted = sorted(trojkeSlovar.items(), key=lambda x: x[1])[:100]
    print(trojkeSorted)

    #ustvarimo se list kjer so sedaj samo trojke, saj idf ni vec pomemben. S tem listom bomo preverili koliko se pojavljajo v posameznem jeziku
    trojkeSortedList = []
    count = 0;

    for i in trojkeSorted:
        trojkeSortedList.append(trojkeSorted[count][0])
        count += 1

    print(trojkeSortedList)
    #ustvarimo prazno matriko
    X = np.empty((0,100), int)
    print(X)


    for l in languages:
        listDrzava = []
        for t in trojkeSortedList:
            if t in trojkeFrekvence[l].keys():
                listDrzava.append(trojkeFrekvence[l][t])
            else:
                listDrzava.append(0)
        X = np.append(X, np.array([listDrzava]), axis=0)

    print(X.shape)
    print(X)

    return X, languages


def power_iteration(X):
    """
    Compute the eigenvector with the greatest eigenvalue
    of the covariance matrix of X (a numpy array).


    Return two values:
    - the eigenvector (1D numpy array) and
    - the corresponding eigenvalue (a float)
    """
    pass


def power_iteration_two_components(X):
    """
    Compute first two eigenvectors and eigenvalues with the power iteration method.
    This function should use the power_iteration function internally.

    Return two values:
    - the two eigenvectors (2D numpy array, each eigenvector in a row) and
    - the corresponding eigenvalues (a 1D numpy array)
    """
    pass


def project_to_eigenvectors(X, vecs):
    """
    Project matrix X onto the space defined by eigenvectors.
    The output array should have as many rows as X and as many columns as there
    are vectors.
    """
    pass


def total_variance(X):
    """
    Total variance of the data matrix X. You will need to use for
    to compute the explained variance ratio.
    """
    return np.var(X, axis=0, ddof=1).sum()


def explained_variance_ratio(X, eigenvectors, eigenvalues):
    """
    Compute explained variance ratio.
    """
    pass


if __name__ == "__main__":

    # prepare the data matrix
    X, languages = prepare_data_matrix()

    # PCA
    # ...

    # plotting
    # ...
