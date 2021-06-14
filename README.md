# NENA Corpus Pipeline

Pipeline for processing NENA markup format texts

# Requirements

Minimum Python requirements are Python 3.8. Package dependencies are stored in [requirements.txt](requirements.txt).

# How to use

For example usage of the pipeline see [example.ipynb](example.ipynb).

The pipeline outputs the following to the specified outdir (see example notebook above):

    1) `tf` directory containing the indexed corpus in 
        text-fabric format
    2) documentation.md: a file containing documentation
        on the makeup of the corpus
    3) search_tool: set of static files which are the 
        nena_search compiled from the corpus data
