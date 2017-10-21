class AllMembers:
    def __init__(self, members=None):
        if members is None:
            self._members = (('Ana',),
                             ('Enrique', 'Concha'),
                             ('Ester',),
                             ('Federico', 'Teresa'),
                             ('Giancarlo',),
                             ('Giuseppe', 'Noemi'),
                             ('Isabel',),
                             ('Juanita',),
                             ('Marcelo', 'Chantal'),
                             ('Maria',),
                             ('Marta',),
                             ('Michele', 'Federica'),
                             ('Philippe',),
                             ('Tommaso', 'Laura')
                             )
        else:
            self._members = members

    def get_members(self):
        return self._members

    def get_members_list(self):
        members_list = [(x, len(x)) for x in self._members]
        return members_list
