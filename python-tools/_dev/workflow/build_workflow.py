"""Build python-tools/data/workflow.json for the "A standard workflow" tab.

Reads the miniGPT project files from project/, the recorded full training run from
recorded/ (train.log, sample.txt, log.csv) when present, and carries verified outputs
forward from the existing workflow.json. Run it from anywhere:
    python3 python-tools/_dev/workflow/build_workflow.py
then record outputs with verify.py --write --lang workflow.
"""
import json, math, pathlib, csv

S = pathlib.Path(__file__).resolve().parent
PROJ = S / "project"
OUT = S.parent.parent / "data" / "workflow.json"
REC = S / "recorded"
GUIDE = "HUDM 5001 advanced track, “Building a miniGPT from an empty folder” (build guide)"

LANGS = {".py": "python", ".toml": "toml", ".yaml": "yaml", ".md": "markdown", ".csv": "text"}


def F(path, content=None):
    p = PROJ / path
    return {"path": path, "content": (content if content is not None else p.read_text(encoding="utf-8")).rstrip("\n") + "\n",
            "lang": LANGS.get(pathlib.Path(path).suffix, "text")}


# ---- the recorded full run (optional) -------------------------------------------------
train_log = (REC / "train.log").read_text(encoding="utf-8").strip() if (REC / "train.log").exists() else ""
sample = (REC / "sample.txt").read_text(encoding="utf-8").rstrip() if (REC / "sample.txt").exists() else ""
log_csv_path = REC / "log.csv"
log_csv = log_csv_path.read_text(encoding="utf-8").strip() if log_csv_path.exists() else ""
best_val, minutes = None, None
if log_csv:
    rows = list(csv.DictReader(log_csv.splitlines()))
    if rows and "val_loss" in rows[0]:
        best_val = min(float(r["val_loss"]) for r in rows)
        minutes = float(rows[-1]["seconds"]) / 60
full_run_done = bool(train_log and sample and log_csv and best_val is not None and "best validation loss" in train_log)
if full_run_done:
    r0, r250, rlast = rows[0], next(r for r in rows if int(r["iter"]) == 250), rows[-1]
    rbest = min(rows, key=lambda r: float(r["val_loss"]))
    CURVE = [[f"iter 0 · train {float(r0['train_loss']):.2f} · val {float(r0['val_loss']):.2f}", "Untrained: within a few hundredths of ln(65) = 4.17 (the extra comes from the random initial weights). If it is 6 or 11, stop and fix the model before spending GPU minutes."],
             [f"iter 250 · val {float(r250['val_loss']):.2f}, already below 2.48", "After 250 iterations the transformer has overtaken the counting baseline. Everything after this is refinement."],
             [f"iter {rbest['iter']} · val {float(rbest['val_loss']):.4f}, the best", f"Validation stops improving here while the training loss keeps falling ({float(rlast['train_loss']):.2f} by iteration {rlast['iter']}, with validation back up to {float(rlast['val_loss']):.2f}): from this point the model is memorising the training text. `best.pt` keeps this checkpoint, which is what the sampler loads."],
             [f"best validation loss {best_val:.4f} -> runs/base/best.pt", f"The headline number, in nats. Perplexity exp({best_val:.4f}) = {math.exp(best_val):.1f}, against 12.0 for counting letter pairs and 65 for guessing."],
             ["python -m minigpt.sample ... --temperature 0.8 --seed 0", "Generates 600 characters from the best checkpoint. Below temperature 1.0 the text looks better than the model really is, because its uncertainty is suppressed: report the loss at 1.0, and say which temperature produced any sample you show."]]
else:
    CURVE = [["iter 0 · train 4.18 · val 4.18", "Untrained: the same ln(65) as step 12."],
             ["passing 2.48", "The moment the transformer overtakes the counting baseline."],
             ["python -m minigpt.sample ... --temperature 0.8 --seed 0", "Generates 600 characters from the best checkpoint."]]

README_FINAL = """# miniGPT

A character-level GPT trained on tinyshakespeare, built from an empty folder with
the HUDM 5001 standard workflow: environment first, Git second, tests alongside.

## Reproduce

    conda create --name minigpt python=3.12 -y && conda activate minigpt
    python -m pip install -e .
    python scripts/get_data.py && python -c "from minigpt.data import build_arrays; build_arrays()"
    python -m minigpt.train --config configs/base.yaml --run-name base

## Results

| model               | val loss | perplexity |
|---------------------|----------|------------|
| uniform (untrained) |  4.174   |   65.0     |
| counting bigram     |  2.482   |   12.0     |
| miniGPT 10.8M       |  %s   |   %s     |
""" % ((f"{best_val:.3f}", f"{math.exp(best_val):.1f}") if best_val else ("~1.5", "~4.5"))

TOPICS = [
    {"id": "wf-setup", "label": "Part I · Set up the workspace"},
    {"id": "wf-data", "label": "Part II · Data"},
    {"id": "wf-models", "label": "Part III · Models"},
    {"id": "wf-run", "label": "Part IV · Train, evaluate, test"},
    {"id": "wf-ship", "label": "Part V · Ship it"},
]

UNITTEST_LINE = ["python -m unittest discover -s tests -v",
                 "Finds every `test_*.py` file under `tests/` and runs it; `-v` prints one line per test. `OK` at the end is what you want; the time it reports varies."]

E = []


def add(**kw):
    kw.setdefault("source", GUIDE)
    kw.setdefault("output", "")
    E.append(kw)


# ============================ Part I · Set up the workspace ============================
add(id="workflow/00-the-plan", title="Step 0 · The plan, and five rules that prevent predictable failures", topic="wf-setup", week=9,
    no_run=True, code_lang="text",
    summary="Every Python project follows the same spine: folder → environment → Git → package scaffold → data → code with tests → run and log → ship. This tab walks it once, building a small character-level GPT from an empty folder, so you can copy the sequence for your own project. Each step shows the exact commands, what every line does, and the real output.",
    example=("Part I    Set up    1 folder · 2 conda env · 3 check · 4 git init\n"
             "                    5 GitHub repo · 6 connect · 7 scaffold\n"
             "Part II   Data      8 download script · 9 clean · 10 tokenizer · 11 split & batch\n"
             "Part III  Models    12 baseline · 13 config · 14 transformer\n"
             "Part IV   Run       15 smoke run · 16 full run · 17 evaluate · 18 test suite\n"
             "Part V    Ship      19 Colab · 20 branches · 21 pull request · 22 README"),
    lines=[["Environment before Git", "Create the conda environment and install the packages first, so the very first commit already records what the code needs to run. A repository whose first commit cannot be installed is one nobody can reproduce."],
           [".gitignore before the first commit", "Commit a 1 MB data file once and it lives in the history forever. Ignore rules go in before anything is staged."],
           ["A walking skeleton before the real model", "Get a tiny model running end to end in seconds, then scale up. Otherwise your first debugging session and your first long training run happen at the same time, and you will not know which is broken."],
           ["A baseline before the neural network", "Thirty lines of counting give you a number to beat. Without it, “my loss is 2.1” means nothing; with it you know 2.1 is worse than counting letter pairs."],
           ["Tests alongside, not at the end", "Every module gets its test in the same sitting. Unit tests (does the code do what I said) and evaluation (is the model any good) are different jobs and live in different folders."]],
    gotcha="The order matters more than the tools. With venv instead of conda, or pytest instead of unittest, the spine is exactly the same.",
    related=["shell/conda-create", "git/init", "python/unittest-testcase", "workflow/01-project-folder"],
    keywords=["project", "workflow", "from scratch", "empty folder", "checklist", "plan"],
    source=GUIDE + ", “Changes to the original plan”")

