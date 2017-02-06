BEGIN { OFS="\t" }
{
	# Since Excel exporting fucks things up.
	# gsub(",",".",$10)
	# remove indels longer than 10bp and variants with AF < 10%
	if(length($4) <= 10 && length($5) <= 10 && $10 > "0.10") {
		# Remove synonymous variants
		if($7 != "synonymous_SNV") {
			# require at least 10 reads supporting the variant
			split($11, allelic_depths, ",")
			if(allelic_depths[2] >= 10) {
				# require a total coverage of the site of atleast 30x
				if($12 >= 30) {
					print $2,$3
				}
			}
		}
	}
}
