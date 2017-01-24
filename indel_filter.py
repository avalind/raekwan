#!/usr/bin/env python
import sys
from pysam import VariantFile


FISHER_LIMIT = 15.0


def main():
    """
        indel_filter.py -- post-processing filters for indels called
        with scalpel. output filtered vcf to stdout.
    """
    if len(sys.argv) < 2:
        print("Usage: {} [path to vcf file]".format(sys.argv[0]))
        sys.exit()

    vcf_file = VariantFile(sys.argv[1], "r")
    vcf_out = VariantFile("-", "w", header=vcf_file.header)

    for variant in vcf_file.fetch():
        # Keep only exonic
        if variant.info['Func.refGene'][0] == 'exonic':
            # Keep only with phred scale fisher scores above fisher_limit
            if variant.info['FISHERPHREDSCORE'] >= FISHER_LIMIT:
                # print(variant)
                vcf_out.write(variant)

if __name__ == "__main__":
    main()
