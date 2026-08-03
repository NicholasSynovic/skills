from argparse import ArgumentParser, Namespace
from pathlib import Path
import re
from yaml import safe_load

def cli() -> Namespace:
    parser: ArgumentParser = ArgumentParser(prog="Cluster SKILLS.md", description="Given a directory of agent skills, run unsupervised clustering algorithms to identify similar skills based on their top level metadata", epilog="Skills are provided from skills.sh",)
    parser.add_argument(
            "-d",
            "--dir", type=lambda x: Path(x).absolute(), required=True,
            )
    return parser.parse_args()

def directory_walk(dir_path: Path) -> list[Path]:
    data: list[Path] = []

    fp: Path
    for fp in dir_path.iterdir():
        if fp.is_file() and fp.name == "SKILL.md":
            data.append(fp)
        elif fp.is_dir():
            data.extend(directory_walk(dir_path=fp))
        else:
            pass
            
    return data

def _get_metadata(skill_fp: Path) -> str:
    regex: str = r"^---\r?\n([\s\S]*?)\r?\n---"
    with open(file=skill_fp, mode="r") as fp:
        match: re.Match[str] | None = re.match(pattern=regex, string=fp.read(), flags=re.M | re.S)        
        return match.group(1).strip() if match is not None else ""

def load_skills(skill_paths: list[Path]) -> list[dict]:
    data: list[dict] = []

    skill_path: Path
    for skill_path in skill_paths:
       data.append(safe_load(_get_metadata(skill_fp=skill_path)))

    return data


def main() -> None:
    args: Namespace = cli()

    skill_paths: list[Path] = directory_walk(dir_path=args.dir)

    from pprint import pprint as print 
    print(load_skills(skill_paths))

    



if __name__ == "__main__":
    main()