add(id="workflow/01-project-folder", title="Step 1 · Make the project folder", topic="wf-setup", week=1,
    summary="One folder holds everything: code, tests, configuration and the (ignored) data. Create it somewhere you can find again and move into it; every command in this workflow is typed from inside this folder.",
    example="mkdir minigpt\ncd minigpt\npwd",
    lines=[["mkdir minigpt", "Makes a new, empty folder named `minigpt` inside the folder you are in (here the home folder)."],
           ["cd minigpt", "Moves into it. The prompt does not always show it, so the next line checks."],
           ["pwd", "Prints the working directory: the full path of the folder you are in."]],
    gotcha="Short, lowercase, no spaces or hyphens: `minigpt`, not `My GPT Project`. The folder name becomes the package name in step 7, and Python cannot import a name with a space or a dash.",
    related=["shell/mkdir", "shell/cd", "shell/pwd", "shell/file-naming"],
    keywords=["mkdir", "new project", "folder"], source=GUIDE + ", step 1")

add(id="workflow/02-conda-env", title="Step 2 · Create an isolated conda environment", topic="wf-setup", week=1, no_run=True,
    summary="An environment is a private Python installation that belongs to this project only. Create it with conda, turn it on with `conda activate`, then install the project's packages with pip. From now on everything you install lands here and nowhere else, and “somewhere else” is never your system Python.",
    example="conda create --name minigpt python=3.12 -y\nconda activate minigpt\npython -m pip install torch numpy pandas pyyaml matplotlib",
    output_note="conda lists what it will install and continues without asking because of `-y`. When activation works, your prompt starts with `(minigpt)` instead of `(base)`. That prefix is the single most useful signal in the whole project: if it says `(base)`, you are about to install into your Anaconda installation instead of your project.",
    lines=[["conda create --name minigpt python=3.12 -y", "Makes a new environment called `minigpt` with its own Python 3.12. `--name` gives it a name, `python=3.12` pins the version (the course default, and a version every package supports), `-y` answers “yes” to the confirmation question."],
           ["conda activate minigpt", "Turns the environment on for this terminal window. Do it every time you open a new terminal to work on the project; the `(minigpt)` prefix tells you it worked."],
           ["python -m pip install torch numpy pandas pyyaml matplotlib", "Installs the packages into the active environment: PyTorch for the model, NumPy and pandas for arrays and tables, PyYAML to read the config files, matplotlib for plots. `python -m pip` (rather than a bare `pip`) runs the pip that belongs to this `python`: a bare `pip` is whichever pip is first on the PATH, which on a computer with Anaconda plus a system Python is not always the same one, and then packages land where `import` cannot find them."]],
    gotcha="Use conda to create the environment and choose the Python version; use `python -m pip` for everything inside it, and do not run `conda install` afterwards: conda does not know what pip installed and can overwrite it, and the environment fails later on an import with an error that points nowhere. If an environment breaks, do not repair it: `conda deactivate`, `conda env remove --name minigpt -y`, and create it again in thirty seconds. Nothing of value lives inside one; your code is in Git and your data is regenerable.",
    related=["shell/conda-create", "shell/conda-activate", "shell/pip-install", "shell/conda-env-commands"],
    keywords=["conda create", "activate", "virtual environment", "venv", "pip install", "python -m pip"], source=GUIDE + ", step 1")

add(id="workflow/03-check-env", title="Step 3 · Check that the right Python is active", topic="wf-setup", week=1,
    summary="Before writing anything, prove that the terminal is using the environment you just made. Four commands answer four questions: which version, which `python` file, which pip goes with it, and do the packages import.",
    example="python -V\nwhich python\npython -m pip --version\npython -c \"import torch; print(torch.__version__, torch.backends.mps.is_available())\"",
    output_note="Recorded on an Apple-silicon Mac, so the GPU check prints `True`. On Windows or Linux without an NVIDIA card it prints `False`, and on Colab the check that prints `True` is `torch.cuda.is_available()`. All of these are fine: step 13 picks the device automatically.",
    lines=[["python -V", "Prints the version. It must say 3.12, the version you pinned in step 2."],
           ["which python", "Prints the path of the `python` command this terminal runs. The path must contain `envs/minigpt`; if it says `base` or `/usr/bin`, the environment is not active. On Windows use `where python`."],
           ["python -m pip --version", "Runs pip as a module of that same `python` and prints where it lives. The path must also contain `envs/minigpt`: this is the pip that step 2 installed into, and the one every `python -m pip install` will use."],
           ["python -c \"import torch; print(...)\"", "`-c` runs the quoted code without a file. Importing torch proves the install worked; the second value says whether the Apple GPU (MPS) can be used."]],
    gotcha="If a package imports in the terminal but not in VS Code, VS Code is using a different Python: open the Command Palette, run “Python: Select Interpreter” and choose `minigpt`, then restart the kernel.",
    related=["shell/vscode-select-interpreter", "shell/python-dash-c", "python/verify-setup", "shell/conda-activate"],
    keywords=["which python", "python -V", "interpreter", "wrong environment"], source=GUIDE + ", step 1 checkpoint")

add(id="workflow/04-git-init", title="Step 4 · git init, ignore first, commit second", topic="wf-setup", week=9,
    summary="Turn the folder into a Git repository, write the ignore rules and a README, and make the first commit. The order matters: Git history is append-only in practice, so anything large or private must be ignored before it is ever staged.",
    files=[F(".gitignore"), F("README.md")],
    example="git init\ngit add .gitignore README.md\ngit commit -m \"Initialise repository with ignore rules\"\ngit status",
    lines=[[".gitignore: .venv/  __pycache__/  *.egg-info/", "Folders Python and pip create while you work. They are regenerated every time and belong to your machine, not to the project."],
           [".gitignore: data/  checkpoints/  runs/  *.pt  *.npy", "Everything regenerable from code: the downloaded corpus, cached arrays, trained weights, training logs. A collaborator should rebuild them by running your scripts, not download them from your repository. Rule of thumb: commit the recipe, never the result."],
           [".gitignore: .ipynb_checkpoints/  .DS_Store", "Notebook autosaves and macOS folder metadata: pure noise in a diff."],
           ["README.md", "One paragraph for now: what the project is. Step 22 turns it into a real README with reproduce instructions and results."],
           ["git init", "Creates the hidden `.git` folder that will store every snapshot. Run once per project."],
           ["git add .gitignore README.md", "Stages exactly these two files. Naming them instead of `git add .` is a habit that keeps surprises out of the first commit."],
           ["git commit -m \"Initialise repository with ignore rules\"", "Saves the snapshot with a message. The output names the branch, the new commit id, and the files it contains."],
           ["git status", "“nothing to commit, working tree clean” means every tracked file is saved. You will see this line a lot."]],
    gotcha="Write ignore rules for things that do not exist yet (`runs/`, `*.pt`). The point is that they never get the chance to be staged.",
    related=["git/init", "git/gitignore", "git/add", "git/commit", "git/status", "markdown/headings"],
    keywords=["git init", "gitignore", "first commit", "readme"], source=GUIDE + ", step 2")

