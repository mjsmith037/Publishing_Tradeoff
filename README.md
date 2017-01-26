# Code to Replicate Analsis for: "And, not Or: Quantity, Quality in Scientific Publishing"
### Matthew J. Michalska-Smith and Stefano Allesina

---------------------------------------------------

## Data Collection

A python script for extracting publication records associated with Scopus IDs is
provided in `Code_Analysis/Retrieve_papers.py`. This Script requires only a
;-delimited file containing columns labeled 'scopus1', 'scopus2', and 'scopus3'
containing the (up to three) synonymous Scopus IDs affiliated with each author
to be included in the analysis, and a Scopus API Key. The latter can be obtained
at (https://dev.elsevier.com/sc_apis.html).

This script will produce a series of files (one for each author) in the `Data`
folder to be utilized in the further analysis. Each of these files will be a
;-delimited file with the header:

`Author;PaperID;Citations;Year;Journal`

## Basic Pairwise Analysis

This part of the analysis involves running the script `PairwiseComparision.R`,
in the folder `Code_Analysis`. There are several global parameters set at the
beginning of the file:

| Parameter    | Default Value | Definition                                        |
|--------------|---------------|---------------------------------------------------|
INTERVAL_START | 1980          | earliest year to consider publications from       |
INTERVAL_END   | 2006          | latest year to consider publications from         |
MINPAPERS      | 20            | the minimum number of publications an author must have within the interval to be included |
QUALITY_TRANS  | "log"         | the transformation (if any) to perform on citations to make them a quality metric |

This will produce a data file located at

`Figures/PairwiseComparison_[QUALITY_TRANS]_[INTERVAL_START]-[INTERVAL_END].RData`

to be used in the figure generation scripts.

## Figure and Table generation

Figures and tables associated with the analysis can be found in the `Code_Figures`
folder. These two scripts `DensityPlot.Rmd` and `KStestPlot.Rmd` plot the density
distributions of the concordance values and statistical comparisons between the
distributions, respectively. The latter also produces the tables found in the text.
