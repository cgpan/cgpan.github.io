# PythonTools — Content Inventory (HUDM 5001, Fall 2026)

Status: **approved 2026-09-04** with the decisions recorded in §11 (setup folded into week 1, mini 01 split across weeks 1–2, visualization in at week 13, Markdown kept and now sourced from the Week 1 notebook, beginner SQL constructs from the SQL page included). Nothing on the page is built yet. This file lists every entry the reference page would contain, where each one comes from, and the week tag it would carry. Rows marked `extra` are additions that are not taught in a lecture but appear in an assignment or solution; rows marked `confirm` need a decision from you.

Source roots (read-only): `.../PhD_Teaching/HUDM_5001_Instructor` and the live course folder `.../PhD_Teaching/HUDM_5001_2026FALL` (GitHub: `cgpan/hudm5001`). Every file opened successfully; no cloud-only placeholders were hit. The syllabus PDF in `PhD_Teaching/` could not be rendered (no `pdftoppm` on this machine) but its content is duplicated in `HUDM_5001_2026FALL/README.md` (syllabus version 08.31.2026), which was read in full.

---

## 1. Source precedence and week mapping

Three overlapping sets of materials exist. I used them in this order:

| Priority | Directory | What it is | Used for |
|---|---|---|---|
| 0 | `HUDM_5001_2026FALL/` | The live Fall 2026 course repo: `README.md` (= syllabus, schedule, AI policy), `Week_01_Colab_Markdown_Python.ipynb`, `asset/*.csv` | **Authoritative** for the week schedule and for week 1 (Colab shortcuts, Markdown, first Python, AI-use comment block). New weekly notebooks will land here |
| 1 | `hudm5001_mini/` (+ `assignment/`, `assignment_solutions/`) | Your Fall 2026 session notebooks 01–05, last committed Sep 3 | **Authoritative** for weeks 1–6 |
| 2 | `hudm5001/class_notes/` | Your synthesized 12-session Colab set (June 2026, Fall 2025 pacing) + `00_environment_setup.md` | Weeks 7–13 (no mini notebook exists yet for those), Shell, Git, setup |
| 3 | `hudm5001_youmilab/` | Prof. Suk's original Fall 2025 repo | Detail and examples where 1–2 are thin; "youmilab-only" candidates listed in §8 |
| — | `Class_asset/` | `class_anouncement.docx` (announcements, no syntax), `why_sql_not_excel.html` (SQL motivation page) | The HTML page adds `HAVING`, `DISTINCT`, `IS NOT NULL`, `PRIMARY KEY`/`NOT NULL`/`CHECK` — listed as `confirm` in §4 |

Week tags follow the Fall 2026 schedule in `HUDM_5001_2026FALL/README.md`. Setup material is folded into week 1 (decision 1).

| Week | Date | Syllabus topic | Source | Note |
|---|---|---|---|---|
| 1 | 9/8 | Syllabus and Intro to Python | `HUDM_5001_2026FALL/Week_01_Colab_Markdown_Python.ipynb`; `hudm5001_mini/01_*` §2.1; `hudm5001/class_notes/00_environment_setup.md` | Colab shortcuts, Markdown, comments/print, AI-use comment block; the local-setup entries (conda, VS Code, running a script) are tagged week 1 too. The live notebook links a Google Doc "Set Up a Python Coding Environment" that is not in the Drive folder, so the setup entries follow `00_environment_setup.md` — worth a cross-check against the Doc |
| 2 | 9/15 | Data Types, Variables and Expressions | `hudm5001_mini/01_Python_Quick_Start.ipynb` §2.2–§2.9 | |
| 3 | 9/22 | Operators, Input/Output, NumPy | `hudm5001_mini/02_Operators_IO_Numpy.ipynb` | |
| 4 | 9/29 | pandas | `hudm5001_mini/03_Pandas.ipynb` | |
| 5 | 10/6 | pandas, SQLite Database | `hudm5001_mini/04_Pandas_SQLite.ipynb` | |
| 6 | 10/13 | Control Structures and Iterables | `hudm5001_mini/05_Control_Structures_Iterables.ipynb` | |
| 7 | 10/20 | Functions, Lambdas, List Comprehensions | `hudm5001/class_notes/08_functions_lambdas_comprehensions.ipynb` | plus `apply(lambda)` from class_notes 06 |
| 8 | 10/27 | Midterm | — | no entries |
| 9 | 11/3 | Intro to Shell and GitHub (no in-person class; recording) | `hudm5001/class_notes/01_shell_and_command_line.ipynb`, `02_github_version_control.ipynb` | |
| 10 | 11/10 | Python Classes, Object-Oriented Programming | `hudm5001/class_notes/09_classes.ipynb` | |
| 11 | 11/17 | Unit Testing and Exception Handling | `hudm5001/class_notes/10_unit_testing_exception_handling.ipynb` + youmilab command-line `.md` files | includes running scripts from the command line |
| 12 | 11/24 | Advanced Topics (1): Coding Practices with AI | `hudm5001/class_notes/11_coding_practices_with_ai.ipynb` | mostly conceptual; 4 syntax entries |
| 13 | 12/1 | Advanced Topics (2): TBD → Data Visualization | `hudm5001/class_notes/12_data_visualization.ipynb` | approved (decision 3); label editable in the week data file |
| 14–16 | 12/8–12/22 | Presentation, Final Project Discussion, Final Project | — | no entries; statsmodels and Dash stay out (§8) unless you say otherwise |

---

## 2. Summary counts

| Language | Topics | Entries | of which `extra` |
|---|---|---|---|
| Python | 16 | 208 | 9 |
| SQL | 5 | 24 | 3 |
| Shell | 5 | 34 | 0 |
| Git | 4 | 23 | 1 |
| Markdown | 1 | 13 | 0 |
| Workflow tab | 5 | 23 | 0 |
| **Total** | **36** | **325** | **13** |

Entry granularity: one entry = one syntax pattern a student would look up. Closely related methods share an entry (for example, the five string methods taught in mini 01 are one entry). 295 is on the dense side. The easiest cuts are the rows marked `optional`, and the three small groups that are menu paths rather than syntax (§3.1 Colab, §3.16, §5.5 setup). Merging those would bring the total to roughly 250 without losing any syntax.

Entry ids are `language/slug` and become the deep link, e.g. `/python-tools/#python/pd-groupby`.

This file lives in `python-tools/_dev/`, which Jekyll never publishes (folders starting with `_` are skipped), together with `verify.py` and its fixtures.

---

## 3. Python

