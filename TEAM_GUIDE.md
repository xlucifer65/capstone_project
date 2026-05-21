# CAPSTONE PROJECT — TEAM GUIDE
## BST-Backed Hyperparameter Optimiser with Transfer Analysis
**Course:** Algorithmic Workshop (AIS / EPITA) | **Instructor:** Adrian ROSARI

---

## WHO DOES WHAT

| Person | Files They Own | Core Skill Needed |
|--------|---------------|-------------------|
| **Person A** | `bst_toolkit/node.py`, `bst_toolkit/bst.py`, `bst_toolkit/registry.py`, `bst_toolkit/rebuild.py` | Recursion, BST algorithms |
| **Person B** | `data/download.py`, `ml_toolkit/grid_search.py`, `ml_toolkit/transfer.py` | pandas, scikit-learn, itertools |
| **Person C** | `benchmarks/timer.py`, `notebook/capstone.ipynb`, integration testing | Jupyter, matplotlib, timing |

---

## FULL WORKFLOW FLOWCHART

```
╔══════════════════════════════════════════════════════════════════╗
║                        PROJECT START                             ║
║              ALL 3 PEOPLE: Clone repo + pip install -e .         ║
╚══════════════════════════════════════════════════════════════════╝
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
  ┌───────────────┐   ┌────────────────┐   ┌────────────────┐
  │   PERSON A    │   │   PERSON B     │   │   PERSON C     │
  │  bst_toolkit  │   │  data +        │   │  benchmarks    │
  └───────────────┘   │  ml_toolkit    │   └────────────────┘
          │           └────────────────┘          │
          │                    │                  │
          ▼                    ▼                  ▼
  ┌───────────────┐   ┌────────────────┐   ┌────────────────┐
  │  STEP A-1     │   │  STEP B-1      │   │  STEP C-1      │
  │  node.py      │   │  download.py   │   │  timer.py      │
  │  (TrialNode   │   │  (downloads    │   │  @timed        │
  │   dataclass)  │   │   both CSVs)   │   │  benchmark()   │
  └───────────────┘   └────────────────┘   └────────────────┘
          │                    │                  │
          ▼                    │            ✅ DONE C-1
  ┌───────────────┐            │            (Can now time
  │  STEP A-2     │            │             anything)
  │  bst.py       │            │
  │  insert       │            ▼
  │  search       │   ┌────────────────┐
  │  delete       │   │  STEP B-2      │
  │  traversals   │   │  grid_search.py│
  └───────────────┘   │  (needs A's    │◄────── WAITS FOR A-3
          │           │   registry)    │
          ▼           └────────────────┘
  ┌───────────────┐            │
  │  STEP A-3     │            │
  │  registry.py  │            │
  │  (wraps BST   │────────────┘
  │   with        │   ← Person A tells B:
  │   add_trial,  │     "registry.py is ready"
  │   top_k etc)  │
  └───────────────┘
          │
          ▼
  ┌───────────────┐
  │  STEP A-4     │
  │  rebuild.py   │────────────────────────────────┐
  │  naive        │                                │
  │  shuffled     │   ← Person A tells B:          │
  │  balanced     │     "rebuild.py is ready"      │
  └───────────────┘                                │
                                                   ▼
                                          ┌────────────────┐
                                          │  STEP B-3      │
                                          │  transfer.py   │
                                          │  (needs A-3,   │
                                          │   A-4 + B-2)   │
                                          └────────────────┘
                                                   │
          ┌────────────────────────────────────────┘
          │
          ▼
╔══════════════════════════════════════════════════════════════════╗
║                    INTEGRATION POINT                             ║
║         ALL PACKAGES DONE — Person C takes over notebook         ║
╚══════════════════════════════════════════════════════════════════╝
          │
          ▼
  ┌───────────────────────────────────────────────────────────┐
  │                    PERSON C: notebook                     │
  │                                                           │
  │  Section 1: Introduction                                  │
  │      ↓                                                    │
  │  Section 2: Dataset A Exploration (uses B's download.py)  │
  │      ↓                                                    │
  │  Section 3: Phase 1 - Grid Search (uses B's grid_search)  │
  │      ↓                                                    │
  │  Section 4: BST Introspection (uses A's bst_toolkit)      │
  │      ↓                                                    │
  │  Section 5: Dataset B Exploration                         │
  │      ↓                                                    │
  │  Section 6: Phase 2 - BST Rebuild (uses A's rebuild.py)   │
  │             + Benchmark with C's timer.py                 │
  │      ↓                                                    │
  │  Section 7: Transfer Analysis (uses B's transfer.py)      │
  │      ↓                                                    │
  │  Section 8: Conclusion                                    │
  └───────────────────────────────────────────────────────────┘
          │
          ▼
╔══════════════════════════════════════════════════════════════════╗
║                        FINAL STEPS                               ║
║  ALL: Review notebook → git commit → git tag v1.0 → submit      ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## DEPENDENCY MAP — What blocks what

```
node.py
   └──► bst.py
            └──► registry.py
                      └──► grid_search.py ──► transfer.py
                      └──► rebuild.py     ──► transfer.py
                                          ──► notebook sections 6+7

