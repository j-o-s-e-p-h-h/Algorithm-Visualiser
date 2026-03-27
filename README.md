# Algorithm Visualiser

A simple Pygame sorting visualizer with a clean white background, gray bars, and multiple classic sorting algorithms.

## Preview

![Sorting Algorithm Visualizer Preview](assets/sorting-visualizer-preview.png)

## Run

```bash
python visualizer.py
```

## Current Interface

The app displays the following layout on screen:

```text
Sorting Algorithm Visualizer
R - Reset | SPACE - Start / Pause
A - Ascending | D - Descending
B - Bubble | I - Insertion | S - Selection | C - Cocktail
M - Merge | Q - Quick
Bubble Sort | Ascending | Ready
```

The status line updates while the program is running to show:

- the currently selected algorithm
- whether the sort is ascending or descending
- whether the app is ready or actively sorting

## Controls

- `R`: reset the list
- `SPACE`: start or pause the current sort
- `A`: sort in ascending order
- `D`: sort in descending order
- `B`: Bubble Sort
- `I`: Insertion Sort
- `S`: Selection Sort
- `C`: Cocktail Sort
- `M`: Merge Sort
- `Q`: Quick Sort

## Visual Style

- white background
- grayscale bars
- highlighted bars during comparisons and swaps
- large `comicsans` headings and controls
