echo 'ORDER\tCONTAINER ID\tNAMES'
docker ps | awk 'NR > 1 {print NR-1 "\t" $1 "\t" $NF}'
