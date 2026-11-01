"""Exercise semantic-release and the real build hook in disposable repositories.

Run with: uv run --no-project --with python-semantic-release==10.6.1 python scripts/check_release.py
No commits/tags are created in the working repository; no push or publication is allowed.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import tomlkit


def run(*command, cwd, env):
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(command)} failed:\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def main():
    root = Path(__file__).resolve().parents[1]
    psr = shutil.which("semantic-release")
    if psr is None:
        raise RuntimeError("Run this script with python-semantic-release==10.6.1 installed")
    config = tomlkit.parse((root / "pyproject.toml").read_text())
    current = config["project"]["version"]
    major, minor, patch = map(int, current.split("."))
    # All three are inferred from conventional titles, never forced CLI bumps.
    cases = [
        ("fix: exercise patch release", f"{major}.{minor}.{patch + 1}"),
        ("feat: exercise feature release", f"{major}.{minor + 1}.0"),
        ("feat!: exercise breaking release", f"{major + 1}.0.0"),
    ]
    # Do not inherit tokens, GitHub output files or the user's global Git hooks.
    env = {
        **{k: v for k, v in os.environ.items() if not k.startswith("GITHUB_") and k != "GH_TOKEN"},
        "GH_TOKEN": "",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
    }
    with tempfile.TemporaryDirectory(prefix="hilbertplot-release-check-") as temporary:
        for number, (title, expected) in enumerate(cases):
            repo = Path(temporary) / str(number)
            repo.mkdir()
            for name in (
                "pyproject.toml",
                "uv.lock",
                "README.md",
                "CHANGELOG.md",
                "LICENSE",
                ".gitignore",
            ):
                shutil.copy2(root / name, repo / name)
            for name in ("src", "scripts"):
                shutil.copytree(
                    root / name, repo / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
                )
            git = ("git", "-C", str(repo))
            run(*git, "init", "-b", "main", cwd=repo, env=env)
            run(*git, "config", "user.name", "Release check", cwd=repo, env=env)
            run(*git, "config", "user.email", "release-check@example.invalid", cwd=repo, env=env)
            run(*git, "config", "commit.gpgsign", "false", cwd=repo, env=env)
            run(*git, "config", "tag.gpgsign", "false", cwd=repo, env=env)
            run(
                *git,
                "remote",
                "add",
                "origin",
                "https://github.com/El3ssar/hilbertplot.git",
                cwd=repo,
                env=env,
            )
            run(*git, "add", ".", cwd=repo, env=env)
            run(*git, "commit", "-m", "chore: initial fixture", cwd=repo, env=env)
            run(*git, "tag", f"v{current}", cwd=repo, env=env)
            run(*git, "commit", "--allow-empty", "-m", title, cwd=repo, env=env)
            run(psr, "version", "--no-push", "--no-vcs-release", cwd=repo, env=env)
            project = tomlkit.parse((repo / "pyproject.toml").read_text())
            lock = tomlkit.parse((repo / "uv.lock").read_text())
            package = next(p for p in lock["package"] if p["name"] == "hilbertplot")
            source = (repo / "src/hilbertplot/__init__.py").read_text()
            declared = re.search(r'__version__ = "([^"]+)"', source).group(1)
            assert project["project"]["version"] == package["version"] == declared == expected
            changed = run(*git, "show", "--pretty=", "--name-only", "HEAD", cwd=repo, env=env)
            assert "uv.lock" in changed.splitlines(), "lockfile missing from release commit"
            assert run(*git, "rev-parse", "HEAD", cwd=repo, env=env) == run(
                *git, "rev-list", "-n", "1", f"v{expected}", cwd=repo, env=env
            )
            assert not run(*git, "status", "--porcelain", cwd=repo, env=env)
            run("uv", "lock", "--check", cwd=repo, env=env)
            assert list((repo / "dist").glob(f"hilbertplot-{expected}-*.whl"))
            print(f"{title!r} -> {expected}: versions, committed lock, tag and build OK")


if __name__ == "__main__":
    main()
