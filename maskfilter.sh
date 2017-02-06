#!/bin/bash
for f in $(find $1 -name 'ip_*.vcf' -print)
do
	grep -i '^#' $f > "patient_${f##./}"
	bedtools intersect -a $f -b $2 >> "patient_${f##./}"
done
