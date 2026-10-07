"""Учебный AST-мутационный тестер для number_filter.py.

Каждый мутант меняет ровно один узел синтаксического дерева и прогоняется
через неизменный набор unittest. Исходные файлы не модифицируются.
"""

import ast
import copy
import io
import json
from pathlib import Path
import types
import unittest

import number_filter
import test_number_filter

ROOT = Path(__file__).resolve().parent


def run_suite(module):
    test_number_filter.nf = module
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_number_filter)
    return unittest.TextTestRunner(stream=io.StringIO()).run(suite)


def replace_node(tree, target_index, replacement):
    mutant = copy.deepcopy(tree)
    target = list(ast.walk(mutant))[target_index]
    ast.copy_location(replacement, target)
    for parent in ast.walk(mutant):
        for field, value in ast.iter_fields(parent):
            if value is target:
                setattr(parent, field, replacement)
                return ast.fix_missing_locations(mutant)
            if isinstance(value, list):
                for pos, item in enumerate(value):
                    if item is target:
                        value[pos] = replacement
                        return ast.fix_missing_locations(mutant)
    return ast.fix_missing_locations(mutant)


def mutations(tree):
    compare_ops = {
        ast.Lt: ast.LtE,
        ast.LtE: ast.Lt,
        ast.Gt: ast.GtE,
        ast.GtE: ast.Gt,
        ast.Eq: ast.NotEq,
        ast.NotEq: ast.Eq,
        ast.Is: ast.IsNot,
        ast.IsNot: ast.Is,
    }

    for index, node in enumerate(ast.walk(tree)):
        variants = []

        if isinstance(node, ast.Compare):
            for position, operator in enumerate(node.ops):
                if type(operator) in compare_ops:
                    replacement = copy.deepcopy(node)
                    replacement.ops[position] = compare_ops[type(operator)]()
                    variants.append(
                        (f"{type(operator).__name__} -> {type(replacement.ops[position]).__name__}", replacement)
                    )

        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
            replacement = copy.deepcopy(node)
            replacement.op = ast.FloorDiv()
            variants.append(("% -> //", replacement))

        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            variants.append(("remove not", copy.deepcopy(node.operand)))

        for description, replacement in variants:
            yield node.lineno, description, replace_node(tree, index, replacement)


def main():
    baseline = run_suite(number_filter)
    if not baseline.wasSuccessful():
        raise SystemExit("Baseline tests must pass before mutation testing")

    tree = ast.parse((ROOT / "number_filter.py").read_text(encoding="utf-8"))
    records = []

    for mutant_id, (line, description, mutant_tree) in enumerate(mutations(tree), 1):
        module = types.ModuleType("number_filter")
        try:
            exec(compile(mutant_tree, str(ROOT / "number_filter.py"), "exec"), module.__dict__)
        except Exception as error:
            records.append({
                "id": mutant_id,
                "line": line,
                "mutation": description,
                "status": "invalid",
                "error": repr(error),
            })
            continue

        result = run_suite(module)
        failures = [str(test) for test, _ in result.failures + result.errors]
        records.append({
            "id": mutant_id,
            "line": line,
            "mutation": description,
            "status": "survived" if result.wasSuccessful() else "killed",
            "detecting_tests": failures,
        })

    test_number_filter.nf = number_filter

    killed = sum(r["status"] == "killed" for r in records)
    survived = sum(r["status"] == "survived" for r in records)
    invalid = sum(r["status"] == "invalid" for r in records)
    valid = killed + survived
    score = 100.0 * killed / valid if valid else 0.0

    payload = {
        "total": len(records),
        "killed": killed,
        "survived": survived,
        "invalid": invalid,
        "mutation_score": round(score, 2),
        "mutants": records,
    }
    (ROOT / "mutation_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Mutants: {len(records)}")
    print(f"Killed: {killed}")
    print(f"Survived: {survived}")
    print(f"Invalid: {invalid}")
    print(f"Mutation score: {score:.2f}%")
    if survived:
        print("Survived mutants:")
        for r in records:
            if r["status"] == "survived":
                print(f"  #{r['id']} line {r['line']}: {r['mutation']}")


if __name__ == "__main__":
    main()