### 3.1 Notebooks & Colab — week 1
Source: `HUDM_5001_2026FALL/Week_01_Colab_Markdown_Python.ipynb` cells 3–6 (cells, shortcuts), `hudm5001_mini/01_Python_Quick_Start.ipynb` header cells, `hudm5001_mini/02_*` "How to open this notebook", `hudm5001_mini/05_*` §2.6 (interrupt), `hudm5001/class_notes/00_environment_setup.md` §1.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/colab-open-notebook | Open a notebook in Colab (Drive / Upload / badge) | 1 | mini 02 header | syntax = menu path |
| python/colab-run-cell | Run a cell, run the Setup cell first (Shift+Enter) | 1 | mini 02 header | |
| python/colab-code-vs-text-cell | Code cells vs text (Markdown) cells | 1 | Week_01 c3 | |
| python/colab-shortcuts | Colab shortcuts: `A`, `B`, `Cmd/Ctrl+M D`, `Cmd/Ctrl+M M`, `Cmd/Ctrl+M Y`; Tools ▸ Keyboard shortcuts | 1 | Week_01 c4, c6 | |
| python/jupyter-shortcuts | Jupyter shortcuts: `D`, `M`, `Y` | 1 | Week_01 c5 | |
| python/colab-save-copy | Save a copy in Drive | 1 | mini 01 tip cell | |
| python/colab-interrupt | Stop a runaway cell (Runtime ▸ Interrupt execution) | 6 | mini 05 §2.6 | |
| python/colab-files-panel | Download a file written in the session (Files panel) | 13 | class_notes 12 §2.5 | optional |

### 3.2 First Python: variables & expressions — week 1
Source: `hudm5001_mini/01_Python_Quick_Start.ipynb` §2.1 (cells 9–33).

| id | title | week | source | notes |
|---|---|---|---|---|
| python/print | `print("Hello, world!")`; several values | 1 | Week_01 c27; mini 01 c9–11 | `end=' '` from class_notes 03/07 noted |
| python/comments | Comments with `#`; the AI-use comment block at the top of a submission | 1 | Week_01 c26–27, c29 (AI policy) | |
| python/assignment | Assign a variable with `=` | 1 | mini 01 c9 | |
| python/multiple-assignment | Multiple assignment and unpacking (`a, b = 3, 4`) | 1 | mini 01 c10–11 | |
| python/variable-names | Variable naming rules and reserved words | 1 | mini 01 c13, ex 3 | |
| python/arithmetic-expressions | Arithmetic: `+ - * / **` | 1 | mini 01 c15–19 | `// %` come in week 3 |
| python/numeric-literals-underscore | Readable numbers with `_` (`1_000_000`) | 1 | mini 01 c12 | |
| python/type | Inspect a value with `type()` | 1 | mini 01 c30 | |
| python/del | Delete a variable with `del` | 1 | mini 01 c31 | |
| python/string-literal | Text needs quotes (`"16"` is not `16`) | 1 | mini 01 c26–28 | |

### 3.3 Data types — week 2
Source: `hudm5001_mini/01_Python_Quick_Start.ipynb` §2.2–§2.9; `hudm5001/class_notes/03_*` for `.get()`.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/bool | Booleans `True` / `False` | 2 | mini 01 c35 | |
| python/isinstance | Type check with `isinstance()` | 2 | mini 01 c35–39 | |
| python/and-or-not | `and`, `or`, `not` and short-circuiting | 2 | mini 01 c36–37; assignment 01 A6 | |
| python/int-float | `int` and `float` | 2 | mini 01 c39 | |
| python/round | `round(x, ndigits)` | 2 | mini 01 c40 | |
| python/str-index-slice | String indexing and slicing `s[0]`, `s[:2]`, `s[-2:]` | 2 | mini 01 c43 | |
| python/len | `len()` | 2 | mini 01 c43 | |
| python/str-methods | String methods: `upper lower strip startswith endswith` | 2 | mini 01 c44 | |
| python/str-replace | `str.replace()` | 2 | mini 01 c48 | |
| python/str-split | `str.split()` (whitespace or a separator) | 2 | mini 01 c58–59 | |
| python/str-immutable | Strings are immutable | 2 | mini 01 c46 | |
| python/str-concat | Concatenate with `+` | 2 | mini 01 c50–52 | |
| python/f-string | f-strings and `.format()` | 2 | mini 01 c50 | format specs `:.2f`, `:12s` from class_notes 05/07 noted |
| python/list | Lists: create, index, slice, mixed types | 2 | mini 01 c57 | |
| python/list-mutate | Change, `append`, `remove`, `+` | 2 | mini 01 c57–61 | |
| python/list-sort | `list.sort()` and `sort(reverse=True)` | 2 | mini 01 c62 | |
| python/nested-list | Nested lists (list of lists) and `[i][j]` indexing | 2 | assignment 01 C2, solutions 01 | `extra` |
| python/tuple | Tuples: ordered, immutable | 2 | mini 01 c66 | |
| python/tuple-unpacking | Tuple unpacking into variables | 2 | mini 01 c11; solutions 01 B6 | |
| python/set | Sets: unique, unordered, `in` | 2 | mini 01 c68 | |
| python/set-union-intersection | `set.union()` / `set.intersection()` | 2 | mini 01 c68 | |
| python/set-from-list | De-duplicate a list with `set(list)` | 2 | solutions 01 C4, 02 C4 | `extra` |
| python/dict | Dictionaries: create, look up, add a key | 2 | mini 01 c70 | |
| python/dict-keys-values-items | `.keys()`, `.values()`, `.items()` | 2 | mini 01 c70 | |
| python/dict-get | Safe lookup with `dict.get()` | 2 | class_notes 03 c44 | not in mini 01 |
| python/nested-dict | Nested dictionaries | 2 | mini 01 c72–75; assignment 01 A9 | |
| python/range | `range(start, stop, step)` and `list(range(...))` | 2 | mini 01 c78 | |
| python/type-conversion | Conversions `int() float() str() list()`; `int('3.8')` fails | 2 | mini 01 c77, takeaways; class_notes 03 c50 | |
| python/mutable-immutable | Mutable vs immutable types (summary table) | 2 | mini 01 takeaways | |
| python/builtin-sum-min-max | `sum()`, `min()`, `max()` on a list | 2 | mini 05 §2.5 text; class_notes 09 solution | `extra` |

### 3.4 Operators — week 3
Source: `hudm5001_mini/02_Operators_IO_Numpy.ipynb` §2.1.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/floor-division | Floor division `//` | 3 | mini 02 c5 | |
| python/modulus | Modulus `%` (remainder, even/odd) | 3 | mini 02 c6 | |
| python/exponent | Exponent `**` | 3 | mini 02 c6 | |
| python/comparison-operators | Comparisons `== != < <= > >=` | 3 | mini 02 c9 | |
| python/is-vs-equals | Identity `is` vs equality `==`; `id()` | 3 | mini 02 c11–12 | |
| python/in-not-in | Membership `in` / `not in` (list and dict keys) | 3 | mini 02 c13, ex Q4 | |
| python/chained-comparison | Chained comparison `-2 < x < 2` and the parentheses trap | 6 | mini 05 c12 | listed here, tagged week 6 |

