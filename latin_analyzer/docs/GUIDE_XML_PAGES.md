# Guide : Analyser des fichiers XML Pages

## C'est quoi un fichier XML PAGE ?

Quand vous transcrivez un manuscrit avec un logiciel d'HTR/OCR (eScriptorium, Transkribus...),
le resultat est sauvegarde au format XML PAGE. Chaque fichier XML correspond a une page du manuscrit.

L'analyseur latin sait lire directement ces fichiers. Il extrait le texte de la zone principale
(appelee `MainZone`) et l'analyse mot par mot.

---

## Utilisation en ligne de commande

C'est la methode la plus simple. Mettez tous vos fichiers XML dans un dossier et lancez :

### Manuscrit a 1 colonne par page

```bash
cd latin_analyzer/src
python3 latin_analyzer_v2.py -i /chemin/vers/dossier_xml/ -o resultat.docx -m xml-single
```

### Manuscrit a 2 colonnes par page

```bash
cd latin_analyzer/src
python3 latin_analyzer_v2.py -i /chemin/vers/dossier_xml/ -o resultat.docx -m xml-dual
```

### Avec rapport des mots non reconnus

```bash
python3 latin_analyzer_v2.py -i /chemin/vers/dossier_xml/ -o resultat.docx -m xml-single --report rapport.txt
```

---

## Ce que le programme extrait

Le programme cherche dans chaque fichier XML les zones de texte marquees `MainZone` :

```xml
<TextRegion custom="structure {type:MainZone;}">
  <TextLine>
    <TextEquiv>
      <Unicode>abbas monachus scriptorium</Unicode>
    </TextEquiv>
  </TextLine>
</TextRegion>
```

En mode `xml-dual`, il cherche les deux colonnes :
- `MainZone:column#1` (colonne gauche)
- `MainZone:column#2` (colonne droite)

---

## Organisation de vos fichiers

### Cas 1 : Manuscrit a 1 colonne (mode single)

```
mon_dossier_xml/
├── page_001.xml    # 1 MainZone par fichier
├── page_002.xml
├── page_003.xml
└── ...
```

Commande :
```bash
python3 latin_analyzer_v2.py -i mon_dossier_xml/ -o resultat.docx -m xml-single
```

### Cas 2 : Manuscrit a 2 colonnes (mode dual)

```
mon_dossier_xml/
├── folio_01.xml    # MainZone:column#1 + MainZone:column#2
├── folio_02.xml
└── ...
```

Commande :
```bash
python3 latin_analyzer_v2.py -i mon_dossier_xml/ -o resultat.docx -m xml-dual
```

---

## Preservation des pages dans le Word

Depuis la version 2.4.0, le fichier Word genere contient des separateurs entre chaque page/folio :

```
──────────────────── Folio: page_001 | Page: 1 ────────────────────
Dominus enim dicit in evangelio quod est ueritas...

──────────────────── Folio: page_002 | Page: 2 ────────────────────
Et ideo beatus augustinus ait in libro...
```

Cela permet de retrouver facilement quelle page du manuscrit contient un mot douteux.

---

## Utilisation en Python

Si vous voulez integrer l'extraction dans votre propre script :

```python
from latin_analyzer.src.latin_analyzer_v2 import LatinAnalyzer

# Creer l'analyseur
analyzer = LatinAnalyzer()

# Analyser un dossier XML (1 colonne)
resultats = analyzer.analyze_page_xml("mon_dossier_xml/", column_mode="single")

# Generer le Word colore
analyzer.generate_docx("resultat.docx", resultats)
```

Pour un manuscrit a 2 colonnes :
```python
resultats = analyzer.analyze_page_xml("mon_dossier_xml/", column_mode="dual")
```

### Extraire le texte sans analyse

Si vous voulez juste extraire le texte brut (sans analyse) :

```bash
cd latin_analyzer/src
python3 export_xml_to_txt.py /chemin/vers/dossier_xml/ sortie.txt single
```

Ou en Python :
```python
from latin_analyzer.src.page_xml_parser import PageXMLParser

parser = PageXMLParser(column_mode="single")
texte, metadata = parser.parse_folder("mon_dossier_xml/")
print(texte)
```

---

## Questions frequentes

### Mes fichiers n'ont pas de MainZone

Verifiez l'attribut `custom` de vos `<TextRegion>` dans le XML.
Si le type est different (par exemple `TextZone` au lieu de `MainZone`),
il faut modifier le code de `page_xml_parser.py` pour chercher le bon type.

### J'ai un mix de pages 1 colonne et 2 colonnes

Separez-les dans deux dossiers et analysez-les separement :
```bash
python3 latin_analyzer_v2.py -i pages_1col/ -o resultat_single.docx -m xml-single
python3 latin_analyzer_v2.py -i pages_2col/ -o resultat_dual.docx -m xml-dual
```

### Comment tester sur une seule page ?

```bash
python3 latin_analyzer_v2.py -i une_seule_page.xml -o test.docx -m xml-single
```

### Ca plante avec "prefix 'xml' not found"

C'est un probleme de namespace dans le XML. Le programme gere normalement ce cas.
Verifiez que votre fichier XML commence bien par :
```xml
<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15">
```

---

## Checklist

Avant de lancer l'analyse, verifiez :

- [ ] Vos fichiers XML contiennent des `TextRegion` avec `MainZone` (ou `MainZone:column#1/2`)
- [ ] Tous les fichiers XML sont dans un seul dossier
- [ ] Vous avez choisi le bon mode (`xml-single` ou `xml-dual`)
- [ ] Le dictionnaire Du Cange est present (`latin_analyzer/data/ducange_data/dictionnaire_ducange.txt`)

---

**Version** : 2.4.0
