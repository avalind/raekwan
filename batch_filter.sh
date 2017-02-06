#!/bin/bash
for f in $(find . -name '*.mutect.calls' -print)
do
	VCF_IN="${f%%.mutect.calls}_mutect.hg19_multianno.vcf"
	VCF_OUT="${f%%.mutect.calls}_true.vcf"
	echo "Running postprocessing with CALLSTAT = $f, VCF_IN = $VCF_IN, VCF_OUT=$VCF_OUT"
	python ~/code/wyoming/explore.py --callstat-file "$f" --vcf-file "$VCF_IN" --out "$VCF_OUT"
done
