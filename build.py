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


repeat = 1
if 't' in sys.argv:
    repeat = 2
if len(sys.argv) == 1 or 'linal' in sys.argv:
    compile("course-1/linear-algebra", "linear-algebra-exam.pdf", repeat)
if len(sys.argv) == 1 or 'matan' in sys.argv:
    compile("course-1/mathematical-analysis", "mathematical-analysis.pdf", repeat)