### 3.5 Input / output & files — week 3
Source: `hudm5001_mini/02_Operators_IO_Numpy.ipynb` §2.2.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/open-write | Write a text file with `with open(path, 'w')` | 3 | mini 02 c27 | |
| python/open-read | Read a text file with `.read()` | 3 | mini 02 c27 | |
| python/file-modes | File modes `'r' 'w' 'a'` and `encoding='utf-8'` | 3 | mini 02 c25, c28 | |
| python/json-dump-load | `json.dump` / `json.load` | 3 | mini 02 c30 | |
| python/json-numpy-gotcha | JSON refuses NumPy numbers: wrap in `int()` / `float()` | 5 | mini 04 takeaways | |
| python/os-path | `os.getcwd`, `os.path.basename/dirname/join/exists` | 3 | mini 02 c35 | |

### 3.6 NumPy — week 3
Source: `hudm5001_mini/02_Operators_IO_Numpy.ipynb` §2.3.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/import-as | `import numpy as np` (aliases) | 3 | mini 02 c3 | |
| python/np-random | `np.random.seed`, `randint`, `randn` | 3 | mini 02 c48, c56 | |
| python/np-array | Create an `ndarray`; `.shape`, `.dtype` | 3 | mini 02 c50 | |
| python/np-vectorized | Vectorized element-wise math | 3 | mini 02 c52 | |
| python/np-special-arrays | `zeros`, `ones`, `identity`, `arange` | 3 | mini 02 c54 | |
| python/np-index-slice | 1-D and 2-D indexing `a[1:3]`, `m[0, 2]`, `m[:, -1]` | 3 | mini 02 c56–57 | |
| python/np-boolean-indexing | Boolean indexing `z[z > 0]` | 3 | mini 02 c56 | |
| python/np-summaries | `.mean() .max() .sum(axis=0) .round()` | 3 | mini 02 c57 | |
| python/mask-sum-count | Count matches with `(mask).sum()` | 3 | solutions 02 C1/C3/C4, 03 C2, 05 C2 | `extra` — used in five solutions |
| python/series-to-array | Series → array with `.values` / `np.array(series)` | 4 | mini 03 c7; solutions 02 C4 | `extra` |

### 3.7 pandas I — week 4
Source: `hudm5001_mini/03_Pandas.ipynb`.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/pd-series | `pd.Series` with an index | 4 | mini 03 c5–9 | |
| python/pd-dataframe-from-dict | `pd.DataFrame` from a dict of lists | 4 | mini 03 c15 | custom `index=` from solutions 03 B3 noted |
| python/pd-read-csv | `pd.read_csv` (path or URL; `index_col=0`) | 4 | mini 03 c20; class_notes 05 c10 | |
| python/pd-inspect | `.head() .tail() .shape .columns .dtypes` | 4 | mini 03 c20–22 | `.info()` from class_notes 05 noted |
| python/pd-describe | `.describe()` (numeric only) | 4 | mini 03 c22 | |
| python/pd-select-columns | `df["col"]` vs `df[["a", "b"]]` | 4 | mini 03 c24 | |
| python/pd-iloc | Rows by position `.iloc` | 4 | mini 03 c25 | |
| python/pd-loc | Rows by label `.loc`, right end included | 4 | mini 03 c25–27 | |
| python/pd-boolean-filter | Filter rows with a boolean mask | 4 | mini 03 c32 | |
| python/pd-combine-conditions | Combine conditions with `&` and `\|` (parentheses) | 4 | mini 03 c34 | |
| python/pd-new-column | Create a column by assignment (vectorized) | 4 | mini 03 c39 | |
| python/pd-value-counts | `.value_counts()` and `normalize=True`; `.unique()` | 4 | mini 03 c41; class_notes 05 solution | |
| python/pd-groupby | `groupby("g")["x"].mean()` | 4 | mini 03 c42 | |
| python/pd-sort-values | `.sort_values(ascending=False)` | 4 | mini 03 c44 | |
| python/pd-missing-basics | `.isna().sum()`, `.dropna()`, `.fillna()` | 4 | mini 03 c49 | |
| python/pd-to-csv | `.to_csv(index=False)` | 4 | mini 03 c51 | |

### 3.8 pandas II — week 5
Source: `hudm5001_mini/04_Pandas_SQLite.ipynb` Part 1.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/pd-agg | `.agg([...])` custom summaries | 5 | mini 04 c10 | |
| python/pd-median-vs-mean | Median vs mean on skewed data | 5 | mini 04 c8–9, ex 1 | conceptual, short |
| python/pd-corr | `.corr()` grid and one pair | 5 | mini 04 c14–16 | |
| python/pd-copy | Work on a copy: `df.copy()` | 5 | mini 04 c21 | |
| python/pd-rename | `.rename(columns={...})` | 5 | mini 04 c21 | |
| python/pd-drop | `.drop(columns=[...])` | 5 | mini 04 c21 | |
| python/pd-astype | Retype with `.astype()` | 5 | mini 04 c22 | |
| python/pd-duplicates | `.duplicated().sum()`, `.drop_duplicates()` | 5 | mini 04 c22 | |
| python/pd-dropna-subset | `.dropna(subset=[...])` | 5 | mini 04 c27 | |
| python/pd-fillna-median | Fill gaps with the median | 5 | mini 04 c27 | |
| python/pd-groupby-agg | `groupby` + `.agg([...])` | 5 | mini 04 c34 | |
| python/pd-groupby-two-keys | Group by two keys | 5 | mini 04 c38 | |
| python/pd-groupby-size | `.groupby(...).size()` / `.count()` | 5 | class_notes 06 solution; mini 04 c43 | |
| python/pd-to-dict | Series → dict with `.to_dict()` | 5 | mini 04 c36 | |
| python/pd-pivot-table | `pd.pivot_table(values, index, columns, aggfunc)` | 5 | mini 04 c40 | |
| python/pd-groupby-drops-nan | Grouping silently drops rows with a missing key | 5 | mini 04 c42–43 | gotcha entry |
| python/pd-concat | `pd.concat` (rows `axis=0`, columns `axis=1`, `ignore_index`) | 5 | mini 04 c49–55, c61 | |
| python/pd-merge | `pd.merge(on=, how=)` | 5 | mini 04 c60, c64 | |
| python/pd-merge-how | `how=` left / right / inner / outer, check the row count | 5 | mini 04 c65–67 | |
| python/pd-get-dummies | One-hot encode with `pd.get_dummies` | 5 | class_notes 06 c18 | `confirm`: not in mini 04 |
| python/pd-apply | `.apply(lambda ...)` on a column / `axis=1` | 7 | class_notes 06 c5; class_notes 11 | tagged week 7 (lambdas); `confirm` |

### 3.9 SQLite from Python — week 5
Source: `hudm5001_mini/04_Pandas_SQLite.ipynb` Part 2. (The SQL statements themselves are in §4.)

