#!/usr/bin/env python

import sqlite3
cn = sqlite3.connect('genera.db')
cr = cn.cursor()
cr.execute("drop table genus")

header = ["Id", "Version", "Family", "Infra_family", "Hybrid_genus",
          "Genus", "Infra_genus", "Hybrid", "Species", "Infra_species",
          "Rank", "Authors", "Basionym_author", "Publishing_author",
          "Full_name_without_family_and_authors", "Publication",
          "Collation", "Publication_year_full", "Name_status",
          "Remarks", "Basionym", "Replaced_synonym",
          "Nomenclatural_synonym", "Distribution", "Citation_type"]

keep_fields = set([0, 2, 4, 5, 12, 13, 15, 16, 17, 18, 20, 21, 22, 24])

header = [name
          for (i, name) in enumerate(header)
          if i in keep_fields]

field_decl = [name + " text" for name in header]
cr.execute("create table genus(%s)" % ", ".join(field_decl))

field_names = ", ".join(header)
placeholders = ", ".join(["?" for i in header])

import codecs

with codecs.open('genera.csv', 'r', 'utf8') as f:
    for l in f.readlines():
        fields = l.strip().split("%")
        fields = [value
                  for (i, value) in enumerate(fields)
                  if i in keep_fields]
        if fields[0] == header[0]:
            continue
        cr.execute("insert into genus (%s) values (%s)"
                   % (field_names, placeholders), fields)

cn.commit()
