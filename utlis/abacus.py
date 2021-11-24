#!/usr/bin/env python
import os


def run_abacus(pdbfilename):
    try:
        os.mkdir("abacus_jobs")
        os.chdir("abacus_jobs")
        os.system("cp ../%s ./" % (pdbfilename))
        print("[INFO: ] Running ABACUS_prepare.")
        os.system("ABACUS_prepare %s" % (pdbfilename))
        print("[INFO: ] Running ABACUS_S1S2.")
        os.system("ABACUS_S1S2 %s" % (pdbfilename))
        print("[INFO: ] Running ABACUS_singleMutationScan.")
        os.system("ABACUS_singleMutationScan %s abacus_output.txt" % (pdbfilename))
    except FileExistsError:
        os.chdir("abacus_jobs")
        if os.path.exists("./abacus_output.txt"):
            print("==" * 2)
            print("[INFO: ] ABACUS results found. Skipping.")
            print("==" * 2)
    os.chdir("../")


def parse_abacus_out():
    try:
        os.mkdir("abacus_results")
    except FileExistsError:
        pass
    longer_names = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
                    'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
                    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
                    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
                    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

    with open('tempfile', 'w') as tem:
        with open("abacus_jobs/abacus_output.txt") as abacusfile:
            for line in abacusfile:
                if line.startswith('site'):
                    wildAA = line.strip().split()[4]
                    wildAAnum = line.strip().split()[1]
                else:
                    tem.write(wildAA + ' ' + wildAAnum + ' ' + line)

    with open('abacus_results/All_ABACUS.score', 'w+') as complete:
        complete.write("#Score file formated by GRAPE from Rosetta.\n#mutation\tscore\tstd\n")
        with open('tempfile') as abacusfile:
            for line in abacusfile:
                wildAA1 = line.strip().split()[0]
                if wildAA1 in longer_names:
                    wildAAabr = longer_names[wildAA1]
                wildAAnum1 = line.strip().split()[1]
                mutAA = line.strip().split()[2]
                if mutAA in longer_names:
                    mutAAabr = longer_names[mutAA]
                sef_energy = line.strip().split()[11]
                complete.write(wildAAabr + "_" + wildAAnum1 + "_" + mutAAabr + '\t' + sef_energy + "\t" + str(0) + '\n')
            tem.close()
        complete.close()
        os.remove('tempfile')


if __name__ == '__main__':
    print("Running")
    parse_abacus_out()