| id | title | week | source | notes |
|---|---|---|---|---|
| python/sqlite-connect | `sqlite3.connect("file.db")` and `.cursor()` | 5 | mini 04 c73 | `':memory:'` from class_notes 06 noted |
| python/sqlite-execute-commit | `cur.execute(sql)` then `conn.commit()` | 5 | mini 04 c73 | |
| python/sqlite-executemany | Insert many rows with `executemany` and `?` placeholders | 5 | mini 04 c75 | |
| python/sqlite-fetchall | `.fetchall()` → list of tuples; iterate `conn.execute(q)` | 5 | mini 04 c80; class_notes 06 c26 | |
| python/pd-read-sql-query | `pd.read_sql_query(query, conn)` | 5 | mini 04 c77–78 | `pd.read_sql` alias noted |
| python/pd-to-sql | `df.to_sql(name, conn, index=False, if_exists="replace")` | 5 | mini 04 c82 | |
| python/sqlite-list-tables | List tables via `sqlite_master` | 5 | mini 04 c82 | |
| python/sqlite-close | `conn.close()` | 5 | mini 04 c91 | |
| python/sql-triple-quoted | Multi-line query in a triple-quoted string | 5 | mini 04 c78 | |

### 3.10 Control flow & iterables — week 6
Source: `hudm5001_mini/05_Control_Structures_Iterables.ipynb`.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/if-else | `if` / `else` and indentation | 6 | mini 05 c5–8 | |
| python/if-elif-else | `elif` ladders: first true branch wins | 6 | mini 05 c10–11 | |
| python/conditional-expression | One-line `x if cond else y` | 6 | mini 05 c17 | |
| python/for-loop | `for item in collection:` | 6 | mini 05 c20–22 | |
| python/for-range | `for i in range(n):` | 6 | mini 05 c23 | |
| python/accumulator | Accumulator pattern and `+=` | 6 | mini 05 c25 | |
| python/counter-if | Counter with `if` inside a loop | 6 | mini 05 c27 | |
| python/enumerate | `enumerate(xs, start=1)` | 6 | mini 05 c29 | |
| python/zip | `zip(xs, ys)` | 6 | mini 05 c30 | |
| python/best-so-far | Best-so-far tracker | 6 | mini 05 c32 | |
| python/while-loop | `while cond:` | 6 | mini 05 c37–39 | |
| python/infinite-loop | Infinite loops and how to stop them | 6 | mini 05 c40 | gotcha entry |
| python/break | `break` | 6 | mini 05 c45 | |
| python/continue | `continue` | 6 | mini 05 c46 | |
| python/none-check | Skip `None` with `is None` | 6 | mini 05 c46 | |
| python/iter-next | `iter()` / `next()` / `StopIteration` | 6 | mini 05 c52 | |
| python/iterator-one-shot | Iterators are one-shot: `list(zip(...))` | 6 | mini 05 c54 | |
| python/dict-loop | Loop over a dict: keys, `.values()`, `.items()` | 6 | mini 05 c57–58 | |
| python/series-items | Loop over a Series with `.items()` | 6 | mini 05 c65 | |
| python/loop-columns | Audit columns with `for col in df.columns` | 6 | mini 05 c67 | |
| python/loop-vs-vectorize | Loop over things, vectorize over numbers | 6 | mini 05 c69–70 | timing output varies; will be labeled |
| python/iterrows | `df.iterrows()` (last resort) | 6 | mini 05 c71 | |
| python/time-perf-counter | Time code with `time.perf_counter()` | 6 | mini 05 c69 | optional |

### 3.11 Functions, lambdas, comprehensions — week 7
Source: `hudm5001/class_notes/08_functions_lambdas_comprehensions.ipynb`; youmilab `functions.ipynb`, `lambda_functions.ipynb`, `list_and_dict_comprehensions.ipynb`, `recursion.ipynb` for detail.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/def | Define a function with `def` and `return` | 7 | class_notes 08 c5 | |
| python/docstring | Docstrings, `help()`, `.__doc__` | 7 | class_notes 08 c5–6 | |
| python/positional-keyword-args | Positional vs keyword arguments | 7 | youmilab functions c29–31 | |
| python/default-args | Default arguments (must come last) | 7 | class_notes 08 c11, c13 | |
| python/star-args | `*args` | 7 | class_notes 08 c12 | |
| python/return-multiple | Return several values; `_` to ignore | 7 | class_notes 08 c15 | |
| python/return-none | No `return` gives `None` | 7 | class_notes 08 §2.3 | |
| python/scope | Local vs global scope | 7 | class_notes 08 c17 | `global` keyword from youmilab as gotcha |
| python/lambda | `lambda` functions | 7 | class_notes 08 c19 | |
| python/sorted-key | `sorted(xs, key=lambda ...)` | 7 | class_notes 08 c20 | |
| python/list-comprehension | `[expr for x in xs if cond]` | 7 | class_notes 08 c25–26 | |
| python/dict-comprehension | `{k: v for ...}` | 7 | class_notes 08 c28 | |
| python/str-isdigit | `str.isdigit()` | 7 | class_notes 08 ex 3 | `extra` (exercise only) |
| python/recursion | Recursion: base case + recursive step | 7 | class_notes 08 c33–34 | |
| python/import-math-random | `import math`, `import random` | 7 | youmilab functions_calling_other_functions | `extra`, `confirm` |

### 3.12 Classes — week 10
Source: `hudm5001/class_notes/09_classes.ipynb`; youmilab `classes1.ipynb`.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/class | Define a class; class attribute; method | 10 | class_notes 09 c5 | |
| python/instantiate | Instantiate and use the dot operator | 10 | class_notes 09 c7 | |
| python/self | `self` | 10 | class_notes 09 c9 | |
| python/init | `__init__` constructor with defaults | 10 | class_notes 09 c11–12 | |
| python/instances-independent | Instances hold independent state | 10 | class_notes 09 c14 | |
| python/mutable-default-gotcha | Never use a mutable default (`grades=[]`) | 10 | class_notes 09 c19 | |
| python/method-updates-list | A method that updates a list attribute | 10 | class_notes 09 c19 | Student class, reused in week 11 |
| python/inheritance | Inheritance and overriding | 10 | class_notes 09 c24 | |

