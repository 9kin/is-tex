# https://tex.stackexchange.com/questions/331400/compiling-toc-once
# https://tex.stackexchange.com/questions/19182/how-to-influence-the-name-of-the-pdf-file-created-with-pdflatex-from-within-the

from os import system, chdir
from pathlib import Path


def compile(directory, pdf_output):
    chdir(directory)
    for _ in range(2):
        system("pdflatex -synctex=1 -interaction=nonstopmode --shell-escape exam.tex")
    chdir("../..")
    (Path(directory) / "exam.pdf").rename(pdf_output)


compile("course-1/linear-algebra", "linear-algebra-exam.pdf")
compile("course-1/mathematical-analysis", "mathematical-analysis.pdf")
