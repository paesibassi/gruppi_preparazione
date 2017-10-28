#!/usr/local/bin/python3

import argparse
import gruppi_preparazione.classes as gr


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', type=int, help='Specify how many members per group')
    parser.add_argument('-r', '--remove', nargs='*', help='Remove members from the list')
    args = parser.parse_args()
    return vars(args)


def assign_arguments(args):
    to_remove = []
    # for name in args.get('remove'):
    #     name = tuple(name.split(','))
    #     to_remove.append(name)
    # print('Escludo i seguenti membri dai gruppi: {r}'.format(r=to_remove))

    members_per_group = args.get('number')
    print('Genero gruppi di {n} persone'.format(n=members_per_group))

    return members_per_group, to_remove


def main():
    args = get_arguments()
    members_per_group, to_remove = assign_arguments(args)  # TODO capture weekday

    all_members = gr.AllMembers('persone.json')  # TODO capture path
    print(all_members.get_groups(members_per_group, 'saturday'))
    all_members.get_groups_string(members_per_group, 'saturday')


if __name__ == '__main__':
    main()
