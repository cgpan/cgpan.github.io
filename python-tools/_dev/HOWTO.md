# PythonTools — how to add and verify entries

The page at `/python-tools/` is rendered entirely from the JSON files in `python-tools/data/`.
Adding a topic for a new week means editing one of those files and running the verifier.
Nothing in `_pages/python-tools.html`, `python-tools.js` or `python-tools.css` needs to change.

Everything in this `_dev/` folder is ignored by Jekyll (folders starting with `_` are never
published), so notes, fixtures and scripts can live here safely. Do **not** put a `README.md`
or any other `.md` file at the top level of `python-tools/`: GitHub Pages turns it into a page.

## Files

| File | Purpose |
|---|---|
| `data/manifest.json` | language list and order, default tab, footer text, verification stamp |
| `data/weeks.json` | week number → date and topic label (drives the “By week” view) |
| `data/markdown.json`, `python.json`, `sql.json`, `shell.json`, `git.json` | one file per language: its topics and entries |
| `img/*.png` | chart images produced by the verifier for entries marked `"figure": true` |
| `_dev/verify.py` | runs every example and records or checks its output |
| `_dev/runner.py` | the Colab-style cell runner used by `verify.py` for Python entries |
| `_dev/fixtures/*.csv` | the course datasets, copied into the sandbox before each run |
| `_dev/INVENTORY.md` | the approved content inventory and decisions log |

## Adding an entry

1. Open the language file and add an object to `entries`. Minimal example:

```json
{
  "id": "python/pd-melt",
  "title": "pd.melt — wide to long",
  "topic": "pandas-ii",
  "week": 13,
  "summary": "One plain-English sentence about what it does.",
  "syntax": "pd.melt(df, id_vars=[...], value_vars=[...])",
  "setup": "import pandas as pd\ndf = pd.DataFrame({...})",
  "setup_note": "imports and a small table",
  "example": "print(pd.melt(df, id_vars=[\"id\"]))",
  "output": "",
  "gotcha": "The mistake beginners make with it.",
  "related": ["python/pd-pivot-table"],
  "keywords": ["reshape", "long format", "unpivot"],
  "source": "hudm5001/class_notes/12_data_visualization.ipynb Exercise 5"
}
```

   * `id` must start with the language name and is the deep link: `#python/pd-melt`.
   * `topic` must be one of the ids in that file's `topics` list; add a topic there first if needed
     (topics are shown in the rail in the order listed).
   * `week` is the week the construct is introduced (see `weeks.json`).
   * `setup` is optional code that runs before the example and is shown collapsed on the page.
   * Leave `output` empty; the verifier fills it. Use backticks in prose fields for inline code.
   * `keywords` feed the search box; add the words a student would type (`merge` on the SQL join entry, for example).

2. Optional flags:

| Flag | Meaning |
|---|---|
| `"tags": ["extra"]` | shows the `extra` chip: used in an assignment but not taught in a lecture |
| `"expect_error": true` | the example is meant to fail; the last line of the error becomes part of the output |
| `"figure": true` | the example draws a chart; the image is saved to `img/` and linked automatically |
| `"volatile": true` | output changes run to run (timings, dates); it is recorded but never fails a check |
| `"no_run": true` | nothing to run (menu paths, concepts); give `syntax` and optionally `output_note` |
| `"runner": "python"` | run a Shell/Git entry as a Colab cell (for `!` and `%cd` lines); `"shell"` works the other way round |
| `"output_note"` | a sentence shown under the output |

3. Run the verifier from the repository root:

```bash
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
/opt/anaconda3/envs/hudm5001-verify/bin/python python-tools/_dev/verify.py --write --show --id python/pd-melt
```

   `--write` stores the real output (and the figure); `--show` prints it so you can read it.
   Run without `--id` to do every entry, and without `--write` to check that stored outputs still match.

4. Build the site locally (`./run_server.sh`, with the same `LANG`/`LC_ALL` exported) and open
   `http://127.0.0.1:4000/python-tools/#python/pd-melt`.

## The verification environment

Outputs are recorded with the conda environment `hudm5001-verify`, created to match Google Colab
in September 2026: Python 3.13, pandas 2.2.3, numpy 2.x, matplotlib, plotnine, plotly, kaleido
and the `markdown` renderer. Re-create it with:

```bash
conda create -n hudm5001-verify -c conda-forge --override-channels python=3.13 pandas=2.2.3 numpy matplotlib plotnine plotly markdown
/opt/anaconda3/envs/hudm5001-verify/bin/pip install kaleido
```

How each language runs is documented at the top of `verify.py`. In short: Python examples run as
notebook cells (bare last expressions are displayed, `!` lines and `%cd` work, `%%writefile` writes a
file); SQL goes through the `sqlite3` shell; Shell and Git run in bash inside a fresh `~/hudm5001`
folder whose path is shown as `/Users/student`.

## Changing the week schedule

Edit `data/weeks.json`. The “By week” rail and the week chips read from it; entries carry only the
week number.
