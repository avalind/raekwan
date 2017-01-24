#!/usr/bin/env python
import argparse
import pandas as pd
from pysam import VariantFile

DEBUG = False


def strand_absolute_count(raw, alt_f=2, alt_r=2):
    """
        Filter out all variants not supported by alt_f reads in forward dir
        and alt_r reads in reverse direction
    """
    lst = raw.strip("()").split(",")
    return int(lst[2]) >= alt_f and int(lst[3]) >= alt_r


def filter_callstat(filename):
    dataset = pd.read_table(filename,
                            comment="#",
                            dtype={'contig': str, 'position': int})

    dataset = dataset[dataset.judgement != "REJECT"]
    dataset = dataset[dataset.n_alt_count == 0]
    return dataset[dataset['strand_bias_counts']
                   .map(lambda x: strand_absolute_count(x))]


def vcf_based_filters(variant):
    def __element(variant, elem="exonic"):
        if variant.info['Func.refGene'][0] == elem:
            return True
        return False

    def __bq(variant, bq_limit=30.0):
        for k in variant.samples.keys():
            if variant.samples[k]["BQ"][0] is not None:
                if DEBUG:
                    print(variant.samples[k]["BQ"])
                if variant.samples[k]["BQ"][0] >= bq_limit:
                    return True
                else:
                    return False

    if not __element(variant):
        return False

    if not __bq(variant):
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Filter Mutect 1.x variant calls based on callstats file")
    parser.add_argument("--callstat-file",
                        help="Path to callstat file from Mutect 1.x",
                        required=True)
    parser.add_argument("--vcf-file",
                        help="Path to vcf file from Mutect 1.x",
                        required=True)
    parser.add_argument("--out",
                        help="Path to file to save filtered vcf in",
                        required=True)

    args = parser.parse_args()

    filtered_callset = filter_callstat(args.callstat_file)
    variant_file = VariantFile(args.vcf_file)
    variant_out = VariantFile(args.out, "w", header=variant_file.header)

    for record in variant_file.fetch():
        if DEBUG:
            print("on record with location on chromosome {} at {}"
                  .format(record.chrom, record.pos))
        callstat_variant = filtered_callset[
            (filtered_callset.contig == record.chrom) &
            (filtered_callset.position == record.pos)]

        if not callstat_variant.empty:
            if vcf_based_filters(record):
                variant_out.write(record)

if __name__ == "__main__":
    main()
