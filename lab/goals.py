import json
import sys

from wcmatch import fnmatch as wcfnmatch

from coverage.results import Numbers


def get_data():
    with open("coverage.json") as j:
        return json.load(j)

def select_files(files, pat):
    flags = wcfnmatch.NEGATE
    selected = [f for f in files if wcfnmatch.fnmatch(f, pat, flags=flags)]
    return selected

data = get_data()
pat = sys.argv[1:]
all_files = list(data["files"].keys())
selected = select_files(all_files, pat)

total = Numbers(precision=3)
for sel in selected:
    sel_summ = data["files"][sel]["summary"]
    total += Numbers(
        n_statements=sel_summ["num_statements"],
        n_excluded=sel_summ["excluded_lines"],
        n_missing=sel_summ["missing_lines"],
        n_branches=sel_summ["num_branches"],
        n_partial_branches=sel_summ["num_partial_branches"],
        n_missing_branches=sel_summ["missing_branches"],
        )

print(total.pc_covered)
print(total.pc_covered_str)
