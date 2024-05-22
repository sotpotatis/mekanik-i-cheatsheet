# Mekanik I Cheatsheet

Contains a cheatsheet with mathematical formulas and material overview for the course SG1133 at [KTH](https://kth.se). It should be (educated guess) similar to other courses covering the material in the book Mekanik I by Prof. Apazidis.
I am a student, not affiliated with anyone teaching the course. The material comes with full reservations for errors.

### Downloads

--> **Latest cheatsheet version:** [here](https://github.com/sotpotatis/mekanik-i-cheatsheet/blob/main/main.pdf)


--> **Latest flashcards version:** [here](https://github.com/sotpotatis/mekanik-i-cheatsheet/blob/main/maintex-deck.apkg)

### Auto-compilation

As I change the cheatsheet, it should automatically be recompiled (updated) and put here. You should find the cheatsheet with the very descriptive name `main.pdf`.

### Anki Flashcards

I created a utility that will probably move to its own repository (hence the existence of `latex-to-anki-README.md`) sometime soon. It should automatically covert the content to an Anki flashcards deck whenever I make updates.
You can download the flashcards from the link above.

**Note:** it seems like the flashcards don't work out of the box (even after installing LaTeX on your computer)

You need LaTeX installed on your computer for the cards to work in Anki and might have to mess around a little with the preamble. Feel free to open an issue if you need help.

You might have some luck changing "Sidhuvud" of the "Basic (Genanki)" notetype to: 
```latex
\documentclass[12pt]{article}\usepackage{graphicx} % Required for inserting images
\usepackage{pdflscape}
\usepackage{multicol}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{fancyhdr}
\usepackage{cancel}
\usepackage{tgbonum}
\usepackage{float}
\usepackage[swedish]{babel}
\usepackage{hyperref}
\usepackage{wasysym}
\usepackage{enumitem}
\usepackage{tabularx}
\usepackage[title]{appendix}
\usepackage[dvipsnames]{xcolor}\usepackage{tgadventor}
\usepackage{helvet}
 \usepackage[stable]{footmisc}
\usepackage{parskip}
\usepackage[swedish]{babel}
\usepackage{dirtytalk}
\usepackage[a4paper, landscape]{geometry}
\renewcommand{\headrule}{}
 \renewcommand{\familydefault}{phv}
\usepackage{sectsty}
\allsectionsfont{\fontfamily{qag}\selectfont}
\pagestyle{fancy}
\pagecolor{SkyBlue!10}
\fancyhf{}
\fancyhead[C]{
\fontfamily{cmr}\selectfont
\colorbox{yellow!25!white}{
\makebox[\textwidth]{
\large{
\llap{\textbf{Mekanik I - Sammanfattning}$\quad\cdot$}
\clap{}
\rlap{\textit{Albin Seijmer}$\cdot$\textit{COPEN}}
}
}
}
\color{ProcessBlue}\rule{\textwidth}{2pt}
}
\newcommand{\dummyargument}{}
\newenvironment{ankiflashcard}[1]{}{}
\usepackage{blindtext}
\usepackage{paracol}
% Column configuration
\setlength{\columnsep}{2em}
\setlength{\columnseprule}{0.1pt}
% Row configuration for tables and arrays
\renewcommand{\arraystretch}{1.25}
\usepackage{amsmath}
\setcounter{secnumdepth}{0}
\title{Mekanik I - Sammanfattning}
\date{}
% Own commands
\newcommand{\ruler}{
\rule{0.5\textwidth}{0.5pt}
}
\newcommand{\numbercircle}[1]{
\text{\textcircled{#1}}
}
\newcommand{\numbercirclewithunderbrace}[2]{
\underbrace{#1}_{\numbercircle{#2}}
}
\usepackage{tikz}

\newcommand\centerofmass{%
    \tikz[radius=0.4em] {%
        \fill (0,0) -- ++(0.4em,0) arc [start angle=0,end angle=90] -- ++(0,-0.8em) arc [start angle=270, end angle=180];%
        \draw (0,0) circle;%
    }%
}
\newcommand{\midtitle}[1]{
\begin{center}
\Huge{\text{#1}}
\newpage
\end{center}
}

            \special{papersize=3in,5in}
            \usepackage[utf8]{inputenc}
            \usepackage{amssymb,amsmath}
            \pagestyle{empty}
            \setlength{\parindent}{0in}
            \begin{document}
```

and then changing "Sidfot" to `\end{document}`
