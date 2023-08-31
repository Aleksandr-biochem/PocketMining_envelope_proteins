import sys, os
import pymol
from pymol import cmd
import gzip, bz2
import re
import string
import colorsys
import numpy as np

def read_pdb( fname ):
    if os.path.exists( fname + ".pdb.gz" ):
        return gzip.open(fname + ".pdb.gz" )
    elif os.path.exists( fname + ".pdb" ):
        return open( fname + ".pdb" )
    elif os.path.exists( fname + ".pdb.bz2" ):
        return open( fname + ".pdb.bz2" )
    else:
        return False

def metric_to_color(metric):
    if metric > 0.5:
        rgb = colorsys.hsv_to_rgb(0, (2*metric) - 1, 1)
    else:
        rgb = colorsys.hsv_to_rgb(0.55, (2*(1 - metric)) - 1, 1)

    r = rgb[0] * 255
    g = rgb[1] * 255
    b = rgb[2] * 255

    color = "0x%02x%02x%02x"%(int(r), int(g), int(b))

    return color

# get PDB file with PocketMiner predictions
pdbname = cmd.get_object_list()[0]
f = read_pdb(pdbname)
if not f:
    print("No pdb files found, exit!")
    exit(0)

# parse file to collect predicted pocket probabilities
pocket_probs = dict()
for line in f:
    if "ATOM" in line:
        data = line.split()
        res_prob = float(data[-2])
        res_id   = int(data[5]) if len(data[4]) == 1 else int(data[4][1:])
        pocket_probs[res_id] = res_prob

# recolor all structure to light gray
cmd.color('gray95')

# color residues
for res_id in pocket_probs:
    color = metric_to_color(pocket_probs[res_id])
    cmd.color(color, "resi %i"%res_id,)