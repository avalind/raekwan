#!/bin/bash
# Create a sample specific mask for the amplicon panel.
cd $1
for filename in $(find $1 -name '*table.done' -print)
do
	SAMPLENAME=$(basename $PWD)
	tail -n +2 $filename >> all.txt
done
awk -f ~/code/wyoming/table_filter.awk all.txt \
	| ~/code/wyoming/transform.py \
        | sort \
	| uniq > "${SAMPLENAME}_samplemask.bed"

