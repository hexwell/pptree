# -*- coding: utf-8 -*-
"""
Ettore Forigo (c) 2020
"""

from itertools import chain, zip_longest, repeat

JOINER_WIDTH = 3
DEFAULT_JOINER = ' ' * JOINER_WIDTH
CONNECTION_JOINER = '─' * JOINER_WIDTH
L_BRANCH_CONNECTOR = '─┘ '
LR_BRANCH_CONNECTOR = '─┴─'
R_BRANCH_CONNECTOR = ' └─'
L_NODE_CONNECTOR = '─┐ '
LR_NODE_CONNECTOR = '─┬─'
R_NODE_CONNECTOR= ' ┌─'
LEFT = 'l'
RIGHT = 'r'


def multijoin(blocks, joiners=()):
    f"""
    Take one block (list of strings) or more and join them line by line with the specified joiners

    :param blocks: [['a', ...], ['b', ...], ...]
    :param joiners: ['─', ...]
    :return: ['a─b', ...]
    """

    # find maximum content width for each block
    block_content_widths = tuple(max(map(len, block), default=0) for block in blocks)

    return tuple(

        joiner.join(

            (string or '')                 # string if present (see fillvalue below)
            .center(block_content_width)  # normalize content width across block

            for string, block_content_width in zip(line, block_content_widths)

        )

        for line, joiner in zip(zip_longest(*blocks, fillvalue=None),
                                chain(joiners, repeat(DEFAULT_JOINER))) # joiners or default

    )


def wire(block, connector):
    left_c = ' ' if connector == R_NODE_CONNECTOR else '─'
    right_c = ' ' if connector == L_NODE_CONNECTOR else '─'

    block, (left, right) = block

    if not (left or right):
        length = len(block[0])  # len of first line


        length -= 1             # ignore connector
        left = length // 2
        right = length - left

    return multijoin([[
        f'{left_c * left}{connector}{right_c * right}',
        *block
    ]])


def branch(blocks):
    wired_blocks = tuple(map(lambda blk: wire(blk, LR_NODE_CONNECTOR), blocks))

    return multijoin(wired_blocks, (CONNECTION_JOINER,))


def branch_dir(blocks, direction):
    if direction == LEFT:
        direction = -1
        connector = R_NODE_CONNECTOR

    elif direction == RIGHT:
        direction = 1
        connector = L_NODE_CONNECTOR

    else:
        raise ValueError('Direction should be left or right')

    blocks = tuple(blocks)

    *rest, last = blocks[::direction]

    last = wire(last, connector)
    rest = branch(rest)

    return multijoin([rest, last][::direction], (CONNECTION_JOINER,))


def connect_branches(left, right):
    joiner = (LR_BRANCH_CONNECTOR if right else L_BRANCH_CONNECTOR) if left else R_BRANCH_CONNECTOR

    return multijoin([left, right], (joiner,))


def blocklen(block):
    if block:
        return len(block[0])

    else:
        return 0
