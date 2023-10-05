# HBS - Herramienta de Búsqueda y Síntesis

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

El propósito de esta herramienta es asistir en los procesos de búsqueda y mapeo sistemático (SMS) de la literatura vigente.

## Estructura de clases


![Repo - Class Diagram](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/JCMiguel/repository-reviewer/main/docs/repo.wsd)

![Engine - Class Diagram](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/JCMiguel/repository-reviewer/main/docs/engine.wsd)

![Historic - Class Diagram](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/JCMiguel/repository-reviewer/main/docs/historic.wsd)


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