add(id="workflow/05-github-repo", title="Step 5 · Create an empty repository on GitHub", topic="wf-setup", week=9, no_run=True, code_lang="text",
    harness='git init -q --bare "$HOME/github/minigpt.git"',
    summary="GitHub is where the project lives outside your laptop: backup, sharing, and later Colab. Create the repository completely empty, so the history starts on your computer and GitHub simply receives it. Two ways to do it, same result: click through the website (A), or one command with the GitHub CLI (B). Either way, step 6 is next.",
    example=("A · In the browser\n"
             "github.com → \"+\" (top right) → New repository\n"
             "  Repository name:  minigpt           ← the same name as your folder\n"
             "  Visibility:       Public or Private\n"
             "  Leave UNTICKED:   Add a README, Add .gitignore, Choose a license\n"
             "→ Create repository\n"
             "\n"
             "B · In the terminal, with the GitHub CLI\n"
             "conda install -c conda-forge gh        # one time (a Mac can also use: brew install gh)\n"
             "gh auth login                          # one time per computer: GitHub.com → HTTPS → Login with a web browser\n"
             "gh repo create minigpt --private       # or --public\n"
             "gh repo view minigpt --web             # optional: open the new page to check"),
    output_note="Route A ends on a page with a box titled “…or push an existing repository from the command line”; its three commands are step 6. Route B prints the address of the new repository, `https://github.com/<your-username>/minigpt`. Neither is recorded here because both need your GitHub account.",
    lines=[["A · Repository name", "Use the folder name so the URL and the folder match: `github.com/<your-username>/minigpt`."],
           ["A · Leave the three boxes unticked", "You already have a README and a .gitignore from step 4. Ticking a box makes GitHub create a first commit that your computer does not have, and your first push is rejected."],
           ["A · Create repository", "Nothing is uploaded yet. The repository is an empty shell waiting for `git push`."],
           ["B · conda install -c conda-forge gh", "Installs the GitHub CLI into the `minigpt` environment. `gh` is a separate program from `git`: git manages your history, gh talks to the GitHub website for you."],
           ["B · gh auth login", "A one-time login per computer. Answer the questions (GitHub.com, HTTPS, Yes, Login with a web browser), copy the one-time code it shows, press Enter, paste the code on the GitHub page that opens. From now on `git push` never asks for a password: gh stored a token that git reuses."],
           ["B · gh repo create minigpt --private", "Creates an empty repository named `minigpt` under your account. `--private` or `--public` is required in this form; with no name and no flag, `gh repo create` asks questions instead. Nothing is uploaded and no README is added, so it matches route A exactly."],
           ["B · gh repo view minigpt --web", "Opens the repository page in your browser, the quickest check that it exists."],
           ["B · the one-command shortcut, for later", "`gh repo create minigpt --private --source=. --remote=origin --push`, run inside the project folder, does steps 5 and 6 together: creates the repository, adds it as `origin`, and pushes. Learn the two-step version first so you know what it does."]],
    gotcha="If you did tick “Add a README” (route A) or added `--add-readme` (route B), the simplest fix is to delete the repository on GitHub (Settings → Danger zone) and create it again empty.",
    related=["git/github-new-repo", "git/gh-repo-create", "git/git-vs-github", "git/personal-access-token", "workflow/06-connect-and-push"],
    keywords=["github", "new repository", "create repo"], source=GUIDE + ", step 2")

add(id="workflow/06-connect-and-push", title="Step 6 · Connect the folder to GitHub and push", topic="wf-setup", week=9,
    summary="Copy the three commands GitHub printed. They tell Git the address of the remote copy, name the branch `main`, and upload the first commit while remembering the link, so that later pushes are just `git push`.",
    example="git remote add origin https://github.com/YOUR-USERNAME/minigpt.git\ngit branch -M main\ngit push -u origin main",
    output_note="Replace `YOUR-USERNAME` with your GitHub user name. On your machine the output names your GitHub URL; in this recorded run a local folder stands in for GitHub, so the output names that folder instead.",
    lines=[["git remote add origin https://github.com/YOUR-USERNAME/minigpt.git", "`origin` is the conventional nickname for your GitHub copy. The URL is the one on the empty-repository page (or the green **Code** button, HTTPS tab)."],
           ["git branch -M main", "Renames the current branch to `main`; older Git versions start on `master`. `-M` renames even if `main` already exists."],
           ["git push -u origin main", "Uploads your commits. `-u` records that local `main` follows `origin/main`, so plain `git push` and `git pull` work from now on. The output ends with the branch tracking line."],
           ["If you used the gh shortcut in step 5", "`gh repo create … --source=. --remote=origin --push` already did all three lines; run `git remote -v` and you will see `origin` pointing at GitHub. Skip to step 7."]],
    gotcha="GitHub does not accept your account password over HTTPS. When asked for a password, paste a personal access token, or sign in once through GitHub Desktop or the `gh` command-line tool.",
    related=["git/remote-add-origin", "git/gh-repo-create", "git/push", "git/personal-access-token", "git/remote"],
    keywords=["remote add origin", "push -u", "first push", "connect github", "gh"], source=GUIDE + ", step 2")

add(id="workflow/07-scaffold", title="Step 7 · Scaffold the package and install it in editable mode", topic="wf-setup", week=9,
    summary="Create the folder layout the project will grow into, describe the package in `pyproject.toml`, and install it with `pip install -e .` so that `import minigpt` works from anywhere on your machine and always points at your source folder. Make all the folders now, even the empty ones: an empty `tests/` that is waiting for you is worth more than a perfect one you meant to create later.",
    files=[F("pyproject.toml")],
    example=("mkdir -p src/minigpt tests configs scripts notebooks data checkpoints\n"
             "touch src/minigpt/__init__.py\n"
             "python -m pip install -q -e .\n"
             "python -m pip show minigpt\n"
             "cd ..\n"
             "python -c \"import minigpt; print(minigpt.__file__)\"\n"
             "cd minigpt\n"
             "git add pyproject.toml src\n"
             "git commit -m \"Scaffold the package\""),
    lines=[["mkdir -p src/minigpt tests configs scripts notebooks data checkpoints", "Seven folders at once; `-p` creates parents and does not complain if one exists. `src/minigpt/` is the importable package where all real code lives; `tests/` mirrors it; `configs/` holds YAML settings; `scripts/` one-off jobs; `notebooks/` thin demos; `data/` and `checkpoints/` are ignored by Git."],
           ["touch src/minigpt/__init__.py", "Creates an empty file. Its presence tells Python that `src/minigpt` is a package."],
           ["pyproject.toml: [build-system]", "Which tool builds the package (setuptools). Boilerplate you copy between projects."],
           ["pyproject.toml: [project]", "Name, version, the Python range it supports, and the packages it depends on. pip reads this list."],
           ["pyproject.toml: [tool.setuptools.packages.find] where = [\"src\"]", "Tells setuptools that packages live under `src/`. This “src layout” makes it impossible to import a half-written package from the current folder by accident."],
           ["python -m pip install -q -e .", "Installs the package from the current folder (`.`) in editable mode (`-e`): Python records a link to `src/`, so every edit is live with no reinstall. `python -m pip` guarantees it is this environment's pip (step 3 checked that); `-q` hides the long list of `Requirement already satisfied` lines, the packages from step 2."],
           ["python -m pip show minigpt", "Proves the install: the version from `pyproject.toml`, `Editable project location` pointing at your folder, and `Requires` listing the dependencies."],
           ["cd .. / python -c \"import minigpt; print(minigpt.__file__)\" / cd minigpt", "The test that matters: import from a folder that is *not* the project. The printed path must end in `src/minigpt/__init__.py`. Then go back into the project."],
           ["git add pyproject.toml src / git commit", "Commits the scaffold. The `src/minigpt.egg-info/` folder that the install created is ignored by the `*.egg-info/` rule."]],
    gotcha="`ImportError: minigpt` later on has two usual causes: the environment is not activated (the prompt says `(base)`), or `python -m pip install -e .` was never run in this environment. A bare `pip install -e .` that used another Python's pip is the sneaky third cause; `python -m pip show minigpt` settles it.",
    related=["shell/mkdir", "shell/touch", "shell/pip-install", "python/import-module", "python/name-main"],
    keywords=["pyproject", "pip install -e", "python -m pip", "editable", "src layout", "package", "scaffold"], source=GUIDE + ", step 3")

