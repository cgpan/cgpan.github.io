#!/usr/bin/env python3
"""Verify (or write) the `output` of every PythonTools entry by actually running it.

Usage
  python3 verify.py                       # check every entry: PASS / FAIL / MISSING
  python3 verify.py --write               # run everything and store outputs (and figures)
  python3 verify.py --lang sql            # one language
  python3 verify.py --id python/print     # one entry
  python3 verify.py --show                # print every captured output
  python3 verify.py --python /opt/anaconda3/envs/hudm5001-verify/bin/python

Run it with the verification environment's python so the Markdown renderer is available:
  /opt/anaconda3/envs/hudm5001-verify/bin/python verify.py --write

How entries run (the `runner` field overrides the language default)
  python    setup and example are notebook cells run by runner.py inside the chosen
            interpreter (Colab-style: `!` lines, `%cd`, `%%writefile`, bare last expression,
            figures). Working directory is shown as /content, the home directory as /root.
  markdown  the example is rendered with Python-Markdown into `output_html`.
  sql       `.headers on`, `.mode column`, `.nullvalue NULL`, then setup + example, fed to
            the `sqlite3` shell on an in-memory database.
  shell/git setup + example run in bash inside a fresh folder ~/hudm5001 under a temporary
            home (shown as /Users/student; the account name is shown as `student`).
            git commits use a fixed author and date so commit ids reproduce.
            macOS has no `wget`; when it is missing a small curl-based stand-in that
            understands `wget -q URL -O file` is put on the PATH for the run.

Entry flags
  "expect_error": true   keep the last line of the error as output (like a notebook)
  "volatile": true       the output changes run to run (dates, timings): record it, never fail
  "figure": true         the example draws a chart; the image is saved to img/ and linked
  "no_run": true         nothing to run (menu paths, conceptual entries)
"""
import argparse, datetime, getpass, json, os, pathlib, platform, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
IMG = ROOT / "img"
FIXTURES = HERE / "fixtures"
RUNNER = HERE / "runner.py"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

LANG_FILES = {"markdown": "markdown.json", "python": "python.json", "sql": "sql.json", "shell": "shell.json", "git": "git.json"}

WGET_SHIM = """#!/bin/bash
# stand-in for wget on machines without it (verification only): wget [-q] URL [-O file]
out=""; url=""
while [ $# -gt 0 ]; do
  case "$1" in
    -q|--quiet) ;;
    -O) out="$2"; shift ;;
    *) url="$1" ;;
  esac
  shift
done
[ -z "$out" ] && out=$(basename "$url")
curl -sL "$url" -o "$out"
"""


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def dump(name, obj):
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def strip_trailing(s):
    return "\n".join(line.rstrip() for line in s.rstrip("\n").splitlines())


def copy_fixtures(dst):
    for f in FIXTURES.glob("*.csv"):
        shutil.copy(f, dst)


def path_with_shims(tmp, python):
    """PATH for a run: the interpreter's bin dir first, plus a wget stand-in when wget is absent."""
    parts = [str(pathlib.Path(python).parent)]
    if shutil.which("wget") is None:
        shim = pathlib.Path(tmp) / "shim"
        shim.mkdir(exist_ok=True)
        (shim / "wget").write_text(WGET_SHIM, encoding="utf-8")
        (shim / "wget").chmod(0o755)
        parts.append(str(shim))
    parts.append(os.environ.get("PATH", ""))
    return os.pathsep.join(parts)


def screenshot_html(html_path, png_path):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=780,470",
                    "--virtual-time-budget=6000", "--screenshot=" + str(png_path), "file://" + str(html_path)],
                   capture_output=True, text=True, timeout=120)