### 3.13 Exceptions, testing, scripts — week 11
Source: `hudm5001/class_notes/10_unit_testing_exception_handling.ipynb`; youmilab `exception_handling.ipynb`, `unit_test_notes.md`, `unit_test_*.py`, `__name__equals__main__.ipynb`, `*_from_cmd_line.md`, `book_lover_unit_testing.md`.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/common-exceptions | Common exceptions (table + traceback reading) | 11 | class_notes 10 c4–5 | |
| python/try-except | `try` / `except` | 11 | class_notes 10 c7 | |
| python/try-else-finally | `else` and `finally` | 11 | class_notes 10 c7 | |
| python/except-as | `except ValueError as e` | 11 | class_notes 10 c9 | |
| python/raise | `raise` your own exception | 11 | class_notes 10 c9 | |
| python/assert | `assert cond, msg` | 11 | class_notes 10 c14 | |
| python/unittest-testcase | Quick assert with `unittest.TestCase()` | 11 | class_notes 10 c16 | |
| python/unittest-suite | A `TestCase` subclass with `test_` methods | 11 | class_notes 10 c18 | |
| python/unittest-run-notebook | Run tests inside a notebook (`TestLoader`, `TextTestRunner`) | 11 | class_notes 10 c18 | `unittest.main(argv=..., exit=False)` from book_lover noted |
| python/unittest-main | `unittest.main()` in a script | 11 | youmilab unit_test_testsuite.py | |
| python/unittest-assert-methods | `assertEqual`, `assertTrue`, `assertIn`, `assertRaises`… | 11 | class_notes 10 table; unit_test_notes.md | |
| python/name-main | `if __name__ == "__main__":` | 11 | class_notes 10 c22–25 | |
| python/writefile-magic | `%%writefile script.py` | 11 | class_notes 10 c23 | |
| python/run-script | Run a script: `!python script.py` / `python script.py` | 11 | class_notes 10 c24; setup §7.2 | |
| python/import-module | Import your own file as a module | 11 | class_notes 10 c25 | |
| python/sys-argv | Command-line arguments with `sys.argv` | 11 | youmilab fibonacci_from_cmd_line.md, setup §7.2 | `extra`, `confirm` |

### 3.14 Coding with AI — week 12
Source: `hudm5001/class_notes/11_coding_practices_with_ai.ipynb`.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/hasattr | Verify a method exists with `hasattr()` | 12 | class_notes 11 c19 | |
| python/define-before-call | Define a function before you call it (NameError) | 12 | class_notes 11 c11–12 | debugging pattern |
| python/return-order | Match return order to the unpacking call | 12 | class_notes 11 c12 | debugging pattern |
| python/str-capitalize-map | `.str.capitalize()` and `.map(dict)` on a column | 12 | class_notes 11 solution | `extra` |

### 3.15 Visualization — week 13 (`confirm`)
Source: `hudm5001/class_notes/12_data_visualization.ipynb`; youmilab `matplotlib.ipynb`, `plotnine_ggplot.ipynb`, `plotly.ipynb` for detail.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/matplotlib-inline | `import matplotlib.pyplot as plt`, `%matplotlib inline` | 13 | class_notes 12 c3 | |
| python/pip-install | `!pip install -q plotnine` | 13 | class_notes 12 c3 | |
| python/plt-plot | `plt.plot` with format strings (`'o'`, `'.-r'`) | 13 | class_notes 12 c6–7 | |
| python/plt-labels | `plt.title / xlabel / ylabel / show` | 13 | class_notes 12 c6 | |
| python/plt-style | `plt.style.use('ggplot')`, `plt.style.available` | 13 | class_notes 12 c8 | |
| python/pd-plot-bar | Bar chart via `Series.plot(kind='bar')` | 13 | class_notes 12 c10 | |
| python/plt-hist | `plt.hist(bins=, edgecolor=)` | 13 | class_notes 12 c11 | |
| python/pd-boxplot | `df.boxplot(column=, by=)` | 13 | class_notes 12 c12 | |
| python/plt-scatter | `plt.scatter(c=, cmap=)` + `plt.colorbar` | 13 | class_notes 12 ex 1 | |
| python/plt-savefig | `plt.savefig(dpi=150, bbox_inches='tight')` | 13 | class_notes 12 c32 | |
| python/ggplot-basics | `ggplot(df) + aes() + geom_*()` | 13 | class_notes 12 c17 | |
| python/geom-bar | `geom_bar` (counts for you) | 13 | class_notes 12 c17 | |
| python/geom-histogram | `geom_histogram(bins=, fill=)` | 13 | class_notes 12 c18 | |
| python/geom-boxplot | `geom_boxplot` | 13 | class_notes 12 c19 | |
| python/geom-point | `geom_point` with `color=` | 13 | class_notes 12 c21, ex 2 | |
| python/facet-wrap | `facet_wrap('species')` | 13 | class_notes 12 c21 | |
| python/theme-labs | `theme_minimal()`, `labs(title=)` | 13 | class_notes 12 c17 | |
| python/px-scatter | `px.scatter(color=, hover_data=)`, `fig.show()` | 13 | class_notes 12 c26 | |
| python/px-histogram | `px.histogram(barmode='overlay')` | 13 | class_notes 12 c27 | |
| python/px-box | `px.box` | 13 | class_notes 12 c27 | |
| python/px-bar | `px.bar` | 13 | class_notes 12 quick ref | |
| python/chart-choice | Which chart for which question (table) | 13 | class_notes 12 §2.5 | conceptual |

### 3.16 Environment & running Python — week 1 (folded from setup, decision 1)
Source: `hudm5001/class_notes/00_environment_setup.md`; the live course links a Google Doc with the same purpose (not readable from the Drive folder). Shell commands (`conda …`) are in §5.5; these are the Python-side entries.

| id | title | week | source | notes |
|---|---|---|---|---|
| python/repl | The interactive interpreter (`python`, `>>>`, `exit()`) | 1 | setup §7.1 | |
| python/hello-script | A minimal script with the `__main__` guard | 1 | setup §7.2 | duplicates week 11 idea; keep as the setup-flavored version |
| python/verify-setup | One-line install check with `python -c` | 1 | setup §9 | |

---

## 4. SQL (SQLite dialect) — week 5

Source: `hudm5001_mini/04_Pandas_SQLite.ipynb` Part 2 unless noted; `hudm5001/class_notes/06_*`; youmilab `sql_expl.ipynb`, `interacting_w_relational_database.py`, `database_warmup_table_joins.py`; `Class_asset/why_sql_not_excel.html`. All examples will be verified with the `sqlite3` CLI.

### 4.1 Tables and rows
| id | title | week | source | notes |
|---|---|---|---|---|
| sql/create-table | `CREATE TABLE t (col TYPE, ...)` with `TEXT REAL INTEGER`; `PRIMARY KEY` / `NOT NULL` shown as options | 5 | mini 04 c73; why_sql_not_excel.html | `CHECK` dropped (decision 5) |
| sql/drop-table-if-exists | `DROP TABLE IF EXISTS` (re-runnable cells) | 5 | mini 04 c73 | |
| sql/insert | `INSERT INTO t VALUES (...)` | 5 | mini 04 c75 | |
| sql/delete | `DELETE FROM t` | 5 | mini 04 c75 | |

### 4.2 Querying
| id | title | week | source | notes |
|---|---|---|---|---|
| sql/select-star | `SELECT * FROM t` | 5 | mini 04 c77 | |
| sql/select-columns | `SELECT a, b FROM t` | 5 | mini 04 c78 | |
| sql/where | `WHERE` with `= > <` | 5 | mini 04 c78 | |
| sql/where-and | `WHERE ... AND ...` | 5 | mini 04 solution (c) | |
| sql/order-by | `ORDER BY col DESC` | 5 | mini 04 c78 | |
| sql/limit | `LIMIT n` | 5 | mini 04 c87 | |
| sql/as-alias | Rename output with `AS` | 5 | mini 04 c83 | |
| sql/is-null | `WHERE col IS NULL` / `IS NOT NULL` | 5 | why_sql_not_excel.html | `extra` (approved, decision 5) |
| sql/distinct | `SELECT DISTINCT` | 5 | why_sql_not_excel.html | `extra` (approved, decision 5) |