# ============================ Part II · Data ============================
add(id="workflow/08-download-script", title="Step 8 · Fetch the data with a script, not by hand", topic="wf-data", week=3,
    summary="Downloading a file by hand is fine exactly once and then becomes the thing nobody can reproduce. A twenty-line script downloads the corpus, checks its size and fingerprint, and is safe to run again. The corpus is tinyshakespeare: 1.1 MB of plays, one character at a time.",
    files=[F("scripts/get_data.py")],
    example="python scripts/get_data.py\npython scripts/get_data.py\ngit status --short\ngit add scripts/get_data.py\ngit commit -m \"Add the data download script\"",
    lines=[["import hashlib, urllib.request, from pathlib import Path", "Standard library only: hashing, downloading, and paths. Nothing to install."],
           ["URL, DEST, EXPECTED_BYTES", "Three constants at the top: where the file comes from, where it goes, how big it must be. For another dataset you change these, not the code."],
           ["DEST.parent.mkdir(parents=True, exist_ok=True)", "Creates `data/` if needed and does not fail if it already exists."],
           ["if not DEST.exists(): ... urlretrieve(URL, DEST)", "Downloads only when the file is missing, so the second run costs nothing."],
           ["digest = hashlib.sha256(raw).hexdigest()[:12]", "A fingerprint of the bytes. If it changes later, the data changed, not your code; three lines that settle arguments."],
           ["if len(raw) != EXPECTED_BYTES: raise SystemExit(...)", "Stops with a message instead of continuing with a wrong file."],
           ["if __name__ == \"__main__\": main()", "Runs `main()` only when the file is executed as a script, not when it is imported."],
           ["python scripts/get_data.py  (twice)", "The first run downloads and reports; the second only reports: same size, same fingerprint."],
           ["git status --short", "Shows `?? scripts/` (untracked, new) and nothing about `data/`: the ignore rule from step 4 is doing its job."]],
    gotcha="If `git status` lists `data/input.txt`, your `.gitignore` is missing the `data/` line or has a typo. Fix it before you commit.",
    related=["python/os-path", "python/open-read", "python/name-main", "python/run-script", "git/gitignore", "shell/wget"],
    keywords=["download", "urllib", "dataset", "sha256", "reproducible"], source=GUIDE + ", step 4")

add(id="workflow/09-clean", title="Step 9 · Clean the text, and write the test in the same sitting", topic="wf-data", week=3, volatile=True,
    summary="Cleaning is a list of explicit decisions about what you will and will not model, written as code so you can still see them in six weeks: normalise Unicode, flatten curly quotes, unify line endings, collapse repeated spaces and blank lines. The test checks a property (cleaning twice changes nothing) rather than one exact output.",
    files=[F("src/minigpt/clean.py"), F("tests/test_clean.py"), F("scripts/inspect_corpus.py")],
    example="python scripts/inspect_corpus.py\npython -m unittest discover -s tests -v\ngit add src tests scripts\ngit commit -m \"Add the corpus cleaner and its tests\"",
    lines=[["unicodedata.normalize(\"NFKC\", raw)", "Turns look-alike characters into one standard form (full-width letters, odd spaces), so the model does not learn two spellings of the same thing."],
           ["for bad, good in SMART.items(): text = text.replace(bad, good)", "Replaces curly quotes and long dashes with their plain keyboard versions, one pair at a time."],
           ["text.replace(\"\\r\\n\", \"\\n\").replace(\"\\r\", \"\\n\")", "Windows and old-Mac line endings become plain `\\n`."],
           ["re.sub(r\"[ \\t]+\", \" \", text)", "A regular expression: one or more spaces or tabs become a single space."],
           ["re.sub(r\"\\n{3,}\", \"\\n\\n\", text)", "Three or more line breaks in a row become two: at most one blank line."],
           ["text.strip() + \"\\n\"", "No leading or trailing whitespace, and exactly one newline at the end."],
           ["describe(text)", "Returns the counts you want to print: characters, lines, vocabulary size, the five most common characters."],
           ["test_cleaning_twice_changes_nothing", "The most valuable cleaner test: `clean(clean(x)) == clean(x)`. If cleaning twice differs from cleaning once, two of your rules are fighting."],
           ["scripts/inspect_corpus.py", "Prints the before-and-after numbers. Only twenty characters were removed and the vocabulary stayed at 65: correct for a corpus that was already tidy."],
           UNITTEST_LINE],
    output_note="If your cleaner deletes thousands of characters or changes the vocabulary size, one rule is too aggressive: go and find out which.",
    gotcha="Test the property, not the output. A test that pins the exact cleaned text of a whole file breaks the moment you improve one rule, and tells you nothing when it does.",
    related=["python/str-methods", "python/str-replace", "python/unittest-testcase", "python/unittest-run-notebook", "python/import-module"],
    keywords=["clean", "normalize", "regex", "unicode", "idempotent", "unittest"], source=GUIDE + ", step 5")

add(id="workflow/10-tokenizer", title="Step 10 · Write the tokenizer: a class with a round-trip test", topic="wf-data", week=10, volatile=True,
    summary="A tokenizer maps text to integers and back. For a character-level model it is genuinely this small, and writing it yourself removes most of the mystery from the word “tokenization”. Five tests, and the round trip is the one that really matters.",
    files=[F("src/minigpt/tokenizer.py"), F("tests/test_tokenizer.py")],
    example=("python -c \"from minigpt.tokenizer import CharTokenizer; tok = CharTokenizer.from_text('hello'); print(tok.chars, tok.encode('hello'), tok.decode([1, 2]))\"\n"
             "python -m unittest discover -s tests -v\n"
             "git add src tests\n"
             "git commit -m \"Add the character tokenizer and its tests\""),
    lines=[["class CharTokenizer: def __init__(self, chars)", "The vocabulary is a list of characters. `stoi` (string to int) and `itos` (int to string) are two dictionaries built from it; a duplicate character is refused with a clear error."],
           ["@classmethod def from_text(cls, text)", "A second way to build one, from the text itself: `sorted(set(text))` is every distinct character in a fixed order."],
           ["@property def vocab_size(self)", "A method you read like an attribute: `tok.vocab_size`, no parentheses."],
           ["encode / decode", "Lists of integers from text and back. `encode` turns a missing character into a clear `ValueError` instead of a `KeyError` deep inside a loop."],
           ["save / load", "The vocabulary is written to JSON and read back. A saved model is useless without its tokenizer, so this file ships with every checkpoint."],
           ["python -c \"... CharTokenizer.from_text('hello') ...\"", "A concrete look: `hello` has four distinct characters, so `encode` gives numbers 0–3 and `decode([1, 2])` returns `hl`."],
           ["test_roundtrip_is_lossless", "`decode(encode(text)) == text`. If this fails, nothing else matters."],
           ["test_save_and_load", "Uses `tempfile.TemporaryDirectory()` so the test never writes into your project folder. A test that touches `data/` passes the first time and fails the second, and the reason is never obvious."],
           UNITTEST_LINE],
    gotcha="The numbering comes from the text the tokenizer was built on. Build it once on the cleaned corpus (step 11 saves it), and load that file everywhere else; rebuilding it on different text silently renumbers the characters.",
    related=["python/class", "python/init", "python/self", "python/dict", "python/json-dump-load", "python/unittest-assert-methods"],
    keywords=["tokenizer", "encode", "decode", "vocabulary", "class", "classmethod", "property"], source=GUIDE + ", step 6")

add(id="workflow/11-split-batch", title="Step 11 · Split the data and produce training batches", topic="wf-data", week=7,
    summary="Two jobs: hold out a validation slice you never train on, and turn the integer array into batches of (context, next character) pairs. The second is where most beginners write their first off-by-one bug, so a small script prints one pair for you to read.",
    files=[F("src/minigpt/data.py"), F("scripts/check_batch.py")],
    example=("python -c \"from minigpt.data import build_arrays; build_arrays()\"\n"
             "python scripts/check_batch.py\n"
             "ls data\n"
             "git add src scripts\n"
             "git commit -m \"Add the split-and-batch code\""),
    lines=[["build_arrays(src, out_dir, val_frac=0.1)", "Reads the raw file, cleans it, builds the tokenizer, encodes the whole corpus as one `uint16` array (65 values fit easily), and splits it 90/10 by position."],
           ["np.save(out / \"train.npy\", ids[:n])", "Caches the arrays as `.npy` files so later steps load in milliseconds instead of re-cleaning. Both are ignored by Git."],
           ["tok.save(out / \"vocab.json\")", "The tokenizer is saved next to the arrays; sampling in step 17 loads it."],
           ["get_batch(split_array, block_size, batch_size, device, generator=None)", "Picks `batch_size` random start positions, cuts `block_size` characters from each for `x`, and the same window moved one character to the right for `y`."],
           ["x = data[i : i + block_size]   y = data[i + 1 : i + block_size + 1]", "The one line to get right: position t of `x` is asked to predict position t of `y`, the character that actually came next. Every position in the block is a training example, which is why transformers train efficiently."],
           ["python scripts/check_batch.py", "Prints one `x` and its `y` (seeded, so it reproduces). The second string must be the first moved one character along; if it is not, fix it now, because this bug is nearly invisible later and quietly caps the model's quality."],
           ["ls data", "Four files: the raw text, two arrays, and the vocabulary."]],
    gotcha="Split by position, not at random. Text is sequential; a random 10% of characters would leak the neighbours of every validation character into training.",
    related=["python/np-index-slice", "python/np-array", "python/return-multiple", "python/np-random"],
    keywords=["train validation split", "batch", "block size", "npy", "off by one"], source=GUIDE + ", step 7")

# ============================ Part III · Models ============================
add(id="workflow/12-baseline", title="Step 12 · Build the dumbest model first: a counting baseline", topic="wf-models", week=6, volatile=True,
    summary="Before any neural network, count how often each character follows each other character, normalise the rows into probabilities, and score the validation text. No PyTorch, no gradients, under a second, and it gives you a number the transformer has to beat.",
    files=[F("src/minigpt/baseline.py"), F("tests/test_baseline.py"), F("scripts/eval_baseline.py")],
    example="python scripts/eval_baseline.py\npython -m unittest discover -s tests\ngit add src tests scripts\ngit commit -m \"Add the counting-bigram baseline\"",
    lines=[["self.counts = np.zeros((vocab_size, vocab_size))", "A 65 × 65 table: row = current character, column = the character that follows."],
           ["np.add.at(self.counts, (ids[:-1], ids[1:]), 1.0)", "Counts every consecutive pair in one vectorised call: `ids[:-1]` are the current characters, `ids[1:]` the next ones."],
           ["probs = (counts + alpha) / row sums", "Turns counts into probabilities per row. `alpha = 1` (add-one smoothing) means no pair is ever impossible; a zero would make the loss infinite."],
           ["nll(ids) = -np.log(p).mean()", "Mean negative log-likelihood in nats, the same unit PyTorch's `cross_entropy` reports, so the two models can be compared directly."],
           ["generate(n, start, seed)", "Samples one character at a time from the row of the current character. Seeded, so it reproduces."],
           ["uniform (untrained)   4.1744 = ln(65)", "A model that knows nothing gives 1/65 to every character; its loss is exactly ln 65. Every model must start here."],
           ["bigram, validation   2.4819   perplexity 11.96", "Counting letter pairs already halves the confusion. Perplexity is `exp(loss)`: “as unsure as choosing among 12 characters”. Write 2.48 on a sticky note; it is the bar."],
           ["tests: uniform when untrained · rows sum to one · fitting lowers the loss", "Three properties that must hold whatever the data. They catch broken smoothing, a wrong axis in the row sum, and a `fit` that does nothing."],
           ["python -m unittest discover -s tests", "Without `-v`: one dot per test, then the count and `OK`."]],
    output_note="These numbers are exact for this corpus. If your bigram lands on 2.48 on the validation split, your cleaning, tokenizer and split are all correct: three components verified by one number.",
    gotcha="Nats, not bits. `np.log` and PyTorch's `cross_entropy` both use the natural logarithm; a `log2` from somewhere else makes the comparison meaningless.",
    related=["python/np-summaries", "python/np-vectorized", "python/class", "python/np-random", "python/unittest-assert-methods"],
    keywords=["baseline", "bigram", "perplexity", "cross-entropy", "nats", "smoothing"], source=GUIDE + ", step 8")

add(id="workflow/13-config", title="Step 13 · Put every knob in one place", topic="wf-models", week=10,
    summary="Every hyperparameter lives in one `Config` object, loaded from a small YAML file. The moment `block_size` is written in three files you will change two of them and spend an hour on the third. Two configs: `tiny.yaml` runs end to end in seconds, `base.yaml` is the real model.",
    files=[F("src/minigpt/config.py"), F("configs/tiny.yaml"), F("configs/base.yaml")],
    example="python -c \"from minigpt.config import Config; print(Config.from_yaml('configs/tiny.yaml'))\"\ngit add src configs\ngit commit -m \"Put every hyperparameter in one Config\"",
    lines=[["def get_device()", "Picks the fastest hardware available: NVIDIA (`cuda`, Colab), Apple GPU (`mps`), otherwise `cpu`. The rest of the code never mentions hardware again."],
           ["@dataclass class Config", "A dataclass turns a list of typed fields with defaults into a class with `__init__`, a readable `repr` and `==` for free. The defaults are the base model."],
           ["def __post_init__(self)", "Runs right after construction: a cheap check (`n_embd` divisible by `n_head`) that turns a twenty-minute shape error deep inside a matrix multiply into a one-line message, and fills in the device."],
           ["Config.from_yaml(path)", "`yaml.safe_load` reads the file into a dict; `cls(**dict)` turns its keys into arguments. Keys that are missing keep their defaults."],
           ["configs/tiny.yaml", "The walking skeleton: 2 layers, 64 dimensions, 100 iterations. It exists so the whole pipeline can run in seconds and tell you whether anything is wired wrong."],
           ["configs/base.yaml", "6 layers, 384 dimensions, 5,000 iterations: about 10.8 million parameters, minutes on a GPU."],
           ["print(Config.from_yaml('configs/tiny.yaml'))", "The dataclass prints all its fields, so you see the YAML values and the defaults side by side, plus the device it chose."]],
    output_note="`device='mps'` because this was recorded on a Mac with an Apple GPU; you will see `cpu` or `cuda`.",
    gotcha="Put cheap checks where the mistake is made, not where it explodes. `__post_init__` is that place for configuration.",
    related=["python/class", "python/init", "python/default-args", "python/dict", "python/open-read"],
    keywords=["config", "yaml", "dataclass", "hyperparameters", "device"], source=GUIDE + ", step 9")

