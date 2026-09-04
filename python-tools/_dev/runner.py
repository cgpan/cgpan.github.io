#!/usr/bin/env python3
"""Run notebook-style cells the way Google Colab would, for PythonTools verification.

Called by verify.py inside the verification environment:
    python runner.py job.json

job.json:
    {"cwd": "...", "cells": ["setup source", "example source"], "capture_from": 1,
     "expect_error": false, "fig": "/tmp/x/fig.png", "html": "/tmp/x/fig.html"}

Behaviour that mimics Colab:
  * lines starting with `!` run in the shell (output captured in order)
  * `%cd path` changes the working directory and prints it
  * a cell whose first line is `%%writefile name` writes the file and prints "Writing name"
  * `%matplotlib inline` and other line magics are ignored
  * a bare expression on the last line is displayed (its repr), like a notebook cell
  * a matplotlib figure left open at the end, a plotnine ggplot or a plotly figure that is
    displayed/shown, is saved to `fig` / `html` so verify.py can turn it into an image
The result is printed as one JSON object on the last line of stdout.
"""
import ast, contextlib, io, json, os, subprocess, sys, traceback, types, warnings

job = json.load(open(sys.argv[1], encoding="utf-8"))
os.chdir(job["cwd"])
sys.path.insert(0, job["cwd"])              # like a notebook: the working folder is importable
OUT = io.StringIO()
ERR = io.StringIO()
SINK = OUT                                  # where the current cell's output goes
MAIN = types.ModuleType("__main__")         # the cells run inside a real __main__ module,
sys.modules["__main__"] = MAIN              # so unittest.main() finds the TestCase classes
NS = MAIN.__dict__
FLAGS = {"figure": False, "html": False}


def sh(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=os.environ)
    SINK.write(p.stdout)


def cd(path):
    os.chdir(os.path.expanduser(path) if path else os.path.expanduser("~"))
    SINK.write(os.getcwd() + "\n")


NS["__sh"] = sh
NS["__cd"] = cd


def install_patches(src):
    """Pre-import plotting libraries mentioned in the cell and neutralise their display calls."""
    if "matplotlib" in src or "plt." in src or ".plot(" in src or ".hist(" in src or ".boxplot(" in src or "plotnine" in src:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            plt.show = lambda *a, **k: None
        except Exception:
            pass
    if "plotly" in src:
        try:
            import plotly.basedatatypes as bdt

            def _show(self, *a, **k):
                self.write_html(job["html"], include_plotlyjs=True, full_html=True, default_width="740px", default_height="430px")
                FLAGS["html"] = True
            bdt.BaseFigure.show = _show
        except Exception:
            pass


def transform(src):
    """Turn Colab magics into Python calls; returns None when the whole cell was a %%writefile."""
    lines = src.split("\n")
    if lines and lines[0].startswith("%%writefile"):
        parts = lines[0].split(maxsplit=1)
        name = parts[1].strip() if len(parts) > 1 else "cell.py"
        existed = os.path.exists(name)
        with open(name, "w", encoding="utf-8") as f:
            f.write("\n".join(lines[1:]).rstrip("\n") + "\n")
        SINK.write(("Overwriting " if existed else "Writing ") + name + "\n")
        return None
    res = []
    for ln in lines:
        s = ln.lstrip()
        ind = ln[:len(ln) - len(s)]
        if s.startswith("!"):
            res.append("%s__sh(%r)" % (ind, s[1:].strip()))
        elif s.startswith("%cd"):
            res.append("%s__cd(%r)" % (ind, s[3:].strip()))
        elif s.startswith("%pip ") or s.startswith("%conda "):
            res.append("%s__sh(%r)" % (ind, s[1:].strip()))
        elif s.startswith("%"):
            res.append(ind + "pass")
        else:
            res.append(ln)
    return "\n".join(res)


def display(val):
    if val is None:
        return
    mod = type(val).__module__ or ""
    if mod.startswith("plotnine"):
        try:
            val.save(job["fig"], width=6.4, height=4.2, dpi=110, verbose=False)
        except TypeError:
            val.save(job["fig"], width=6.4, height=4.2, dpi=110)
        FLAGS["figure"] = True
        return
    if mod.startswith("plotly"):
        val.show()
        return
    if mod.startswith("matplotlib.figure"):
        return  # saved below from the open figures
    SINK.write(repr(val) + "\n")


def run_cell(src, capture):
    global SINK
    SINK = OUT if capture else io.StringIO()
    install_patches(src)
    code = transform(src)
    if code is None:
        return
    tree = ast.parse(code, filename="<cell>")
    last = tree.body[-1] if tree.body and isinstance(tree.body[-1], ast.Expr) else None
    body = tree.body[:-1] if last is not None else tree.body
    sink = SINK
    # Colab shows stdout and stderr together, so unittest output (stderr) is part of what students see.
    # Warnings keep Python's default filters (library-internal DeprecationWarnings stay hidden, as in Colab)
    # and are reported separately so verify.py can flag them.
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink), warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("ignore", ResourceWarning)
        exec(compile(ast.Module(body=body, type_ignores=[]), "<cell>", "exec"), NS)
        if last is not None:
            display(eval(compile(ast.Expression(last.value), "<cell>", "eval"), NS))
    for w in caught:
        ERR.write("%s: %s\n" % (w.category.__name__, w.message))


def save_open_figure():
    if "matplotlib.pyplot" not in sys.modules:
        return
    plt = sys.modules["matplotlib.pyplot"]
    if plt.get_fignums():
        plt.gcf().savefig(job["fig"], dpi=110, bbox_inches="tight")
        FLAGS["figure"] = True
        plt.close("all")


cells = job["cells"]
capture_from = job.get("capture_from", len(cells) - 1)
for i, src in enumerate(cells):
    try:
        run_cell(src, capture=(i >= capture_from))
    except SyntaxError as e:
        if job.get("expect_error"):
            OUT.write("SyntaxError: %s\n" % e.msg)
        else:
            ERR.write(traceback.format_exc())
        break
    except BaseException as e:  # noqa: BLE001 — we are emulating a notebook's error display
        if job.get("expect_error"):
            msg = str(e)
            OUT.write(type(e).__name__ + (": " + msg if msg else "") + "\n")
        else:
            ERR.write(traceback.format_exc())
        break
try:
    save_open_figure()
except Exception:
    ERR.write(traceback.format_exc())

sys.__stdout__.write(json.dumps({"output": OUT.getvalue(), "stderr": ERR.getvalue(), "figure": FLAGS["figure"], "html": FLAGS["html"]}) + "\n")
