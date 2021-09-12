import os
from lingpy import *
from lingpy.compare.partial import *
from lingpy.convert.strings import write_nexus
from pyedictor import fetch
from lingpy import Wordlist

os.chdir('/home/frederic/Seafile/Arbeiten/Quechua/bbipquechua/Phylo')


with open("crossandean.tsv", "w",
        encoding="utf-8") as f:
        f.write(fetch("crossandean",
                columns=["ID", "ALIGNMENT", "COGIDS", "CONCEPT",
                "DOCULECT", "FORM", 
                "SPANISH", "TOKENS", "VALUE", "BORROWING", "NOTE",
                "SOURCE", "SUBGROUP"]
                ))

wl = Wordlist('crossandean.tsv')                        
                       

# These are the blacklists for the nexus file
blacklist_concepts = ['star', 'green', 'with', 'small']
blacklist_subgroups = ['Aymara', 'Uru-Chipaya']
blacklist_borrowings = ['aymara', 'esp', 'uru']
blacklist_historical = ['CuzquenoAntiguo', 'Anonimo', 'SantoTomas',
                        "Kawki", "Jaqaru", "Huancane", "Puki", "Sullkatiti",
                        "Chipaya", "Iruhito", "Tsimu"]

# This output creates a second wordlist with only the filtered data. 
# There may be a way to directly filter a wordlist, but I wouldn't know how
wl.output('tsv',
                filename = './filtered',
                subset = True,
                rows = dict(doculect = 'not in' + str(blacklist_historical),
                                borrowing = 'not in' + str(blacklist_borrowings),
                                #subgroup = 'not in' + str(blacklist_subgroups),
                                concept = 'not in' + str(blacklist_concepts)))

wl_filtered = Wordlist('./filtered.tsv')

# Word-parameterised nexus
nexus_ls = write_nexus(wl_filtered,
        ref="cogids", 
        mode="beast",
        filename='./crossandean_lex_01_sd.nex')
