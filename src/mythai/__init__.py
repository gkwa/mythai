import argparse
import dataclasses
import logging
import pathlib
import typing

from . import main2
from . import tasks as taskmod

__project_name__ = "mythai"


@dataclasses.dataclass
class MyDataClass:
    skip_publish: bool
    position: int
    whimsicle_name: str
    provisioner: str
    packer_tpl: str
    packer_rendered: str = ""
    image: str = ""
    output_image: str = dataclasses.field(init=False)
    task: str = ""

    def __post_init__(self):
        y = f"{self.position:03d}"
        self.output_image = f"{y}-{self.task or self.whimsicle_name}"
        self.packer_rendered = f"{y}-ubuntu-{self.task or self.whimsicle_name}.pkr.hcl"


def doit(data: typing.List[MyDataClass], outdir: pathlib.Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(data, 1):
        index_formatted = f"{index:03d}"
        provisioner_tpl = pathlib.Path(item.provisioner)

        provisioner_rendered = outdir / provisioner_tpl.with_suffix("")
        x = outdir / f"{index_formatted}-{provisioner_tpl.with_suffix('')}"

        y = pathlib.Path(x)

        logging.debug(
            f"Rendering provisioner template: {provisioner_tpl} to {provisioner_rendered}"
        )
        out = main2.render_template(provisioner_tpl.name, data=item)
        y.write_text(out)

        if item.task:
            y = y.rename(outdir / f"{index_formatted}-{item.task}.sh")

        packer_tpl = pathlib.Path(item.packer_tpl)
        packer_rendered = outdir / item.packer_rendered
        logging.debug(f"Rendering packer template: {packer_tpl} to {packer_rendered}")

        image = item.image

        out = main2.render_template(
            packer_tpl.name,
            data={
                "skip_publish": str(item.skip_publish).lower(),
                "script": y.name,
                "image": image,
                "output_image": item.output_image,
            },
        )
        packer_rendered.write_text(out)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="increase output verbosity"
    )
    parser.add_argument(
        "--outdir", default="mythai", help="output directory"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    outdir = pathlib.Path(args.outdir)
    items: typing.List[MyDataClass] = []

    whimsicle_names = [
        "wacky-wombat",
        "jolly-penguin",
    ]

    skip_publish = False

    for whimsicle_name in whimsicle_names:
        image = (
            "images:ubuntu/focal/cloud" if not items else items[len(items) - 1].output_image
        )

        data = MyDataClass(
            skip_publish=skip_publish,
            position=len(items) + 1,
            whimsicle_name=whimsicle_name,
            provisioner=f"{whimsicle_name}.sh.j2",
            packer_tpl="ubuntu.pkr.hcl.j2",
            image=image,
        )
        items.append(data)

    tasks = taskmod.main()
    for task in tasks:
        data = MyDataClass(
            skip_publish=True,
            position=len(items) + 1,
            whimsicle_name="larry-luster",
            provisioner="larry-luster.sh.j2",
            packer_tpl="ubuntu.pkr.hcl.j2",
            image="002-jolly-penguin",
            task=task,
        )

        items.append(data)

    doit(items, outdir)

    return 0
