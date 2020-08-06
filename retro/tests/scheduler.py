import sys
import unittest
import pygame
from retro.src import retro

class SandboxScheduler:
    def __init__(self):
        self.window = retro.Window(
            title='scheduler', size=(100, 100), ups=120, fps=60
        )

    def helper(self, name, frequency):
        accu = 1
        tick = 0
        clock = pygame.time.Clock()

        def step():
            nonlocal accu, tick
            accu += clock.tick()
            if tick % frequency == 0:
                print(name, 1000 * tick / accu)
            tick += 1

        return step

    def loop(self):
        self.window.loop(
            self.helper('U', self.window.ups),
            self.helper('R', self.window.fps),
        )

class TestScheduler(unittest.TestCase):
    @classmethod
    def str2schedule(cls, ustr, rstr):
        return tuple(
            ((uc != '_'), (rc != '_'))
            for uc, rc in zip(ustr, rstr)
        )

    def template_scheduling(self, ups, fps, ctrl_ustr, ctrl_rstr):
        highps = ups if ups >= fps else fps
        control = self.str2schedule(ctrl_ustr, ctrl_rstr) * 4
        schedule = retro.Window.scheduler(ups, fps)
        schedule = tuple( schedule()[1:] for _ in control )
        self.assertEqual(control, schedule)

    def test_signature(self):
        retro.Window.scheduler(ups = 30, fps = 15)

    def test_eq(self):
        self.template_scheduling(
            ups = 20, fps = 20,
            ctrl_ustr = 'UUUUUUUUUUUUUUUUUUUU',
            ctrl_rstr = 'RRRRRRRRRRRRRRRRRRRR',
        )

    def test_half(self):
        self.template_scheduling(
            ups = 20, fps = 10,
            ctrl_ustr = 'UUUUUUUUUUUUUUUUUUUU',
            ctrl_rstr = 'R_R_R_R_R_R_R_R_R_R_',
        )

    def test_gt(self):
        self.template_scheduling(
            ups = 20, fps = 15,
            ctrl_ustr = 'UUUUUUUUUUUUUUUUUUUU',
            ctrl_rstr = 'RRR_RRR_RRR_RRR_RRR_',
        )

    def test_lt(self):
        self.template_scheduling(
            ups = 17, fps = 20,
            ctrl_ustr = 'UUUUUUU_UUU_UUUUUUU_',
            ctrl_rstr = 'RRRRRRRRRRRRRRRRRRRR',
        )

    def test_odd(self):
        self.template_scheduling(
            ups = 9, fps = 13,
            ctrl_ustr = 'UUU_U_UUU_U_U',
            ctrl_rstr = 'RRRRRRRRRRRRR',
        )

if '--interactive' in sys.argv:
    SandboxScheduler().loop()
else:
    unittest.main()
