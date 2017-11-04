#!/usr/local/bin/python3

import argparse
import gruppi_preparazione.classes as gr


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='Specify the path to the json data file')
    parser.add_argument('-n', '--number', type=int, help='Specify how many members per group')
    parser.add_argument('-w', '--weekday', type=str, help='Specify weekday to remove members')
    args = parser.parse_args()
    return vars(args)


def assign_arguments():
    args = get_arguments()
    args = dict((k, args[k]) for k in args if args[k] is not None) # deletes the None values
    path = args.get('file', './gruppi_preparazione/tests/members_example.json')
    members_per_group = args.get('number', 4)
    print('Generating groups of {n} people'.format(n=members_per_group))
    weekday = args.get('weekday', 'saturday')
    print('Generating groups excluding members for weekday: {w}'.format(w=weekday))
    return path, members_per_group, weekday


def main():
    path, members_per_group, weekday = assign_arguments()

    all_members = gr.AllMembers(path)
    all_members.print_groups(members_per_group, weekday)


if __name__ == '__main__':
    main()
