# TruthDiscovery
Truth Discovery in DBGroup@SUSTech

## Project Note
This is my graduation project for my bachelor’s degree.

## Project Details
Within this project, we implement several present algorithms in Truth Discovery, including LTM (VLDB 2012), DART (VLDB 2018) and some naive solution as Majority Vote.
We propose a two-stage model to infer truth from conflicting data.

First stage: estimate source quality based on quality measure, i.e. recall and specificity.

Second stage: use estimated source quality for initialization and perform truth discovery.

Thank Xueling LIN for sharing the data used in her work (Domain-Aware Multi-Truth Discovery from Conflicting Sources, VLDB 2018).

Orginal data contains two datasets:
1. Book
  - Book and (multiple) author information
  - Conflicts on author information, provided by multiple information sources (booksellers)
2. Movie
  - Movie and (multiple) director information
  - Conflicts on director information, provided by multiple information sources (websites)

We perform data cleaning on both datasets and use them as inputs for our model.
