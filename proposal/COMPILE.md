Compilation instructions for MAT292_Proposal.tex (embedded bibliography)

This version of `MAT292_Proposal.tex` includes an embedded `thebibliography`
environment, so it no longer needs `references.bib` or BibTeX. You can compile
it with a single pdflatex run.

From the `proposal` directory (PowerShell):

   pdflatex MAT292_Proposal.tex

If you edit the document and want to be safe, running pdflatex twice is
standard practice:

   pdflatex MAT292_Proposal.tex; pdflatex MAT292_Proposal.tex

If you prefer to keep using BibTeX or switch to biblatex/biber, tell me and
I'll revert or convert the bibliography accordingly.
