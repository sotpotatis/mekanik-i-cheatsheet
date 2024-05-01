# LaTeX to Anki

A very simple script to create Anki flashcards from LaTeX documents.

## Usage

Wrap a part of your LaTeX document with `\begin+end{ankiflashcard}` like this:

```
\begin{ankiflashcard}
    \textit{This will be shown in your flashcard...}
\end{ankiflashcard}
```

Make sure to define the dummy environment `ankiflashcard` in the beginning of you document like so:

```
\newenvironment{ankiflashcard}[1][]{}{}
```

The `1` can be changed to any number right now, the script might parse arguments at a later stage.