def run_python(entry, python, slug):
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp) / "content"
        work.mkdir()
        copy_fixtures(work)
        cells = ([entry["setup"]] if entry.get("setup") else []) + [entry["example"]]
        job = {"cwd": str(work), "cells": cells, "capture_from": len(cells) - 1, "expect_error": bool(entry.get("expect_error")),
               "fig": str(pathlib.Path(tmp) / "fig.png"), "html": str(pathlib.Path(tmp) / "fig.html")}
        jobfile = pathlib.Path(tmp) / "job.json"
        jobfile.write_text(json.dumps(job), encoding="utf-8")
        env = {"PATH": path_with_shims(tmp, python), "HOME": tmp, "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8",
               "PYTHONHASHSEED": "0", "COLUMNS": "80", "MPLBACKEND": "Agg", "PYTHONIOENCODING": "utf-8", "TZ": "America/New_York",
               "PYTHONDONTWRITEBYTECODE": "1",
               # keep matplotlib's font cache between runs (a fresh HOME would rebuild it every time)
               "MPLCONFIGDIR": os.path.join(tempfile.gettempdir(), "pythontools-mplconfig")}
        p = subprocess.run([python, "-X", "utf8", str(RUNNER), str(jobfile)], cwd=work, env=env, capture_output=True, text=True, timeout=300)
        lines = p.stdout.strip().splitlines()
        try:
            res = json.loads(lines[-1]) if lines else {}
        except json.JSONDecodeError:
            res = {}
        if not res:
            return "", "runner failed:\n" + p.stdout + p.stderr, None
        out = res["output"]
        for real in (os.path.realpath(str(work)), str(work)):
            out = out.replace(real, "/content")
        for real in (os.path.realpath(tmp), tmp):
            out = out.replace(real, "/root")
        err = res.get("stderr", "") + p.stderr
        image = None
        if entry.get("figure"):
            IMG.mkdir(exist_ok=True)
            png = IMG / (slug + ".png")
            if res.get("figure") and pathlib.Path(job["fig"]).exists():
                shutil.copy(job["fig"], png)
                image = "img/" + png.name
            elif res.get("html") and pathlib.Path(job["html"]).exists():
                screenshot_html(job["html"], png)
                image = "img/" + png.name if png.exists() else None
            else:
                err += "\nno figure was produced although \"figure\": true"
    return strip_trailing(out), err.strip(), image


def run_markdown(entry):
    import markdown  # Python-Markdown
    html = markdown.markdown(entry["example"], extensions=["fenced_code", "tables", "sane_lists"])
    return html.strip(), "", None


def run_sql(entry):
    script = ".headers on\n.mode column\n.nullvalue NULL\n" + entry.get("setup", "") + "\n" + entry["example"] + "\n"
    p = subprocess.run(["sqlite3", ":memory:"], input=script, capture_output=True, text=True, timeout=60)
    return strip_trailing(p.stdout + p.stderr), "", None


def run_shell(entry, python, git=False):
    with tempfile.TemporaryDirectory() as tmp:
        home = pathlib.Path(tmp) / "home"
        work = home / "hudm5001"
        work.mkdir(parents=True)
        copy_fixtures(work)
        env = {"PATH": path_with_shims(tmp, python), "HOME": str(home), "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8",
               "TZ": "America/New_York", "TERM": "dumb", "PAGER": "cat", "GIT_PAGER": "cat",
               "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_PARAMETERS": "'init.defaultBranch=main' 'advice.detachedHead=false'"}
        if git:
            env.update({
                "GIT_AUTHOR_NAME": "Student Example", "GIT_AUTHOR_EMAIL": "student@example.com",
                "GIT_COMMITTER_NAME": "Student Example", "GIT_COMMITTER_EMAIL": "student@example.com",
                "GIT_AUTHOR_DATE": "2026-09-08T11:00:00-04:00", "GIT_COMMITTER_DATE": "2026-09-08T11:00:00-04:00",
            })
        script = entry.get("setup", "") + "\n" + entry["example"] + "\n"
        p = subprocess.run(["bash", "-c", script], cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180)
        out = p.stdout
        for real in (os.path.realpath(str(home)), str(home), os.path.realpath(tmp), tmp):
            out = out.replace(real, "/Users/student")
    user = getpass.getuser()
    if user:
        out = out.replace(user, "student")
    return strip_trailing(out), "", None


