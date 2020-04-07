# A -lt B == A < B (less than)
# A -le B == A <= B (less than and equal)
# A -gt B == A > B (greater than)
# A -ge B == A >= B (greater than and equal)

# count=0
# while [ $count -le 10000 ]
# do
#   echo $count
#   # printf "Count has a value of $count\n"
#   count=$(($count+1))
#   # ((count++))
# done

docker ps | awk -F'tcp' '{print $2}' | awk '{print $1}' | xargs echo
