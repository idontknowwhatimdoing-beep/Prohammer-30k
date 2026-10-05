"""Data revision number shared by the .gst and every .cat: the next git commit number (commits so far + 1).
New Recruit and BattleScribe compare revisions to decide whether a cached file is outdated, so it must grow with
every published change."""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def revision():
    env = os.environ.get("P30K_REVISION")
    if env:
        return int(env)
    try:
        n = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=HERE, capture_output=True, text=True,
                           check=True).stdout.strip()
        return int(n) + 1
    except Exception:
        return 1


REVISION = revision()
