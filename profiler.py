import cProfile
import pstats

import scanner

cProfile.run("scanner.main('fp.txt', 'fl.txt')")
p = pstats.Stats('restats.txt')
p.strip_dirs().sort_stats(-1).print_stats()