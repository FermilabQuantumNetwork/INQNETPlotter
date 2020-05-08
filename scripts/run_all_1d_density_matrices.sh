#!/bin/bash

#no-spools
python python/make_density_matrix_spools_1d.py --teleportation_type early --output_file_name ../data/CQNET_March2020/results/density_matrix_no_spools_early_cqnet_april2020.pdf
python python/make_density_matrix_spools_1d.py --teleportation_type late --output_file_name ../data/CQNET_March2020/results/density_matrix_no_spools_late_cqnet_april2020.pdf
python python/make_density_matrix_spools_1d.py --teleportation_type plus --output_file_name ../data/CQNET_March2020/results/density_matrix_no_spools_plus_cqnet_april2020.pdf
#spools
python python/make_density_matrix_spools_1d.py --teleportation_type early --spools --output_file_name ../data/CQNET_March2020/results/density_matrix_spools_early_cqnet_april2020.pdf
python python/make_density_matrix_spools_1d.py --teleportation_type late --spools --output_file_name ../data/CQNET_March2020/results/density_matrix_spools_late_cqnet_april2020.pdf
python python/make_density_matrix_spools_1d.py --teleportation_type plus --spools --output_file_name ../data/CQNET_March2020/results/density_matrix_spools_plus_cqnet_april2020.pdf