### 4.3 Aggregation
| id | title | week | source | notes |
|---|---|---|---|---|
| sql/count | `COUNT(*)` vs `COUNT(col)` | 5 | mini 04 c85 | pairs with pandas `.count()` gotcha |
| sql/aggregate-functions | `AVG MIN MAX SUM ROUND` | 5 | mini 04 c83; class_notes 06 c28 | |
| sql/group-by | `GROUP BY` | 5 | mini 04 c83 | |
| sql/having | `HAVING` (filter after grouping) | 5 | why_sql_not_excel.html | `extra` (approved, decision 5) |

### 4.4 Joins and the CLI
| id | title | week | source | notes |
|---|---|---|---|---|
| sql/left-join | `LEFT JOIN ... ON` | 5 | mini 04 c87 | |
| sql/inner-join | `INNER JOIN` (drops unmatched rows) | 5 | youmilab database_warmup_table_joins.py | |
| sql/table-alias | Table aliases `passengers AS p` | 5 | mini 04 c87–89 | |
| sql/join-plus-group-by | Join and aggregate together | 5 | mini 04 c89 | |
| sql/sqlite-master | `SELECT name FROM sqlite_master WHERE type='table'` | 5 | mini 04 c82 | |
| sql/sqlite3-cli | The `sqlite3` shell: `sqlite3 file.db`, `.tables`, `.databases`, `.q` | 5 | youmilab interacting_w_relational_database.py | |
| sql/pandas-vs-sql | pandas ↔ SQL side-by-side table | 5 | mini 04 §2.12 | conceptual |

---

## 5. Shell — week 9 (Colab magics tagged where first used)

Source: `hudm5001/class_notes/01_shell_and_command_line.ipynb`; youmilab `warm_ups/shell_warmup.md`; `hudm5001/class_notes/00_environment_setup.md` for §5.5.

### 5.1 Orientation
| id | title | week | source | notes |
|---|---|---|---|---|
| shell/terminal-vs-shell | Terminal vs shell; bash vs PowerShell | 9 | class_notes 01 §2.1 | conceptual |
| shell/bang-in-colab | Run a shell command in Colab with `!` | 9 | class_notes 01 c5 | |
| shell/echo-whoami-date | `echo`, `whoami`, `date` | 9 | class_notes 01 c5 | |
| shell/pwd | `pwd` | 9 | class_notes 01 c7 | |
| shell/ls | `ls` and flags `-l -a -lh -R` | 9 | class_notes 01 c7, c16 | |
| shell/paths | Absolute vs relative paths; root `/` | 9 | class_notes 01 c8–9 | |
| shell/cd | `cd` and the shortcuts `. .. ~ -` | 9 | class_notes 01 c13 | |
| shell/percent-cd | `%cd` persists in Colab, `!cd` does not | 9 | class_notes 01 c14 | |

### 5.2 Files and folders
| id | title | week | source | notes |
|---|---|---|---|---|
| shell/mkdir | `mkdir`, `mkdir -p` | 9 | class_notes 01 c16 | |
| shell/touch | `touch` | 9 | class_notes 01 c16 | |
| shell/cp | `cp` | 9 | class_notes 01 c17 | |
| shell/mv | `mv` (move or rename) | 9 | class_notes 01 c17 | |
| shell/rm | `rm`, `rm -r`, `rmdir` — no undo | 9 | class_notes 01 c15, c18 | |
| shell/file-naming | File-naming rules; quoting names with spaces | 9 | class_notes 01 §2.7 | |

### 5.3 Reading and summarizing files
| id | title | week | source | notes |
|---|---|---|---|---|
| shell/cat | `cat` | 9 | class_notes 01 c22 | |
| shell/head-tail | `head -n`, `tail -n`, `tail -n +2` | 9 | class_notes 01 c23–24 | |
| shell/wc | `wc -l -w -c` | 9 | class_notes 01 c23 | |
| shell/sort-uniq | `sort`, `sort -n`, `uniq -c` | 9 | class_notes 01 c24 | |
| shell/cut | `cut -d, -f2` | 9 | class_notes 01 c24 | |
| shell/pipe | Pipes `\|` | 9 | class_notes 01 c24–25 | |
| shell/wget | Download a file with `wget -q URL -O name` | 9 | class_notes 01 c23 | |
| shell/less-nano-diff | `less`, `nano`, `diff` | 9 | youmilab shell_warmup.md | optional; table only in source |

### 5.4 Speed tricks
| id | title | week | source | notes |
|---|---|---|---|---|
| shell/tab-completion | Tab completion | 9 | class_notes 01 §2.6 | |
| shell/history | `history`, `!76`, `!$`, arrow keys | 9 | class_notes 01 §2.6 | |

### 5.5 Environment & running Python — week 1 (folded from setup, decision 1)
| id | title | week | source | notes |
|---|---|---|---|---|
| shell/conda-version | `conda --version`, `python --version` | 1 | setup §3 | |
| shell/conda-create | `conda create -n hudm5001 python=3.12` | 1 | setup §4.1 | |
| shell/conda-activate | `conda activate` / `conda deactivate` | 1 | setup §4.1 | |
| shell/conda-install | `conda install -c conda-forge ...` | 1 | setup §4.2 | |
| shell/pip-install | `python -m pip install dash` (inside the env; `python -m` so pip matches the interpreter) | 1 | setup §4.2 | |
| shell/conda-env-commands | `conda env list`, `conda list`, `conda env export`, `conda remove` | 1 | setup §4.4 | |
| shell/environment-yml | `conda env create -f environment.yml` | 1 | setup §4.3 | optional |
| shell/launch-tools | `jupyter lab`, `spyder`, `code .` | 1 | setup §5–6, quick ref | |
| shell/python-script | `python my_script.py` | 1 | setup §7.2 | |
| shell/python-dash-c | `python -c "..."` one-liner | 1 | setup §9 | |
| shell/vscode-select-interpreter | VS Code: "Python: Select Interpreter" | 1 | setup §6 | syntax = menu path |
| shell/ipykernel-install | `python -m ipykernel install --user --name hudm5001` | 1 | setup §10 | optional |

---

## 6. Git — week 9

Source: `hudm5001/class_notes/02_github_version_control.ipynb`; youmilab `demo_github.md`, `fork_and_clone_course_repo.md`, `lab_github_assignment.md`.

### 6.1 One-time setup
| id | title | week | source | notes |
|---|---|---|---|---|
| git/git-vs-github | git vs GitHub; repository | 9 | class_notes 02 §2.1 | conceptual |
| git/version | Check git: `git --version` / `git` | 9 | class_notes 02 c3, §2.2 | |
| git/config | `git config --global user.name / user.email` | 9 | class_notes 02 §2.2 | |
| git/personal-access-token | Create a personal access token (GitHub UI) | 9 | class_notes 02 §2.2 | syntax = menu path |

