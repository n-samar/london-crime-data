```
source .venv/bin/activate
streamlit run app.py
# Then, navigate using your browser to the link that streamlit outputs
```

This presents total crimes per LSOA (one dot per LSOA) from January 2024 to
June 2025.

The crime threshold you pick corresponds to the color yellow. Lower crime areas
are greener, with zero crime being all green. Higher are reader, with `2 *
threshold` being all red.
