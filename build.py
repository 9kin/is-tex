# https://tex.stackexchange.com/questions/331400/compiling-toc-once
# https://tex.stackexchange.com/questions/19182/how-to-influence-the-name-of-the-pdf-file-created-with-pdflatex-from-within-the
import sys

from os import system, chdir
from pathlib import Path


def compile(directory, pdf_output, repeat=1):
    chdir(directory)
    for _ in range(repeat):
        system("pdflatex -synctex=1 -interaction=nonstopmode --shell-escape exam.tex")
    chdir("../..")
    (Path(directory) / "exam.pdf").rename(pdf_output)

args = sys.argv[1:]
repeat = 1
if 't' in args:
    repeat = 2
    args = list(filter(lambda x : x != 't', args))
if len(args) == 0 or 'linal' in args:
    compile("course-1/linear-algebra", "linear-algebra-exam.pdf", repeat)
if len(args) == 0 or 'matan' in args:
    compile("course-1/mathematical-analysis", "mathematical-analysis.pdf", repeat)

