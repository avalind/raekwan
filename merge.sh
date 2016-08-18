#!/bin/bash
cp $1 "${1}.temp"
cp $2 "${2}.temp"
bgzip "${1}.temp"
bgzip "${2}.temp"
tabix "${1}.temp.gz"
tabix "${2}.temp.gz"
bcftools concat -a "${1}.temp.gz" "${2}.temp.gz" | vcf-sort > $3
rm *.temp.gz*