download.py ──► grid_search.py ──► notebook section 3
            ──► notebook section 2+5

timer.py ──► notebook section 6 (benchmarks)
```

**Simple rule:**
- Person B **cannot** start `grid_search.py` until Person A finishes `registry.py`
- Person B **cannot** start `transfer.py` until Person A finishes `rebuild.py`
- Person C **cannot** write notebook sections 3-8 until A and B are done
- Person C **CAN** start `timer.py` on Day 1 — it has no dependencies

---

## PERSON A — STEP BY STEP

```
[ ] Step A-1: Write bst_toolkit/node.py
    → TrialNode dataclass (score, params, left, right)
    → __lt__ method
    → __repr__ method
    → COMMIT: "feat: implement TrialNode dataclass"

[ ] Step A-2: Write bst_toolkit/bst.py
    → __init__
    → insert + _insert (recursive helper)
    → search + _search
    → delete + _delete (3 cases)
    → find_min, find_max
    → height + _height
    → is_balanced + _check_balanced
    → inorder, preorder, postorder, level_order
    → all private traversal helpers
    → COMMIT: "feat: implement BST insert, delete, search, traversals"

[ ] Step A-3: Write bst_toolkit/registry.py
    → HyperparamRegistry class
    → add_trial, best, worst, top_k
    → range_query, prune_below
    → all_trials, summary
    → _reverse_inorder, _range helpers
    → COMMIT: "feat: implement HyperparamRegistry"
    → *** TELL PERSON B: registry.py is ready ***

[ ] Step A-4: Write bst_toolkit/rebuild.py
    → rebuild_naive
    → rebuild_shuffled
    → rebuild_balanced
    → _build_from_sorted (divide & conquer)
    → COMMIT: "feat: implement 3 BST rebuild strategies"
    → *** TELL PERSON B: rebuild.py is ready ***
```

---

## PERSON B — STEP BY STEP

```
[ ] Step B-1: Write data/download.py
    → Download breast cancer ZIP from UCI
    → Download banknote ZIP from UCI
    → Extract, clean, save as wdbc.csv and banknote.csv
    → Idempotent (skip if files already exist)
    → Print row counts
    → COMMIT: "feat: implement dataset download and preprocessing"

[ ] Step B-2: Write ml_toolkit/grid_search.py     ← WAIT FOR A-3
    → Use itertools.product to generate all param combos
    → Call evaluate_fn for each combo
    → Store results in HyperparamRegistry
    → tqdm progress bar
    → COMMIT: "feat: implement grid search with BST registry"

[ ] Step B-3: Write ml_toolkit/transfer.py        ← WAIT FOR A-3, A-4, B-2
    → In-order traverse both registries
    → Build rank lookup dicts
    → Compute rank drift for each config
    → Return sorted report list
    → COMMIT: "feat: implement transfer analysis"
```

---

## PERSON C — STEP BY STEP

```
[ ] Step C-1: Write benchmarks/timer.py           ← NO DEPENDENCIES, START NOW
    → @timed decorator with functools.wraps
    → benchmark(fn, *args, repeats=5) function
    → Use time.perf_counter()
    → COMMIT: "feat: implement timing decorator and benchmark utility"

[ ] Step C-2: Integration testing                 ← WAIT FOR A + B
    → Test that all imports work
    → Run small manual tests in a scratch .py file
    → Fix any import errors

