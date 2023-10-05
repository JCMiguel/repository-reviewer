# HBS - Herramienta de Búsqueda y Síntesis

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

El propósito de esta herramienta es asistir en los procesos de búsqueda y mapeo sistemático (SMS) de la literatura vigente.

## Estructura de clases


![Repo - Class Diagram](https://www.plantuml.com/plantuml/png/dP11IaCn48RtESMif4Lw0N5HSEL2A7W0IPF13YQPnym4gTMx6nArxuaBDRl_6tw-oMpLl5ZDoJd1YU7wTRC1GiHPrC1JLUT2yghG-Sb1Usssy-8p6egsD23Scr1vX2ff2Vn4JtXSigv_EAAN9SSIVw2j_imIrNtgRxYOr63S_1SGKKSwRtFPzrsjlnftQ0UEixasIpYird05LCozVVop7m5ElnVrmaoqg_j40V9ttsqX8v_e1RjppvpEqd7gFsb7vV_YBPPOSte7)

![Engine - Class Diagram](https://www.plantuml.com/plantuml/png/bLHDRzGm4BtdLrZYGiKkFm1nQA5Rj1BVSE0scjYJnC9nLlQu507_dJXEt6JJLhkvHBRVcu_dDxxqZ8v3QugYEA3yYJK9ihMs9FuKGaY3teitwBNSvTtXssx55JjT1YRVByRTPm9aLOFIaiKh4NyJNA1ZBGrvg6n_vDdb4m17XmvaPojTGwKDMMnf1JgWmzO_0hklwcrdsGN9dUjNCxgscW6UUpBLnGp-WRZfrBA5b28u6WhpYTCdAhlEF81AbQrXkJbKy1jRCm0s8bRUKxWPAfyH_XLPyI-1d2PtYkOnnoIAwL2HMbMQfLV8MBcasa6zl9wMvyct4PxGoMRiEztpNDFFeJHQYlPOsXSYQvR4olifu1XTKHdgrCF5KfQzLNHtXYmbUXhC2AewzkF-u_Nk1tpx_kdhrRiTtEpVxvwmqYpkoahdjfqzaezhOj2nDP3erAW2kjf7fBQSWQJqYKX5XfXEmtgyVHevxz7fMsHQDvaySWWC66r6OvIMlCUQijMZm6j2L8FGFin9Mgr9J7TyLXORsfBSYPIe1jffTDAz7Li8Xe7BKpNrF3rDAVRzgDr4p8pS8ii6VcbkeASmkPdoALEC9HjSHjY8eRhXPXQlHpyeyvVwzT_jTlcGh8yN0rKKbsHLQCr_)

![Historic - Class Diagram](https://www.plantuml.com/plantuml/png/dLTVZnCt47_VJs6b3oGYdEZhgLGSS4UH3jgIzgcgB6SzsLWuzjRs0X6bdxtZMMVNCTcx7FToQtl-pFpcDsFdkG_2XMwdgqh39h1WcLFDDZ2f7DH1MLDLhQW_Y0QOWzPwzgLYJAnzSA8EhDR2U_OU3-8-_Jrvmgw2K-ikWCV5OPTrJhDBXdh3ZcZL1zWNcrAHL-7mW1R3oJyTk3rlXHCxNvxLrcnKCt4eOTqrkBcsLhFHkmkgrk2v545iK0zGf9KNhmxBQapefJN1TNMmBi-8SsLKu7pkGM-M14-Ae0zWcS8gDYcS5CqpTYEqXqNcwos4hPKPT8_PkbDQyX4PShWOZZyAhQG8C2s10NZW160Abhu9-SLO09BLLiWxHDzP0uEia99dPKaA64y7f92-UTYtSDf20u7dA2KJHkoImY3fGRXwI-TeXJZdmd1Ae78mOgr1vjcdA8CTwvny11LqxmJBC9ijsHuzPEk1vTbUnQR-scwTqimCT5XAv_CjQTMu74D426eHJaMv4yfmkRbCpBo9Hp7_V3sOWSyHbCB6imZueY2J8_YI3unTgrf4xaHTy5mu9_OZp7ahKCVllYMfCghqVB81C7CAg0owzX-JahUTgw5CUiasIWCHWtX1-lybLYmoGdojleupQwjyi4xLE9tIiFg5TlRtpglNjx--kBhbxwzNVzx-iU8tRswltrszlIx65SSmf-V6AeYWwbDeHUdvniOyOyCfqx1Y94pL-4hAUPyrIiJZ5Ir6F5z3c5FReQcdHzjylUTApfL4JML2Sh42fy2NSWXs03Vl_w6WLZvCnKGwhOEFodP-heo4pxq7Yk0kBoIRDEwFQIT2lKMevlJHLoBI0hJaaHW-nObk__hxjAKRoeTOFfTyu-okDvDOkMHnL1njBPBHCXWoGMFN2TF08HeFBIe-MZugmHefGnNFMgMK90uFV1rBV1zZ3rHzSRMwdkBhcrVynZh4B-q_y8xhYNVKpvDtrpZW7VXE1txetsHBoIESotj8j2qO6Lq59NIqaVHwQtuOJYF57QsdheWWcaCMmI6BE6wCki762SIrCeEZJofi-HQ415SqPy49qevOy0rXc_HnmUMXgAM5yf72uqXsdAVeoodZGtbsrfYXU3BabRpChloSPmcj-pZc8TO-agICKDkc8Q3Y1y9xSKiR3sMOeL4_OInHvGpAHJCHj19E4cYThS7x_gwRkWFZ0o7QQ8L1zT2r6hwvkcgXwqwZD6_1rM2GKSdWABC3rq2wRm_ERDY2MqpKVhhgMGe3oLI07MLxqFk1yTxbfoqOBimU8-QcqphttUjzen8vpQtZbEtzycVBOUHdI2aJxfGwAXkNoXD1OyMIMdp0OTtoacNgwPsHDNgEx8HSwl_Jaf5eBJXbPNenfVeM4PpJg6zsDBfwcl2OkB-Cyu4Q8YTUrh4lBIfrHlA-TTcNx--AwLeDSpILus7Ytvqysfb8FtlSWMcK0JQ-xNxlm2bmryF-n2IBlPMUfl4k1fccSvLIE-UtuSHCE__E9FtVQEoKe3nE3-VEmJ0JYjz0HxyZ1sHwxD6CpTuDrU79E_kHiHcpw7RszE9YbejKupVxwL-KE8AogewMcOdeyCHXyaZnO3G_9r8C0PABWhyL_Zq78xkT_Xy0)


## Configuración

Work in Progress... :)

## Ejemplos de uso

A continuación se muestran ejemplos de uso frecuente.

### Búsqueda sistemática de artículos

#### Búsqueda por título

Si deseamos buscar por título, basta con indicar encerrado entre comillas la cadena que necesitemos y pasarlo al script
mediante el atributo `--title`. A continuación se muestra un ejemplo donde se desea buscar artículos cuyo título
contenga la palabra "xai".

```bash
python .\querier.py --title "xai"
```

#### Búsqueda combinada

Se pueden combinar los atributos de ejecución para realizar una búsqueda más específica.
Supongamos que se desea buscar los artículos que respondan a estos criterios:

```
TITLE = "xai"
AND
ABSTRACT = "xai"
AND
SINCE DATE >= 2015
```

El comando que realizar esta búsqueda resulta:

```bash
python .\querier.py --title "xai" --abstract "xai" --from-year 2015
```

#### Búsqueda por cadena de búsqueda avanzada

Para efectuar esta búsqueda se debe pasar un diccionario como argumento al atributo --query.
Supongamos que se desea realizar esta búsqueda:

```
KEYWORD = ("histology" OR "histopathology")
AND
TITLE = "xai"
```

La línea de comandos necesaria para realizarla debe ser: 

```bash
python .\querier.py --query '{ \"keyword\": [ \"histopalogy\", \"histopathology\" ], \"title\": \"xai\"}'
```

### Fichaje de artículos y revisión

#### Fichar artículo

```bash
python .\indexer.py save
```

#### Listar fichas

```bash
python .\indexer.py get
```

#### Mostrar ficha por índice de fichaje

El siguiente comando muestra la ficha cuyo índice sea 1.

```bash
python .\indexer.py get --index 1
```

#### Listar fichas por nombre de archivo del artículo

```bash
python .\indexer.py get --filename example.pdf
```

Se puede efectuar una búsqueda parcial. La siguiente línea de comando lista todas las fichas que contengan la cadena
"ai" en el campo "Nombre de Archivo"

```bash
python .\indexer.py get --filename ai
```

#### Editar ficha por número de índice

El siguiente comando permite editar la ficha con índice 1.

```bash
python .\indexer.py edit 1
```

#### Borrar ficha por número de índice

El siguiente comando permite eliminar la ficha con índice 1.

```bash
python .\indexer.py delete 1
```

## Licencia

Este trabajo se desarrolla bajo el marco de la licencia
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg