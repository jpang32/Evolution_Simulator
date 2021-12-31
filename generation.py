from __future__ import annotations
from microbe import Microbe
import random


class Generation:

    count = 0
    size = 500

    def __init__(self):
        self.members = []

    # This needs to be fixed when we figure out how to deal with killing
    # microbes in environment
    @classmethod
    def next_gen_from_members_list(cls, members):
        g = Generation()
        g.members = members

        while len(g) < Generation.size:
            j = random.randint(0, len(members) - 1)
            k = random.randint(0, len(members) - 1)
            new_member = members[j] + members[k]
            # TODO: Add member to environment
            g.members.append(new_member)

        Generation.count += 1
        print('Generation ', Generation.count)

        return g

    def add_members(self, m_list):
        self.members = m_list

    def __len__(self):
        return len(self.members)

    # TODO: Create Iterator?