### 6.2 Fork, clone, the core loop
| id | title | week | source | notes |
|---|---|---|---|---|
| git/fork | Fork a repo (GitHub UI) | 9 | class_notes 02 §2.3 | |
| git/clone | `git clone <url>` | 9 | class_notes 02 c8 | |
| git/status | `git status` | 9 | class_notes 02 c11 | |
| git/add | `git add file` / `git add .` | 9 | class_notes 02 §2.5 | |
| git/commit | `git commit -m "message"` | 9 | class_notes 02 §2.5 | |
| git/push | `git push` | 9 | class_notes 02 §2.5 | |
| git/log | `git log --oneline -5` | 9 | class_notes 02 c8 | |
| git/diff | `git diff` | 9 | class_notes 02 c10 (mentioned only) | `extra`, `confirm` |

### 6.3 Staying up to date
| id | title | week | source | notes |
|---|---|---|---|---|
| git/sync-fork | Sync fork ▸ Update branch (GitHub UI) | 9 | class_notes 02 §2.6 | |
| git/pull | `git pull` | 9 | class_notes 02 §2.6 | |
| git/remote | `git remote -v`, `git remote add upstream <url>` | 9 | class_notes 02 §2.7 | |
| git/fetch-merge | `git fetch upstream` + `git merge upstream/main` | 9 | class_notes 02 §2.7 | note: source says `upstream/master master` |

---

## 7. Markdown — week 1 (kept, decision 4)

Source: `HUDM_5001_2026FALL/Week_01_Colab_Markdown_Python.ipynb` §1.1–§1.5 teaches the first nine constructs; the remaining four are constructs students see in every course notebook's text cells (`<details>` is how solutions are hidden). The "output" of a Markdown entry is the rendered result, produced by a real Markdown renderer.