add(id="workflow/14-model", title="Step 14 · The transformer in four classes, with the two tests that catch almost everything", topic="wf-models", week=10, volatile=True,
    summary="Build it in order and run the tests after each class. A `Head` is one attention mechanism; `MultiHeadAttention` runs several in parallel; a `Block` wraps attention plus a small feed-forward network in residual connections; `GPT` stacks blocks between an embedding table and an output layer. Two tests matter most: the loss at initialisation equals ln(65), and information does not flow backwards in time.",
    files=[F("src/minigpt/model.py"), F("tests/test_model.py")],
    example=("python -c \"from minigpt.config import Config; from minigpt.model import GPT; m = GPT(Config.from_yaml('configs/base.yaml')); print(f'{m.n_params() / 1e6:.2f}M parameters')\"\n"
             "python -m unittest discover -s tests -v\n"
             "git add src tests\n"
             "git commit -m \"Add the transformer and its four tests\""),
    lines=[["class Head(nn.Module)", "Every PyTorch layer is a class that inherits from `nn.Module`: `__init__` declares the pieces (three `nn.Linear` projections: key, query, value) and `forward` says how data flows through them."],
           ["self.register_buffer(\"tril\", torch.tril(...))", "A lower-triangular matrix of ones, saved with the model but never trained. It is the causal mask."],
           ["att = q @ k.transpose(-2, -1) * k.shape[-1] ** -0.5", "Attention scores: how much each position should look at every other position, scaled so the numbers stay reasonable."],
           ["att.masked_fill(self.tril[:T, :T] == 0, float(\"-inf\"))", "Positions in the future are set to minus infinity, so softmax gives them probability zero. This line is what stops the model from cheating."],
           ["class MultiHeadAttention", "Runs `n_head` heads side by side (an `nn.ModuleList`), concatenates their outputs, and mixes them with one more linear layer."],
           ["class FeedForward", "Two linear layers with a GELU between them, applied to every position separately: the part of the block that “thinks” about what attention gathered."],
           ["class Block:  x = x + self.attn(self.ln1(x))", "Pre-norm residual: normalise, transform, add the result back to the input. The `x +` is what lets gradients flow through many layers."],
           ["class GPT:  tok_emb + pos_emb", "Each character id becomes a learned vector, plus a learned vector for its position in the block; the sum is what the blocks process."],
           ["loss = F.cross_entropy(logits.view(B * T, -1), targets.reshape(B * T))", "Flattens batch and time into one long list of predictions and computes the average loss, in nats."],
           ["@torch.no_grad() def generate(...)", "Feeds the last `block_size` characters, takes the logits of the final position, turns them into probabilities, samples one character, appends it, repeats. `temperature` and `top_k` shape the sampling."],
           ["test_loss_at_init_is_uniform", "An untrained model must be exactly as confused as guessing: loss ≈ ln(65) = 4.17. If you see 6 or 11, the output layer or the reshape is wrong; if you see 0.02, targets are leaking into the input."],
           ["test_attention_is_causal", "Change only the last character of a sequence; the logits at every earlier position must stay bit-for-bit identical. A broken mask produces a beautiful training curve and a useless model."],
           ["10.79M parameters", "`n_params()` adds up every trainable tensor. The number to quote in the README."]],
    gotcha="If the causal test fails, look at the mask before anything else. Everything downstream will look fine and be wrong.",
    related=["python/class", "python/inheritance", "python/init", "python/self", "python/unittest-testcase"],
    keywords=["transformer", "attention", "nn.Module", "causal mask", "embedding", "GPT"], source=GUIDE + ", step 10")

# ============================ Part IV · Train, evaluate, test ============================
add(id="workflow/15-smoke-run", title="Step 15 · Train the walking skeleton, and log every run", topic="wf-run", week=13, volatile=True,
    summary="The training loop is short; what makes it professional is everything around it: a fixed seed, a loss averaged over many batches instead of one noisy one, a CSV you can plot, a `manifest.json` recording which commit produced which number, and a checkpoint of the best validation loss. Always run the tiny config first: seconds, and it tells you whether the whole pipeline is wired correctly.",
    files=[F("src/minigpt/train.py")],
    example="python -m minigpt.train --config configs/tiny.yaml --run-name smoke\ncat runs/smoke/log.csv\ngit add src\ngit commit -m \"Add the training loop\"",
    lines=[["python -m minigpt.train --config configs/tiny.yaml --run-name smoke", "`-m` runs a module inside the installed package (`src/minigpt/train.py`) as a script, which is why its imports work from any folder."],
           ["argparse: --config, --run-name", "Command-line options with defaults, so the same script serves every experiment without being edited."],
           ["torch.manual_seed(cfg.seed); np.random.seed(cfg.seed)", "Fixed seeds make a run repeatable: same batches, same initial weights."],
           ["run_dir = Path(\"runs\") / run", "One folder per run, named by you or by the time. Everything the run produces goes there, and `runs/` is ignored by Git."],
           ["manifest.json: config, commit, params", "`git_commit()` asks Git for the current commit id, so every number you report is tied to the exact code that made it."],
           ["estimate_loss(model, splits, cfg)", "Averages the loss over `eval_iters` batches for train and validation. One batch is far too noisy to steer by."],
           ["for it in range(cfg.max_iters + 1): ...", "The loop: get a batch, forward pass, `zero_grad`, `backward`, clip the gradient norm, `opt.step()`. Every `eval_interval` steps it evaluates, writes a CSV row, and saves `best.pt` when validation improved."],
           ["iter 0 | train 4.18 | val 4.18", "Must match the untrained number from step 12. After 100 tiny iterations the loss is already falling; the point is not quality, it is that nothing crashed."],
           ["cat runs/smoke/log.csv", "The same numbers as a table: this file is what step 17 plots."]],
    output_note="Timings and the device (`mps`) depend on your hardware, and the losses can differ in the last decimals between CPU and GPU.",
    gotcha="If the loss starts near 11, the reshape in `cross_entropy` is wrong or `vocab_size` does not match the tokenizer; near 0, the targets are leaking into the inputs; stuck above 2.48, the transformer is losing to counting and the learning rate is the first suspect.",
    related=["python/for-loop", "python/open-write", "python/json-dump-load", "python/sys-argv", "python/time-perf-counter", "shell/python-script"],
    keywords=["train", "training loop", "checkpoint", "log", "seed", "smoke test"], source=GUIDE + ", step 11")

full_output = ""
if full_run_done:
    full_output = train_log + "\n\n" + sample
manual = (f"once, 2026-09-04, on an Apple M5 Max GPU (`mps`), {minutes:.0f} minutes for the training run; the verifier does not repeat it"
          if full_run_done else "pending")
add(id="workflow/16-full-run", title="Step 16 · The full run, and how to read the curve", topic="wf-run", week=13,
    manual_run=manual,
    harness=("mkdir -p runs/base\ncat > runs/base/log.csv <<'PT_LOG'\n" + log_csv + "\nPT_LOG") if log_csv else "",
    summary="The same command with the real config: about 10.8 million parameters for 5,000 iterations. Three things to check, in order. It starts at 4.18 like the untrained model. It passes 2.48 within a few hundred iterations: the moment the transformer overtakes counting. Train and validation stay close. Then sample from the best checkpoint and read what it learned.",
    example="python -m minigpt.train --config configs/base.yaml --run-name base\npython -m minigpt.sample --checkpoint runs/base/best.pt --n 600 --temperature 0.8 --seed 0",
    output=full_output,
    output_note=("Recorded from one run of exactly these commands on an Apple M5 Max GPU (%s minutes). Your numbers will differ slightly with different hardware and random draws; that is expected. Note how the run overfits after the best checkpoint: stopping earlier, or more dropout, would be the next experiment." % (f"{minutes:.0f}" if minutes else "?")),
    lines=CURVE,
    gotcha="Keep any single run under about ten minutes while developing; a project you cannot iterate on inside one sitting gets abandoned. On Apple silicon set `PYTORCH_ENABLE_MPS_FALLBACK=1` in the terminal first; on Colab the same config runs on a T4 unchanged.",
    related=["workflow/15-smoke-run", "workflow/17-evaluate", "python/plt-plot"],
    keywords=["full run", "training curve", "overfitting", "temperature", "sample"], source=GUIDE + ", steps 11–12")

add(id="workflow/17-evaluate", title="Step 17 · Evaluate: sample text and plot the curve", topic="wf-run", week=13, volatile=True,
    figure_file="runs/base/curve.png" if log_csv else "runs/smoke/curve.png",
    summary="Evaluation is a different job from unit testing. Tests ask “does the code do what I said”; evaluation asks “is the model any good”, has no assertions, and produces evidence you show a reader: validation loss, perplexity, the loss curves, and a table of samples.",
    files=[F("src/minigpt/sample.py"), F("scripts/plot_curve.py")],
    example=("python -m minigpt.sample --checkpoint runs/smoke/best.pt --n 150 --seed 0\n"
             + ("python scripts/plot_curve.py runs/base\n" if log_csv else "python scripts/plot_curve.py runs/smoke\n")
             + "git add src scripts\ngit commit -m \"Add sampling and the loss-curve plot\""),
    lines=[["torch.load(args.checkpoint, map_location=\"cpu\", weights_only=False)", "Reads the checkpoint dictionary the training loop saved: weights, config, iteration, validation loss."],
           ["Config(**ck[\"config\"]);  model.load_state_dict(ck[\"model\"])", "Rebuilds the exact model shape from the saved config, then loads the weights into it."],
           ["CharTokenizer.load(\"data/vocab.json\")", "The vocabulary saved in step 11 turns the generated ids back into text."],
           ["model.generate(start, args.n, args.temperature, args.top_k)", "Starts from a single character and grows the sequence `n` times."],
           ["the smoke sample", "After 100 tiny iterations the text is still noise with the shape of words: expected. The sample from the full run is in step 16."],
           ["scripts/plot_curve.py", "Reads `log.csv` with pandas, plots train and validation loss, and draws the two reference lines: 4.17 (untrained) and 2.48 (counting bigram). The gap between the two curves is the overfitting story."],
           ["fig.savefig(f\"{run}/curve.png\")", "Saves the figure next to the log, in the run folder, so the picture and the numbers that made it stay together. This is the figure that goes in any write-up."]],
    output_note="The curve is drawn from the `log.csv` of the full run recorded in step 16." if log_csv else "",
    gotcha="Quietly sampling at temperature 0.5 and calling it quality is the most common way people mislead themselves about a language model.",
    related=["python/plt-plot", "python/plt-labels", "python/plt-savefig", "python/pd-read-csv", "python/np-random"],
    keywords=["evaluate", "sample", "generate", "loss curve", "plot", "perplexity"], source=GUIDE + ", step 12")

add(id="workflow/18-test-suite", title="Step 18 · Consolidate the test suite: one command, seconds, no data", topic="wf-run", week=11, volatile=True,
    summary="By now every module has its tests. Add the one that covers the seams: overfit a single batch on purpose. If the model cannot memorise four sequences it sees two hundred times, the training wiring is broken, and you find out in three seconds instead of after an hour of training. The whole suite must run in seconds without touching `data/` or the network.",
    files=[F("tests/test_training.py")],
    example="python -m unittest discover -s tests\ngit add tests\ngit commit -m \"Add the overfit-one-batch test\"\ngit log --oneline",
    lines=[["test_model_can_overfit_one_batch", "Builds a tiny model and one random batch, runs 200 optimiser steps on it, and requires the loss to fall below a quarter of its starting value."],
           ["python -m unittest discover -s tests", "The whole suite: one dot per test, the count, `OK`. This is the command to run before every commit, and inside Colab."],
           ["git log --oneline", "The history so far, one line per commit: a readable record of how the project was built."]],
    gotcha="Do not test that the model is accurate; that is slow and flaky. Test properties that must hold regardless of training: shapes, the round trip, loss at initialisation, causality, rows summing to one, idempotent cleaning, and this overfit test.",
    related=["python/unittest-suite", "python/unittest-main", "python/assert", "git/log"],
    keywords=["test suite", "unittest discover", "overfit", "regression test"], source=GUIDE + ", step 13")

# ============================ Part V · Ship it ============================
add(id="workflow/19-colab", title="Step 19 · Use Colab as a thin client", topic="wf-ship", week=9, no_run=True, code_lang="python",
    summary="The repository is the project; the notebook is a window onto it. The first cell clones your GitHub repository, installs the package and prepares the data; the second checks the GPU, runs the tests and trains; the third copies the results to Google Drive, because Colab disconnects. The notebook contains no model code, which is why the same repository runs identically on your laptop and on Colab's GPU.",
    example=("# cell 1 - get the code and the data\n"
             "!git clone -q https://github.com/YOUR-USERNAME/minigpt.git\n"
             "%cd minigpt\n"
             "!pip install -q -e .\n"
             "!python scripts/get_data.py\n"
             "!python -c \"from minigpt.data import build_arrays; build_arrays()\"\n"
             "\n"
             "# cell 2 - check the runtime, test, train\n"
             "import torch\n"
             "print(torch.__version__, torch.cuda.is_available())\n"
             "!nvidia-smi --query-gpu=name,memory.total --format=csv\n"
             "!python -m unittest discover -s tests\n"
             "!python -m minigpt.train --config configs/tiny.yaml --run-name smoke\n"
             "!python -m minigpt.train --config configs/base.yaml --run-name colab-01\n"
             "\n"
             "# cell 3 - keep the results (Colab forgets everything when it disconnects)\n"
             "from google.colab import drive\n"
             "drive.mount('/content/drive')\n"
             "!mkdir -p /content/drive/MyDrive/minigpt-runs\n"
             "!cp -r runs/colab-01 /content/drive/MyDrive/minigpt-runs/"),
    output_note="Runs only in Colab (Runtime → Change runtime type → GPU). Nothing is recorded here because it depends on your GitHub account and a live Colab session.",
    lines=[["!git clone -q https://github.com/YOUR-USERNAME/minigpt.git", "`!` runs a shell command from a notebook cell. Downloads your repository into Colab's `/content` folder; `-q` keeps it quiet."],
           ["%cd minigpt", "A Colab magic that changes the notebook's working directory (a plain `!cd` would not stick)."],
           ["!pip install -q -e .", "The same editable install as step 7, inside Colab's Python. Plain `pip` is safe here because a Colab runtime has exactly one Python; on your own computer keep writing `python -m pip`."],
           ["!python scripts/get_data.py  /  !python -c \"... build_arrays()\"", "Steps 8 and 11 again: the data is never in the repository, so every fresh machine rebuilds it from the scripts."],
           ["print(torch.__version__, torch.cuda.is_available())", "Must print `True`; otherwise the runtime has no GPU and the full run will take hours."],
           ["!nvidia-smi --query-gpu=name,memory.total --format=csv", "Which GPU Colab gave you and how much memory it has, for the record."],
           ["!python -m unittest discover -s tests", "The tests run here too: a fresh machine is exactly where a missing dependency shows up."],
           ["the two training lines", "The smoke run first, then the real run under a new name, so both logs are kept."],
           ["drive.mount('/content/drive')", "Asks permission to attach your Google Drive as a folder; then `cp -r` copies the run folder there, where it survives the session."]],
    gotcha="Never paste a token into a cell: use Colab's Secrets panel and `userdata.get(\"GITHUB_TOKEN\")`. Strip outputs before committing a notebook (`pip install nbstripout` then `nbstripout --install`), and use “Restart and run all” before you trust a result: notebook state is invisible and lies to you.",
    related=["shell/bang-in-colab", "shell/percent-cd", "python/pip-install", "git/clone", "python/colab-files-panel"],
    keywords=["colab", "clone", "thin client", "drive mount", "gpu"], source=GUIDE + ", step 14")

