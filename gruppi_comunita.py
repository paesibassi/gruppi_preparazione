#!/usr/local/bin/python3

import argparse
import random
from gruppi_preparazione.classes import AllMembers


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', type=int, help='Specify how many members per group')
    parser.add_argument('-r', '--remove', nargs='*', help='Remove members from the list')
    args = parser.parse_args()
    return vars(args)


def copy_list(members):
    members_list = [(x, len(x)) for x in members]
    return members_list


def remove_members(members_list, to_remove):
    for nome in to_remove:
        members_list.remove((nome, len(nome)))
    return members_list


def generate_groups(members, members_per_group, to_remove=None):
    members = copy_list(members)
    members = remove_members(members, to_remove)
    groups = []
    while len(members) > 0:
        group, people = [], 0
        while people < members_per_group and len(members) > 0:
            member = members.pop(random.randrange(len(members)))
            people += member[1]
            group.append(member[0])
        groups.append(group)
    return groups


def format_groups(members, members_per_group, to_remove):
    group = generate_groups(members, members_per_group, to_remove)
    for g, group in enumerate(group, start=1):
        print('Gruppo', g, end=': ')
        components = len(group)
        for m, member in enumerate(group, start=1):
            num_pers = len(member)
            if num_pers == 1:
                print(member[0], end='')
            elif num_pers == 2:
                print(member[0], '&', member[1], end='')
            else:
                raise ValueError('Only single members or couples are supported.')
            if m < components:
                print(', ', end='')
        print('')
    return None


def main():
    args = get_arguments()
    to_remove = []
    for name in args.get('remove'):
        name = tuple(name.split(','))
        to_remove.append(name)
    to_remove = tuple(to_remove)
    print('Escludo i seguenti membri dai gruppi: {r}'.format(r=to_remove))
    members_per_group = args.get('number')
    print('Genero gruppi di {n} persone'.format(n=members_per_group))
    all_members = AllMembers()
    format_groups(all_members.get_members(), members_per_group, to_remove)


if __name__ == '__main__':
    main()