[ ] Step C-3: Write notebook/capstone.ipynb       ← WAIT FOR A + B
    → Section 1: Introduction
    → Section 2: Dataset A exploration
    → Section 3: Grid search Phase 1
    → Section 4: BST introspection
    → Section 5: Dataset B exploration
    → Section 6: Rebuild + benchmarks
    → Section 7: Transfer analysis
    → Section 8: Conclusion
    → COMMIT: "docs: complete capstone notebook"
```

---

## HANDOFF CHECKLIST — Person to Person

### Person A → Person B (after Step A-3)
Person A writes a quick message or posts in your group chat:

```
"registry.py is done. You can now import like this:

from bst_toolkit.registry import HyperparamRegistry

reg = HyperparamRegistry()
reg.add_trial(0.9533, {'n_estimators': 100, 'max_depth': 5})
print(reg.best())   # should print the node
print(reg.summary())

Make sure you git pull before starting grid_search.py"
```

### Person A → Person B (after Step A-4)
```
"rebuild.py is done. You can import:

from bst_toolkit.rebuild import rebuild_naive, rebuild_shuffled, rebuild_balanced

Each function takes (registry, evaluate_fn, dataset)
and returns a new HyperparamRegistry"
```

### Person B → Person C (after Steps B-1, B-2, B-3)
```
"All ml_toolkit and data files are done.

To load data:
  from data.download import load_wdbc, load_banknote
  (or just: import subprocess; subprocess.run(['python', 'data/download.py']))

To run grid search:
  from ml_toolkit.grid_search import grid_search
  registry_A = grid_search(param_grid, evaluate_fn, (X, y), verbose=True)

To run transfer analysis:
  from ml_toolkit.transfer import analyse_transfer
  report = analyse_transfer(registry_A, registry_B)"
```

### Person A → Person C (after all A steps)
```
"All bst_toolkit files are done. Key imports for notebook:

from bst_toolkit.registry import HyperparamRegistry
from bst_toolkit.rebuild import rebuild_balanced, rebuild_naive, rebuild_shuffled

reg.inorder()        # sorted list of all nodes
reg.top_k(5)         # top 5 results
reg.is_balanced()    # True/False
reg.summary()        # dict with stats"
```

---

## PARALLEL WORK TIMELINE

```
Day 1-2
  Person A: node.py + bst.py
  Person B: download.py
  Person C: timer.py   ← can finish this in a few hours

Day 3-4
  Person A: registry.py  ← CRITICAL PATH
  Person B: testing download.py, reading grid_search spec
  Person C: plan notebook structure, write Section 1 text

Day 5
  Person A: rebuild.py
  Person B: grid_search.py  ← starts when A-3 is done
  Person C: integration tests

Day 6-7
  Person A: help review/test
  Person B: transfer.py  ← starts when A-4 is done
  Person C: notebook sections 2-5

Day 8
  Person B: done
  Person C: notebook sections 6-8
  ALL: final review + commit + tag v1.0
```

---

## COMMUNICATION RULE

Every time someone finishes a file, they must:

1. **Push to GitHub** — `git push origin main`
2. **Post in group chat** — "Done with X.py, you can pull and use it"
3. **Show a quick test output** — paste 3-4 lines proving it works

---

## QUICK TEST COMMANDS (Person A runs these to verify)

```python
# Paste this in Python to test node.py + bst.py
from bst_toolkit.node import TrialNode
from bst_toolkit.bst import BST

bst = BST()
bst.insert(0.85, {'n_estimators': 50})
bst.insert(0.92, {'n_estimators': 100})
bst.insert(0.78, {'n_estimators': 200})

print(len(bst))           # 3
print(bst.find_max())     # score=0.92
print(bst.find_min())     # score=0.78
print([n.score for n in bst.inorder()])  # [0.78, 0.85, 0.92]
```

```python
# Paste this to test registry.py
from bst_toolkit.registry import HyperparamRegistry

reg = HyperparamRegistry()
reg.add_trial(0.85, {'n_estimators': 50})
reg.add_trial(0.92, {'n_estimators': 100})
reg.add_trial(0.78, {'n_estimators': 200})
reg.add_trial(0.95, {'n_estimators': 150})

print(reg.best())         # score=0.95
print(reg.top_k(2))       # [0.95, 0.92]
print(reg.summary())      # dict with count=4, etc.
```

```python
# Person C test for timer.py
from benchmarks.timer import timed, benchmark

@timed
def slow_function():
    total = 0
    for i in range(100000):
        total += i
    return total

slow_function()            # prints: slow_function ran in X.XX ms
```
