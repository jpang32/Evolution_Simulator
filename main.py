from microbe import Microbe
from genome import Genome

m = Microbe(3)

## Test random Genome creation and color generation for Microbe

print(m.genome)
print(Microbe.get_brain_structure())
print(m.color)

## Test passing down genes from two Microbes. Also add mutation.

# Passes down two genes from gene class itself
g1 = Genome(3, Microbe)
g2 = Genome(3, Microbe)
print(g1)
print(g2)

g3 = Genome.from_genomes(g1, g2)
print(g3)

# Add two Microbes together to create a new one with merged genome
m1 = Microbe(4)
m2 = Microbe(4)

print(m1.genome)
print(m2.genome)

m3 = m1 + m2
print(m3.genome)

#Add two Genomes together
g1 = Genome(3, Microbe)
g2 = Genome(3, Microbe)

print(g1)
print(g2)

g3 = g1 + g2

print(g3)
