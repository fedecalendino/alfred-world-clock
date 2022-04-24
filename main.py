import sys

from workflow import Workflow


def main(workflow):
    workflow.add_item(
        title="title",
        arg="arg",
        copytext="copytext",
        icon="icon.png",
        valid=True,
    )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
