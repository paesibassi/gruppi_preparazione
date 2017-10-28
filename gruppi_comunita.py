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
    path = args.get('file')
    weekday = args.get('weekday')
    print('Genero gruppi escludendo membri per il giorno: {w}'.format(w=weekday))
    members_per_group = args.get('number')
    print('Genero gruppi di {n} persone'.format(n=members_per_group))
    return path, members_per_group, weekday


def main():
    path, members_per_group, weekday = assign_arguments()

    all_members = gr.AllMembers(path)
    all_members.print_groups(members_per_group, weekday)


if __name__ == '__main__':
    main()