def versions(python):
    v = {"date": datetime.date.today().isoformat()}
    try:
        code = ("import sys, json\n"
                "d = {'python': sys.version.split()[0]}\n"
                "for m in ['pandas', 'numpy', 'matplotlib', 'plotnine', 'plotly']:\n"
                "    try:\n        d[m] = __import__(m).__version__\n    except Exception:\n        pass\n"
                "print(json.dumps(d))")
        v.update(json.loads(subprocess.run([python, "-c", code], capture_output=True, text=True, timeout=120).stdout))
    except Exception as e:  # pragma: no cover
        v["python_error"] = str(e)
    try:
        v["sqlite"] = subprocess.run(["sqlite3", "--version"], capture_output=True, text=True).stdout.split()[0]
    except Exception:
        pass
    try:
        v["git"] = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip().replace("git version ", "")
    except Exception:
        pass
    v["platform"] = platform.platform()
    return v


def stamp(v, lang):
    if lang == "python":
        parts = ["python " + v.get("python", "?")]
        for m in ("pandas", "numpy"):
            if m in v:
                parts.append(m + " " + v[m])
        return v["date"] + " · " + " · ".join(parts)
    if lang == "sql":
        return v["date"] + " · sqlite3 " + v.get("sqlite", "?")
    if lang == "git":
        return v["date"] + " · git " + v.get("git", "?")
    if lang == "shell":
        return v["date"] + " · bash on " + ("macOS" if sys.platform == "darwin" else sys.platform)
    return v["date"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="store the captured outputs")
    ap.add_argument("--lang", choices=sorted(LANG_FILES))
    ap.add_argument("--id")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--show", action="store_true", help="print captured output for every entry")
    args = ap.parse_args()

    v = versions(args.python)
    print(f"verifying with python={v.get('python')} pandas={v.get('pandas')} numpy={v.get('numpy')} "
          f"matplotlib={v.get('matplotlib')} plotnine={v.get('plotnine')} plotly={v.get('plotly')} sqlite3={v.get('sqlite')} git={v.get('git')}")
    totals = {"PASS": 0, "FAIL": 0, "MISSING": 0, "WRITE": 0, "SKIP": 0, "STDERR": 0}
    for lang, fname in LANG_FILES.items():
        if args.lang and lang != args.lang:
            continue
        data = load(fname)
        changed = False
        for e in data["entries"]:
            if args.id and e["id"] != args.id:
                continue
            if e.get("no_run") or not e.get("example"):
                totals["SKIP"] += 1
                continue
            runner = e.get("runner", lang)
            slug = e["id"].replace("/", "-")
            if runner == "python":
                out, err, image = run_python(e, args.python, slug)
            elif runner == "markdown":
                out, err, image = run_markdown(e)
            elif runner == "sql":
                out, err, image = run_sql(e)
            else:
                out, err, image = run_shell(e, args.python, git=(runner == "git"))
            key = "output_html" if runner == "markdown" else "output"
            stored = e.get(key, "")
            if err:
                totals["STDERR"] += 1
            if args.show or err:
                print(f"--- {e['id']} ---")
                print(out)
                if err:
                    print("[stderr]", err)
            if args.write:
                if stored != out or (image and e.get("image") != image):
                    e[key] = out
                    if image:
                        e["image"] = image
                    changed = True
                    totals["WRITE"] += 1
                    print(f"WRITE   {e['id']}" + (f"  -> {image}" if image else ""))
                else:
                    totals["PASS"] += 1
            else:
                if not stored and not e.get("image"):
                    totals["MISSING"] += 1
                    print(f"MISSING {e['id']}")
                elif stored == out or e.get("volatile"):
                    totals["PASS"] += 1
                else:
                    totals["FAIL"] += 1
                    print(f"FAIL    {e['id']}")
                    print("  stored  :", repr(stored[:300]))
                    print("  captured:", repr(out[:300]))
        if args.write:
            data["verified"] = stamp(v, lang)
            dump(fname, data)
            if changed:
                print(f"saved {fname}")
    if args.write:
        m = load("manifest.json")
        m["verified"] = {"date": v["date"], "python": v.get("python", ""), "pandas": v.get("pandas", ""), "numpy": v.get("numpy", ""),
                         "matplotlib": v.get("matplotlib", ""), "plotnine": v.get("plotnine", ""), "plotly": v.get("plotly", ""),
                         "sqlite": v.get("sqlite", ""), "git": v.get("git", "")}
        dump("manifest.json", m)
    print("summary:", totals)
    return 1 if (totals["FAIL"] or totals["MISSING"]) and not args.write else 0


if __name__ == "__main__":
    sys.exit(main())