add(id="workflow/20-branches", title="Step 20 · Every experiment on its own branch", topic="wf-ship", week=9,
    summary="Once the pipeline works, every change is an experiment and experiments belong on branches. This is also how three people share one codebase without overwriting each other. Put the number in the commit message: six weeks later `git log --oneline` is a readable history of what you tried and what it bought you, which is exactly the material a report is written from.",
    example=("git switch -c experiment/wider-model\n"
             "sed -i '' 's/n_embd: 384/n_embd: 512/' configs/base.yaml\n"
             "git diff\n"
             "git add configs/base.yaml\n"
             "git commit -m \"Widen to n_embd=512 (experiment)\"\n"
             "git push -u origin experiment/wider-model\n"
             "git switch main"),
    lines=[["git switch -c experiment/wider-model", "Creates the branch and moves to it. Nothing on `main` changes. Slashes in the name are just a naming convention."],
           ["sed -i '' 's/n_embd: 384/n_embd: 512/' configs/base.yaml", "Edits the file in place: replace `n_embd: 384` with `n_embd: 512`. In real life you open the file in VS Code and change the number; the command is here so the step can be recorded. On Linux the option is `-i` without the quotes."],
           ["git diff", "Shows exactly what changed, line by line (`-` old, `+` new), before you commit it."],
           ["git commit -m \"Widen to n_embd=512 (experiment)\"", "After running the experiment, put the result in the message as well: “val loss 1.47 (was 1.51)”."],
           ["git push -u origin experiment/wider-model", "Publishes the branch under the same name, which is what the pull request in step 21 needs."],
           ["git switch main", "Back to the safe branch: `configs/base.yaml` shows 384 again, because the change exists only on the branch."],
           ["Your branch is ahead of 'origin/main' by 11 commits", "A reminder from Git: `main` has not been pushed since step 6. Commit often, push at the end of a session; step 22 pushes everything."]],
    gotcha="Commit the run's `manifest.json` together with the config change, so the number and the code that produced it travel together.",
    related=["git/branch", "git/diff", "git/push", "git/log", "git/pull-request"],
    keywords=["branch", "switch", "experiment", "sed", "diff"], source=GUIDE + ", step 15")

add(id="workflow/21-pull-request", title="Step 21 · Open a pull request, get a review, merge", topic="wf-ship", week=9, no_run=True, code_lang="text",
    summary="After the push, GitHub offers to open a pull request: a page that shows the diff, lets a teammate (or future you) comment, and ends with a **Merge** button that folds the branch into `main`. In a solo project it is still the place where you write down what the change achieved.",
    example=("GitHub → your repository → \"Compare & pull request\" (the banner shown after a push)\n"
             "  base: main   ←   compare: experiment/wider-model\n"
             "  Title:        Widen the model to n_embd=512\n"
             "  Description:  what changed and what it bought: val loss 1.47 (was 1.51), 14 min on a T4\n"
             "→ Create pull request → (review) → Merge pull request → Delete branch\n"
             "\n"
             "Then, on your computer:\n"
             "git switch main\n"
             "git pull\n"
             "git branch -d experiment/wider-model"),
    output_note="Nothing runs locally until the last three commands; they bring the merged result down and delete the finished branch.",
    lines=[["base ← compare", "`base` is where the change goes (`main`); `compare` is the branch that holds it."],
           ["Description", "Numbers and a sentence. This text, not your memory, is what the report is written from."],
           ["Merge pull request", "GitHub creates a merge commit on `main`. Your laptop does not know yet."],
           ["git switch main  /  git pull", "Downloads the merged commits so local `main` matches GitHub."],
           ["git branch -d experiment/wider-model", "`-d` deletes the local branch only if it has been merged, so it is safe."]],
    gotcha="If GitHub reports conflicts, `main` moved while you worked: run `git pull origin main` on your branch, fix the marked files, commit and push again, and the button turns green.",
    related=["git/pull-request", "git/pull", "git/branch"],
    keywords=["pull request", "merge", "review", "PR"], source=GUIDE + ", step 15")

add(id="workflow/22-readme", title="Step 22 · A README that earns its place", topic="wf-ship", week=9,
    summary="One page: what this is, how to reproduce it, and what the numbers are. Someone with your repository and nothing else should reach your headline result with four commands. Commit it and push; the project is now something another person can run.",
    files=[F("README.md", README_FINAL)],
    example="git add README.md\ngit commit -m \"Write the README: reproduce and results\"\ngit push\ngit log --oneline",
    lines=[["# miniGPT, then one paragraph", "What it is, in two sentences. Not a tutorial."],
           ["## Reproduce: four commands", "Environment, install, data, train: exactly the commands from steps 2, 7, 8, 11 and 16, with `python -m pip` so the reader's install lands in the environment they just created. If a reader cannot paste these and get your number, the README is not finished."],
           ["## Results: a table", "Untrained, baseline, model: the three numbers from steps 12 and 16, in the same units, so the improvement is visible at a glance. Markdown tables are pipes and dashes."],
           ["git push", "No `-u` needed any more: step 6 recorded where `main` goes."],
           ["git log --oneline", "The finished history: a dozen commits that read like a build log."]],
    gotcha="Update the results table every time the number changes, in the same commit as the change. A README with stale numbers is worse than one with none.",
    related=["markdown/headings", "markdown/table", "markdown/code-block", "git/push", "git/log"],
    keywords=["readme", "reproduce", "results table", "documentation"], source=GUIDE + ", step 15")

# ---- carry verified outputs forward, write ------------------------------------------------
old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
old_by_id = {e["id"]: e for e in old.get("entries", [])}
for e in E:
    o = old_by_id.get(e["id"])
    if o and not e.get("output") and not e.get("manual_run"):
        e["output"] = o.get("output", "")
        if o.get("image"):
            e["image"] = o["image"]
    if e.get("harness") == "":
        del e["harness"]
    if e.get("output_note") == "":
        del e["output_note"]
ids = [e["id"] for e in E]
assert len(ids) == len(set(ids)), "duplicate ids"
topic_ids = {t["id"] for t in TOPICS}
assert all(e["topic"] in topic_ids for e in E)
data = {"language": "workflow", "topics": TOPICS, "entries": E, "verified": old.get("verified", "")}
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(E)} entries, full run recorded: {full_run_done}" + (f", best val {best_val:.4f}, {minutes:.1f} min" if full_run_done else ""))
