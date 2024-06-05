
import axiomic
import os
import argparse
import rich
import dataclasses
from typing import List


@dataclasses.dataclass
class ParamListTable:
    param_ref: List[str]
    file_path: List[str]
    value_preview: List[str]


def print_param_list_table(table: ParamListTable):
    table_rows = []
    for param_ref, file_path, value_preview in zip(table.param_ref, table.file_path, table.value_preview):
        table_rows.append([param_ref, file_path, value_preview])
    table_console = rich.table.Table(show_header=True, header_style="bold blue")
    table_console.add_column("Param Ref")
    table_console.add_column("File Path")
    table_console.add_column("Value Preview")
    for row in table_rows:
        table_console.add_row(*row)
    console = rich.console.Console()
    console.print(table_console)


def _recur_dir(dirname):
    filenames = []

    if os.path.isdir(dirname):
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            if os.path.isdir(filepath):
                sub_names = _recur_dir(filepath)
                filenames.extend(sub_names)
            else:
                filenames.append(filepath)

    return filenames


def path_to_param_ref(p):
    if not p.startswith('p/'):
        raise ValueError(f"Invalid param path: {p}")
    part = p[2:].replace('/', '.')
    if part.endswith('.txt'):
        part = part[:-4]
    return f'P.{part}'


def get_param_preview(data_root, param_path):
    full_path = os.path.join(data_root, param_path)
    with open(full_path, 'r') as file:
        content = file.read().replace('\n', ' ')
    return content[:60]


def list_param_files(data_rot):
    filenames = _recur_dir(os.path.join(data_rot, 'p'))
    # strip data_rot prefix
    filenames = [filename[len(data_rot):] for filename in filenames]
    return filenames


def build_param_table(data_rot):
    param_file_list = list_param_files(data_rot)

    table = ParamListTable([], [], [])

    for param_path in param_file_list:
        table.param_ref.append(path_to_param_ref(param_path))
        table.file_path.append(os.path.join(data_rot, param_path))
        table.value_preview.append(get_param_preview(data_rot, param_path))
    return table


def handle_create_param(data_rot, name):
    if not name.startswith('P.'):
        raise ValueError(f"Invalid param name: {name}")
    filepath = os.path.join(data_rot, name.replace('.', '/') + '.txt')

    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            file.write("")
    
    print(f'Created file: {filepath}')


def main():
    parser = argparse.ArgumentParser(description="Axiomic Data Tool")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # Create the parser for the "list" subcommand
    list_parser = subparsers.add_parser("list", help="List parameters in Axiomic data root")
    list_parser.add_argument("--data_rot", help="Path to Weave data root")

    # Create the parser for the "create" subcommand
    create_parser = subparsers.add_parser("create", help="Create a new parameter")
    create_parser.add_argument("--data_rot", help="Path to Axiomic data root")
    create_parser.add_argument("name", help="Name of the parameter")

    args = parser.parse_args()

    if args.subcommand == "list":
        param_table = build_param_table(args.data_rot)
        print_param_list_table(param_table)
    elif args.subcommand == "create":
        handle_create_param(args.data_rot, args.name)
    else:
        print("Invalid subcommand")

if __name__ == "__main__":
    main()
    