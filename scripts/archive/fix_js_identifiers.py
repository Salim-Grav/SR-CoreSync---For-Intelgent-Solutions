# -*- coding: utf-8 -*-
with open('fr/demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix known corrupted identifiers
c = c.replace('const currentEn attente', 'const currentPending')
c = c.replace('currentEn attente', 'currentPending')
c = c.replace('querySelectorTout', 'querySelectorAll')

# Check if netMontant or vatMontant exist
# In English they are netAmount, vatAmount
c = c.replace('netMontant', 'netAmount')
c = c.replace('vatMontant', 'vatAmount')

with open('fr/demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied identifier fixes!")
