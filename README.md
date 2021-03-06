# NENA Corpus Pipeline

Pipeline for processing NENA markup format texts

# Requirements

Minimum Python requirements are Python 3.8. Package dependencies are stored in [requirements.txt](requirements.txt).

# How to use

For example usage of the pipeline see [example.ipynb](example.ipynb).

The pipeline outputs the following to the specified outdir (see example notebook above):

    1) `tf` directory containing the indexed corpus in 
        text-fabric format
    2) documentation.md: a file containing documentation
        on the makeup of the corpus
    3) search_tool: set of static files which are the 
        nena_search compiled from the corpus data

# Nena Markup Format

NENA texts are transcribed stories or dialogues derived from audio recordings in 
the field. These transcriptions have traditionally taken the form of publications 
or files stored on a personal computer. In the NENA text-corpus project we normalize 
these various formats into a simple plain-text version. This version is intended 
to be both human- and machine-readable and include annotations. Markup languages 
like [Markdown](https://daringfireball.net/projects/markdown/syntax) are examples
of hybrid formats which are easy for people to use and can be read by machines 
with some basic parsing. 

The NENA Markup Format is a simple plain-text format for inputting and annotating
NENA transcriptions. The format outlined below is inspired both by Markdown and, 
more distantly, by the Eep Talstra Centre for Bible and Computer's 
[PIL text format](https://github.com/ETCBC/data_creation/blob/master/documentation/pil_format.pdf)
used for Aramaic and Hebrew corpora.

**Contents**

* [Example of NENA Markup](#Example-of-NENA-Markup-Text)
* [Structure](#Structure)
  * [Metadata Block](#Metadata-block)
  * [Text Block](#text-block)
    * [Canonical Letters](#Canonical-letters)
    * [Foreign Letters](#Foreign-letters)
    * [Paragraph Structure](#Paragraph-structure)
    * [Punctuation](#Punctuation)
    * [Span Tag](#Span-Tag)
    * [Foreign Language Tag](#Foreign-Language-Tag)

## Example of NENA Markup Text

Below is an example of a text annotated with NENA Markup. The markup is mainly 
hypothetical for illustrative purposes and contains all possible markup patterns.

```
dialect:: urmi_c
title:: When Shall I Die?
encoding:: UTF-8
speakers:: YD=Yulia Davudi, GK=Geoffrey Khan
place:: +Hassar +Baba-??an??a, N
text_id:: A32 
corpus_id:: 42

(1 0:00) x??-yuma ???malla ???Nasr??d??n v??y??l?? t??va ?????al-k????sa.?? x?? m??n-n?????? 
???v??r??va,?? m????rr?? ???m??lla?? ????t??n ??o-k????sa pr??mut,?? b??t-n??pl??t.?? m????rr?? <P:b????ro> 
b??ba?? ????t??n=da?? ???????la l????tlux?? t??yy??t b-d??yyi k????t??t.?? ???????k?? si-???bar-???????lux.?? 
????na ???????l-????nil??.?? n??pl??n n??pl??n.?? (2 0:08) ???h??la?? ??o-n????a l??va x????a x?? 
???????sr?? ???pasuly??y,?? ???m??lla bit??y??l?? dr??m ?????al-???????rra.?? b??k??y??m??l?? ???b??rx???????l?? 
???b??ru.?? m??ra?? ???maxl??ta,?? ????t??n ???d??lux ????na b??t-n??pl??nva m-???al-??il??na.?? 
bas-t??nili x??z??n ????na ????man b??t-m??t??n.?? ??o-n????a xz??l?? k??at-???? ???m??lla?? h??nu 
x??????????a ... ???bas??r??l???? m????rr?? k????tu?? ???maxl??ta,?? m????dr??,?? ??GK:maxl??ta??? ???r??ba 
???maxl??ta.?? m????rr?? k??at-????man xm??rtux ??????l?? ????h?? ?????ar?????la,?? ????-yuma m??t??t.?? 
????-yum??t xm??rtux ??????l?? ????h?? ?????ar?????la,?? ????-yuma m??t??t.?? 

(3 0:16 GK) <E:Ok>  (YD) ???m??lla m??tt??va ... ????????na?? ???yak????yra ?????al-xm??rta.?? ????????na?? m????ndi 
???r??ba m??tt??va ?????al-xm??rta?? ??u-xm??rta?? ???b??yyava ??ask????va ???????llul.??
??u-bas-p??xa ???pl???????l?? m??nn??.?? ???????r,?? ???ri?????la.?? ???m??lla m????rr?? ????ha,?? ????na d????n
k??arb??n?? k??a-my??ta.?? (4 0:20) x??????????a=da s????k??la?? xa-x??ta.?? ????nu mudm??xx??l??
?????al-???????rra.?? m????rr???? x??na ???d????n m??tila.?? ????=t-d-??????l???? ???m??lla m????tl??.?? n??????,??
 xuyrav??tu?? x??????lun t??lun m????rrun?? ??a m??-vad??t? k??a-m??=iv??t ???t??mma??? m????rr?? 
 xob-????na m??t??n.?? l?? b??xz??y??tun k??at-m??t??n!?? l?? m????rrun ??at-x??ya!?? 
 hamz??m??v??t.?? b????v??k??una ???t??ma?? m??ra?? xm??r??l??,?? l??l?? ???p??arm??y??.??
```

# Structure

NENA Markup texts consist of two blocks: 1) metadata block, 2) text block.

## Metadata Block

The metadata block contains metadata features and values. Each unique feature
and value is contained on its own line and separated from other feature/values 
by a single line break. 

A single feature/value pair is separated with double colons, to distinguish it
from the allowable single colon in the text block. Trailing / leading spaces 
will be stripped.

```
feature:: value
```

The metadata block is ended by two adjacent newline characters.

Obligatory features are: 

* `dialect` - this the dialect code rather than its pretty name; see [configs](pipeline/configs/dialects.json) for known codes
* `corpus_id` - this is the unique database id associated with this text
* `title` - a unique title for this text
* `speakers` - the speakers in the text, which are identified with an abbreviation (first/last) followed by a = assignment; multiple speakers are comma separated. See example text above for example.

Other valuable features include data about the interviewer, place, 
or transcriber. 

## Text Block

The text block contains the body of the transcribed text. The text must be 
written using valid canonical letters or acceptable foreign character combinations
and valid punctuation characters.

### Canonical Letters

Canonical letters are all valid character combinations in the entire NENA corpus, regardless of the dialect.
These are defined in the config file [alphabet.json](pipeline/configs/alphabet.json).
We draw a distinction between "characters" and "letters". A "character" is a 
technical term for a unique unicode codepoint with very many combination
possibilities (e.g. diacritics). A "letter" is a semantic entity that links
a given combination of characters with a single phonological value. NENA canonical 
letters are thus a select subset of all possible character combinations. With 
the exception of foreign words, only this subset is allowed in the text portions 
of a text block. 

#### Normalize to Decomposed 
We define letters strictly in terms of decomposed character sets in order to correctly match and validate
character combinations. All NENA markup texts are normalized with `unicodedata.normalize('NFD', string)`
to ensure only decomposed character combos are evaluated. 

### Foreign Letters

Letters in words [marked as foreign](#Foreign-Language-Tag) are considered
non-canonical and need only match the regular expression pattern defined in
[markup_tags.json](pipeline/configs/markup_tags.json) under "foreign_letter".
An example of a foreign letter is the `u` with umlaut in German words.

### Paragraph Structure

Paragraphs are units of text with some kind of thematic cohesion. Paragraphs 
are delineated by a single blank line (two newline characters). For example:

```
This is
one paragraph.

This is another paragraph.
```

Paragraphs are currently recognized by the parser but do not yet play any important
role in the corpus.

### Punctuation

Punctuation must conform to the begin / end punctuations in [punct_begin.json](pipeline/configs/punct_begin.json)
and [punct_end.json](pipeline/configs/punct_end.json). Beginning punctuations
are typically inflectional markup. A dialectical example of this is the `+` found at the 
beginning of words in Christian Urmi. A more common example would be opening quotation marks,
which are distinguished from closing with a lack of trailing space. By contrast "+whitespace is
considered an ending punctuation. Additional beginning punctuations can be added in the configs. 

Ending punctuations include white spaces, full stops, commas, semi-colons and more. 
These items are associated with the ends of words and are usedto delineate words.


### Span Tags

A span is simply a stretch of text with associated metadata. The metadata
indicated by a span remains "active" for all words which follow it until
a given metadata value is updated by a subsequent span. 

Span tags are defined as open and closed parentheses with space-separated metadata. The metadata
may occur in any order since the parser evaluates these individually after splitting on spaces.

The metadata allowed in a span tag is defined as one of the following:

* line numbers - verse-like reference numbers, from publications if applicable, or made new if not
* time stamp - indicates time position of spoken text in an audio file, indicated by at minimum 2 numbers separated with a colon: 0:05
* speaker - initials of a speaker which consists of 1+ capital letters (`[A-Z]`); only latin letters should be used; the initials must be defined in the metadata of the document under "speakers", which assigns each initial to a full name. E.g. `GK=Geoffrey Khan`

Span tags contain a minimum of 1 metadata element and a maximum of 3. The same kind of metadata element should not 
be used more than once for a single tag as this is considered non-sensical (i.e. only 1 speaker per span, only 1 timestamp, only 1 line number).

Some examples of span tags in practise:

```
(2 0:05 GK)
```

Which means: Geoffrey Khan is speaking at 5 seconds in the 
audio within (publication) line number 2

or 

```
(1 0:00) Here is some text (GK) But here is some more.
```
Which means: someone was speaking within a span of text beginning at
0 seconds in publication line 1; Geoffrey Khan then began speaking at 
some point in the middle of that span.

### Foreign Language Tag

NENA texts occasionally contain words or stretches of words spoken in a language
foreign to NENA. These words should be indicated with an opening single angle 
bracket (<), a [valid language code](pipeline/configs/foreign_languages.json), a colon, 
the foreign words, and a single closing bracket:

```
This is some NENA. <Du:Dit is niet NENA>
```

Any number of words are allowed in a foreign language tag, but the tag should
not take up a substantial portion of the NENA text.
