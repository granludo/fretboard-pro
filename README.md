# fretboard-pro

Fretboard-pro allows to design a fretboard for a guitar, bass guitar or any fretted instrument fretboard with tempered intonation 

c) By Marc Alier 2022, @granludo  under GPL License v3.0

Demo https://apendizdeluthier.com/fretboard-generator 

## how it works

A web form (on /front-end forlder ) invoques a web app (implemented webs.py file) and returns an HTML file with 
the description of the fretboar (tables of fret positions and so on) and the links to the PDF file with a 1:1 scale drawing of the 
fretboard ( including fret positions, nut, intonnated bridge and string positions ) and a DXF file.

conf.json file informs the URL of the output folder so the links are usable.


