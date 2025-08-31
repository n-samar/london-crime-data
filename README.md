Download the merged_output.csv file from this Google drive link and place it at
the root of this repo (this is a ~300MB file containing the crime data in csv format): https://drive.google.com/file/d/1gVodZbMmBUfXODtTKNlmCZWMIeHtrKXe/view?usp=sharing

I suggest you create a conda environment, and pip install all the dependencies
that need to be installed: streamlit, pandas, pydeck, plotly, numpy. Then you can:

```
source .venv/bin/activate # activate conda environment
streamlit run app.py
# Then, navigate using your browser to the link that streamlit outputs
```

This presents total crimes per LSOA (one dot per LSOA) from January 2024 to
June 2025.

The crime threshold you pick corresponds to the color yellow. Lower crime areas
are greener, with zero crime being all green. Higher are reder, with `2 *
threshold` being all red.

## Use `merge_csvs.py` to collect up-to-date crime data

You can merge the per-month crime statistics CSVs from the [government website](https://data.police.uk/data/) (select date range and Metropolitan Police Service; you will get one directory per month) into the merged_outputs.csv format used by app.py
by just putting the downloaded containing directories (called, e.g., 2025-02) in the root of this directory and running merge_csvs.py.
