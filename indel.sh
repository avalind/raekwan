#!/bin/bash

function sample_name_from_path() {
	base="${1##*/}"
}

TEMPFILE="/temp/$1.contig_fix"

awk -f /Users/anders/code/wyoming/fix_contigs.awk $1 > $TEMPFILE
python /Users/anders/code/wyoming/indel_filter.py $TEMPFILE > 
