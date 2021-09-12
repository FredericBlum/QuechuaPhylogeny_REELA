## Morphology

from lingpy import *
from lingpy.compare.partial import *
from lingpy.convert.strings import write_nexus
from pyedictor import fetch
from lingpy import Wordlist


with open("crossandean_m.tsv", "w",
        encoding="utf-8") as f:
        f.write(fetch("crossandeanm",
                columns=["ID", "ALIGNMENT", "COGIDS", "CONCEPT",
                "DOCULECT", "FORM", "SPANISH", "TOKENS", "VALUE", 
                "BORROWING", "NOTE", "SOURCE"]
                ))


wl = Wordlist('./crossandean_m.tsv')

borrowings = ['esp']

list_concepts = ["ABLATIVE", "ACCOMPANIMENT", "ACCUSATIVE", "ADDITIVE", "AGENTIVE", 
                "BENEFACTIVE", "CAUSATIVE", "ASSERTIVE", "CISLOCATIVE", "COMPARATIVE", 
                "CONDITIONAL", "CONTINUATIVE", "DATIVE/ILATIVE", "DESIDERATIVE", "DISCONTINUATIVE", 
                "DISTAL DEMONSTRATIVE", "PROGRESSIVE", "EMPHATIC", "EXCLUSIVE", "EVIDENTIAL CONJECTURAL", 
                "EVIDENTIAL DIRECT","EVIDENTIAL REPORTATIVE", "FACTIVE", "FREQUENTIVE", "GENITIVE", 
                "IMPERATIVE", "INCEPTIVE", "INCHOATIVE", "INCLUSIVE", "INFINITIVE", 
                "INJUNCTIVE", "INSTRUMENTAL-COMITATIVE", "JOINT ACTION", "LIMITATIVE", "INTERRUPTED ACTION", 
                "LOCATIVE", "MIDDLE VOICE", "MULTIPLE POSSESSIVE", "NEGATION", "PASSIVE ACCIDENTAL", 
                "PAST TENSE", "PERFECT", "PERFECTIVIZER", "PLURAL", "POSSESSIVE", 
                "PROXIMAL DEMONSTRATIVE", "REASON", "RECIPROCAL", "REPETITIVE", "REPORTATIVE PAST TENSE",
                "RESTRICTIVE", "SEQUENTIAL", "SUBORDINATOR ADVERBIAL", "SUBORDINATOR IDSUB", "SUBORDINATOR DIFFSUB", 
                "TOPIC", "VERBAL BENEFACTIVE", "UNINTERRUPTED ACTION", "INTERROGATION","NOMINALIZER NQA", 
                "NOMINALIZER NA","PRIVATIVE", "DIRECTIONAL INSIDE", "DIRECTIONAL OUTSIDE", "DIRECTIONAL DOWN", 
                "DIRECTIONAL UP","1 OBJECT", "1PL POSSESSOR", "1PL VERBAL", "1PL VERBAL CONDITIONAL", 
                "1PL VERBAL FUTURE", "1S POSSESSOR", "1S VERBAL", "1S VERBAL FUTURE", "2S OBJECT", 
                "2S POSSESSOR", "2S VERBAL", "3S FUTURE", "3S POSSESSOR", "3S VERBAL"]

# This output creates a second wordlist with only the filtered data. 
# There may be a way to directly filter a wordlist, but I wouldn't know how
wl.output('tsv',
                filename = './filtered_m',
                subset = True,
                rows = dict(borrowing = 'not in' + str(borrowings),
                                concept = 'in' + str(list_concepts)))

wl_filtered_m = Wordlist('./filtered_m.tsv')

# This creates the nexus file for Bayesian Inference
nexus_ls = write_nexus(wl_filtered_m,
        ref="cogids", 
        mode="beast", 
        filename='./crossandean_m.nex')

# Distance matrix for NeighborNets
# dst = matrix2dst(wl_filtered.get_distances(ref='cogids', mode='swadesh'), wl_filtered.taxa)
# with io.open('./crossandean_m.dst', 'w', encoding='utf8') as fp:
#    fp.write(dst)
