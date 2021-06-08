# import time
import os
import ast
import json

from config import Config

from helpers.logger import get_app_logger

from models.ad_object import AdObject

logger = get_app_logger("FACEBOOK_SDK_PARSER")


def class_name_to_readable(className: str):

    output = ""
    for x in className:
        output += f"_{x.lower()}" if x.isupper() else x

    return output[1:]


def parse_tree(filename, tree):

    node = {
        "sdk_filename": filename,
        "class_name": None,
        "readable_name": None,
        "fields": [],
    }

    for ctx in tree.body:

        # WE TARGET THE FIRST CLASS FROM SDK ADOBJECT
        # class XYZ():
        #     class Field(): -> contain all request params
        #
        #     _field_types {
        #       name : string,
        #       url : string
        #     }

        # https://docs.python.org/3/library/ast.html#ast.ClassDef
        if isinstance(ctx, ast.ClassDef):

            node["class_name"] = ctx.name
            node["readable_name"] = class_name_to_readable(ctx.name)

            for ctx2 in ctx.body:

                # https://docs.python.org/3/library/ast.html#ast.Assign
                # https://docs.python.org/3/library/ast.html#ast.Name
                # https://docs.python.org/3/library/ast.html#ast.Dict
                if (
                    isinstance(ctx2, ast.Assign)
                    and ctx2.targets[0].id == "_field_types"
                ):

                    # ctx2.value -> ast.Dict()

                    keys = ctx2.value.keys
                    values = ctx2.value.values

                    for index, key in enumerate(keys):

                        node["fields"].append(
                            {
                                "field": str(key.value),
                                "type": str(values[index].value),
                            }
                        )

            node["fields"] = json.dumps(node["fields"])

    return node


def main():

    FULL_FILES_LIST = os.listdir(Config.FULL_PATH)

    ADOBJECTS_FILES = list(filter((lambda x: ".py" in x), FULL_FILES_LIST))

    TO_PROCESS = [f for f in ADOBJECTS_FILES if f not in Config.EXCLUSION_LIST]

    logger.info(f"**** FOUND {len(TO_PROCESS)} files to parse ****\n")

    AdObject().reset_ad_object()

    for x in TO_PROCESS:

        node = {"class_name": None, "readable_name": None, "fields": []}

        with open(f"{Config.FULL_PATH}/{x}", "r") as source_file:
            tree = ast.parse(source_file.read())

        node = parse_tree(filename=x, tree=tree)

        try:
            logger.info(f" ++ TRYING TO INSERT : {node['class_name']}")

            AdObject().add_ad_object(node)

        except Exception as error:

            logger.error(f"Can't insert node : {error}")

    logger.info(f"**** PARSING DONE ****\n")


if __name__ == "__main__":
    main()