import gruppi_preparazione.classes as gr

def test_AllMembers_init():
    ana = ('Ana',)
    ruiz = (('Ana',),('Enrique','Concha'))
    assert len(gr.AllMembers().get_members_list()) == 14
    assert len(gr.AllMembers(ana).get_members_list()) == 1
    assert len(gr.AllMembers(ruiz).get_members_list()) == 2

    assert (('Federico', 'Teresa'), 2) in gr.AllMembers().get_members_list()