| id | title | week | source | notes |
|---|---|---|---|---|
| markdown/headings | Headings `#` `##` `###` `####` | 1 | Week_01 §1.1 | |
| markdown/paragraphs | Paragraphs and line breaks (two spaces + Enter; blank line) | 1 | Week_01 §1.2 | gotcha: the course teaches the two-space line break; a blank line makes a true paragraph |
| markdown/lists | Bulleted lists with `-` `*` `+`; numbered with `1.` | 1 | Week_01 §1.3 | |
| markdown/bold | Bold `**text**` | 1 | Week_01 §1.4 | |
| markdown/italic | Italic `*text*` | 1 | Week_01 §1.4 | |
| markdown/inline-code | Inline code with backticks | 1 | Week_01 §1.4 | |
| markdown/code-block | Fenced code block with a language (` ```python `) | 1 | Week_01 §1.4 | |
| markdown/link | Links `[text](url)` | 1 | Week_01 §1.5 | |
| markdown/image | Images `![alt](url)` and `<img width=>` | 1 | mini 01 c4, c42 | |
| markdown/blockquote | Blockquotes `>` | 1 | mini 01 c24 | |
| markdown/table | Tables | 1 | mini 01 c4, takeaways | |
| markdown/horizontal-rule | Horizontal rule `---` | 1 | every notebook | |
| markdown/details-summary | Collapsible `<details><summary>` (how solutions are hidden) | 1 | every notebook | |
| markdown/checklist | Task list `- [ ]` | 1 | setup §9 | optional |

---

## 8. Youmilab-only candidates (Fall 2025 material not in mini or class_notes) — `confirm` each

These are taught in Prof. Suk's original notebooks but do not appear in your Fall 2026 notebooks. Default is **exclude** unless you tick them.

| area | construct | source | suggested tag if included |
|---|---|---|---|
| I/O | `input()` | youmilab functions_calling_other_functions, control_structures assignment | extra, week 6 |
| I/O | `pickle.dump / load`, `os.listdir()` | youmilab input_output.ipynb | extra, week 3 |
| I/O | `pd.read_csv(sep=';', header=None)` | youmilab input_output, matplotlib, pandas_myocardial | extra, week 4 |
| dict | `dict.fromkeys()` | youmilab data_types | skip |
| NumPy | `np.sqrt`, `np.unique`, `.std()`, `np.clip`, `.T`, `arr.copy()` | youmilab numpy.ipynb, numpy_assignment | extra, week 3 |
| pandas | `df.replace('?', np.nan)`, `sort_index`, `del df['col']`, `.reshape`, `pd.melt` | youmilab pandas1/2, myocardial, visual_minnesota | skip |
| pandas | `df.query("...")` | youmilab plotly.ipynb | extra, week 13 |
| Matplotlib | `plt.subplot` + `plt.tight_layout`, `plt.legend(loc=)`, `plt.grid`, `plt.xlim/ylim`, `fontsize=` | youmilab matplotlib.ipynb, matplotlib_subplot.ipynb | week 13 |
| Plotnine | `geom_density`, `geom_violin`, `geom_jitter`, `geom_col`, `facet_grid`, `theme_bw`, `scale_fill_*`, `position='fill'`, `geom_smooth`, `patchworklib` | youmilab plotnine_ggplot.ipynb, visual_minnesota | week 13 |
| Plotly | `px.line`, `update_layout`, `update_traces`, `scatter_matrix`, `imshow`, `choropleth`, `scatter_geo`, `sunburst`, `facet_col`, `animation_frame`, `px.data.*` | youmilab plotly.ipynb | week 13 |
| seaborn | `sns.countplot / boxplot / histplot / scatterplot(hue=)`, `sns.load_dataset` | youmilab matplotlib, pandas1, myocardial | not in your scope list; skip |
| statsmodels | `smf.ols('y ~ x', data).fit().summary()`, `.params`, `sm.add_constant`, `sm.OLS` | youmilab statsmodels.ipynb | **excluded** (not requested in decision 3) |
| Dash | `dash.Dash`, `html.Div/H1/P`, `dcc.Graph`, `app.run()`, `@app.callback(Output, Input)`, `dcc.Dropdown`, `dcc.RangeSlider`, `dcc.Input` | youmilab dash_basics, dash_callback | **excluded** (not requested in decision 3; a Dash example cannot show real output beyond the server banner) |
| Functions | `global` keyword; predicate/helper functions | youmilab functions, functions_calling_other_functions | fold into `python/scope` gotcha |
| Recursion | `fibonacci_robust` edge cases, `RecursionError` | youmilab recursion.ipynb | fold into `python/recursion` gotcha |
| Testing | assert-method table (`assertIs`, `assertIsNone`, `assertIsInstance`…), equivalence classes | youmilab unit_test_notes.md | fold into `python/unittest-assert-methods` |
| Shell | `less`, `nano`, `diff` | youmilab shell_warmup.md | listed as optional in §5.3 |

---

## 9. Items intentionally out of scope

- Figures (`*.png`, `*.jpg`), datasets (`*.csv`, `*.txt`, `*.json` data files, `*.pkl`), `*.zip` archives, `LICENSE`, `.gitignore` files, `lecture_notes_template.ipynb` (empty template), `roadmap.md` (ordering only), `hudm5001_semester_project_guidelines.md` (no syntax), `class_anouncement.docx` (announcements only), `group_project_browse_data.md` / `get_and_read_coffee_data.md` / `dl_work_w_constants_file.md` (warm-ups whose only new construct is `np.loadtxt`, listed in §8 as skip).
- Everything in `hudm5001_youmilab/lecture_notes/python/` that duplicates a mini or class_notes topic is cited only as a secondary source.

---

## 10. Open questions — answered 2026-09-04

1. Week 0 → **folded into week 1.**
2. Week 1 / week 2 split of mini 01 → **yes.**
3. Visualization at week 13 → **yes.** statsmodels / Dash → not requested; excluded.
4. Markdown section → **keep**, now sourced from `Week_01_Colab_Markdown_Python.ipynb`.
5. SQL constructs from the SQL page → **include the beginner-common ones**: `DISTINCT`, `IS NULL` / `IS NOT NULL`, `HAVING`; `PRIMARY KEY` / `NOT NULL` folded into `CREATE TABLE`; `CHECK` dropped.
6. `extra` rows → no removals requested; all kept and tagged.
7. Entry count → no reduction requested.

## 11. Decisions log

| Date | Decision |
|---|---|
| 2026-09-04 | Inventory approved with the answers above. `HUDM_5001_2026FALL/` added as the top-priority source; week labels taken from its README (syllabus v08.31.2026). |

## 12. Build status — 2026-09-04

All entries are built and every output on the page was produced by running the example (see `HOWTO.md` for the verifier and the environment).

| Language | Topics | Entries | `extra` |
|---|---|---|---|
| Python | 16 | 208 | 9 |
| SQL | 5 | 24 | 3 |
| Shell | 5 | 34 | 0 |
| Git | 4 | 23 | 1 |
| Markdown | 1 | 13 | 0 |
| Workflow tab | 5 | 23 | 0 |
| **Total** | **36** | **325** | **13** |

Entries per week: wk 1: 45, wk 2: 30, wk 3: 23, wk 4: 17, wk 5: 54, wk 6: 26, wk 7: 17, wk 9: 55, wk 10: 11, wk 11: 17, wk 12: 4, wk 13: 25.

Flags: `no_run` 32, `volatile` 22, `expect_error` 10, `figure` 19, `manual_run` 1.

Verification environment: conda env `hudm5001-verify` (Python 3.13.15, pandas 2.2.3, numpy 2.5.2, matplotlib 3.11.1, plotnine 0.15.8, plotly 6.9.0), sqlite3 3.53.2, git 2.55.0, bash on macOS. Python examples run as Colab-style cells; shell and git examples run in a fresh `~/hudm5001` folder shown as `/Users/student`.

### 12.1 Differences from the approved inventory

Ids listed above but not built (4): `markdown/checklist` (task-list checkboxes; not in the Week 1 notebook), `shell/less-nano-diff` (built as `shell/diff`; `less` and `nano` are interactive and have no capturable output), `shell/environment-yml` and `shell/ipykernel-install` (optional setup rows; the setup that was kept is `shell/conda-create`, `shell/conda-install`, `shell/conda-env-commands`, `shell/vscode-select-interpreter`). Add any of them later by following `HOWTO.md`.

Ids built but not listed above (1): `shell/diff`, the replacement for `shell/less-nano-diff`.

### 12.2 `extra` entries for review

| Id | Week | Title | Source |
|---|---|---|---|
| `git/diff` | 9 | git diff — what exactly changed | hudm5001/class_notes/02_github_version_control.ipynb §2.5 (mentioned) |
| `python/builtin-sum-min-max` | 2 | sum(), min(), max() on a list | hudm5001_mini/05_Control_Structures_Iterables.ipynb §2.5; hudm5001/class_notes/09_classes.ipynb Exercise 2 |
| `python/import-math-random` | 7 | The math and random modules | hudm5001_youmilab/lecture_notes/python/functions_calling_other_functions.ipynb |
| `python/mask-sum-count` | 3 | Count matches: (arr > 100).sum() | hudm5001_mini/assignment_solutions/02 C1, C3, C4; 03 C2; 05 C2 |
| `python/nested-list` | 2 | Nested lists: a list of lists | hudm5001_mini/assignment/01_Python_Quick_Start_Assignment.ipynb C2 |
| `python/series-to-array` | 4 | Series → array or list: .values, np.array(), .to_list() | hudm5001_mini/03_Pandas.ipynb §2.2; assignment_solutions 02 C4 |
| `python/set-from-list` | 2 | set(list) — de-duplicate a list | hudm5001_mini/assignment_solutions/01 C4 and 02 C4 |
| `python/str-capitalize-map` | 12 | .str.capitalize() and .map(dict) on a column | hudm5001/class_notes/11_coding_practices_with_ai.ipynb Exercise 2 solution |
| `python/str-isdigit` | 7 | str.isdigit() — is this text all digits? | hudm5001/class_notes/08_functions_lambdas_comprehensions.ipynb Exercise 3 |
| `python/sys-argv` | 11 | sys.argv — command-line arguments | hudm5001_youmilab/programming_assignments/python/fibonacci_from_cmd_line.md; hudm5001/class_notes/00_environment_setup.md §7.2 |
| `sql/distinct` | 5 | SELECT DISTINCT — unique values | Class_asset/why_sql_not_excel.html |
| `sql/having` | 5 | HAVING — filter the groups | Class_asset/why_sql_not_excel.html |
| `sql/is-null` | 5 | IS NULL / IS NOT NULL — find missing values | Class_asset/why_sql_not_excel.html |

### 12.3 Additions on 2026-09-04 (evening)

- Git gained a topic **Start your own project** (`git-start`): `git/init`, `git/gitignore`, `git/github-new-repo`, `git/gh-repo-create` (the GitHub CLI route), `git/remote-add-origin`, `git/branch`, `git/pull-request`. The push/clone examples talk to a local bare repository that stands in for GitHub (git's `url.<base>.insteadOf` rewrite), so the commands shown are exactly the ones a student types.
- All terminal install commands use `python -m pip …` instead of a bare `pip …` (decision 2026-09-04: pip on the PATH may belong to another Python); Colab cells keep `!pip`.
- A sixth tab, **A standard workflow** (`workflow.json`, 23 steps in five parts), walks the miniGPT build guide from an empty folder with conda (not venv) and unittest (not pytest): every step shows the files it writes, the commands, a line-by-line explanation, and the real output of running the steps in order inside one sandbox. The 5,000-iteration training run is recorded once (`manual_run`) rather than repeated. Sources: `_dev/workflow/` (builder, project files, recorded run); environment `minigpt-verify` (Python 3.12, torch).

