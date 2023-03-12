#!/usr/bin/python3
# -*- coding: utf8
print("Importing test_pubmed")


if __name__ == "__main__" :
    print("Script en ejecucion", str(__name__))

# execution:    python example.py --from-year 2016 --debug "multiagent systems"
# params:       {'api_key': 'cc05171a50d4e873982081d58c54a730c207', 'retmax': '25', 'tool': 'repository-reviewer', 'email': 'mlbassi@frba.utn.edu.ar', 'retmode': 'json', 'term': 'multiagent systems', 'mindate': '2016', 'title': None}
# url-query:    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&api_key=cc05171a50d4e873982081d58c54a730c207&retmax=25&tool=repository-reviewer&email=mlbassi%40frba.utn.edu.ar&retmode=json&term=multiagent+systems&mindate=2016

# OBSERBACIONES:
#           --> Traduce correctamente los argumentos del script a los parametros de busqueda del repositorio.
#           --> Inserta los caracteres '+' en lugar de los espacios entre los terminos de la busqueda.
#           --> TODO: Podría definir la variable ans como global y definirla antes de la ejecución para luego inspeccionarla por consola
#           --> TODO: Continuar estudiando en el sitio de E.Utilities como ejecutar la busqueda y obtener los resultados
#                       https://www.ncbi.nlm.nih.gov/books/NBK25498/#chapter3.ESearch__ESummaryEFetch
#                       https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch


# Ejemplo de ejecución
# eSearch   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&tool=repository-reviewer&email=mlbassi%40frba.utn.edu.ar&api_key=cc05171a50d4e873982081d58c54a730c207&term=multiagent+systems&mindate=2022&retmax=2&usehistory=y
# eSummary: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&tool=repository-reviewer&email=mlbassi%40frba.utn.edu.ar&api_key=cc05171a50d4e873982081d58c54a730c207&query_key=1&WebEnv=MCID_640e3a7cf9e9525e78705564&retmax=2&usehistory=y

# {'header': 
#     {
#      'type': 'esearch',
#      'version': '0.3'
#     },
#     'esearchresult': 
#         {'count': '1945',
#          'retmax': '25',
#          'retstart': '0',
#          'idlist': ['36904911',
#                     '36904577',
#                     '36899574',
#                     '36899514',
#                     '36877741',
#                     '36877574',
#                     '36868165',
#                     '36850846',
#                     '36850402',
#                     '36849291',
#                     '36833121',
#                     '36832665',
#                     '36832588',
#                     '36822046',
#                     '36816929',
#                     '36809528',
#                     '36803889',
#                     '36801138',
#                     '36795712',
#                     '36778956',
#                     '36774870',
#                     '36763529',
#                     '36757990',
#                     '36742190',
#                     '36732119'
#                     ],
#         'translationset': [
#                             {'from': 'multiagent',
#                             'to': '"multiagent"[All Fields] OR "multiagents"[All Fields]'},
#                             {'from': 'systems',
#                             'to': '"system"[All Fields] OR "system\'s"[All Fields] OR "systems"[All Fields]'}
#                           ],
#     'querytranslation': '("multiagent"[All Fields] OR "multiagents"[All Fields]) AND ("system"[All Fields] OR "system s"[All Fields] OR "systems"[All Fields])'
#     }
# }
