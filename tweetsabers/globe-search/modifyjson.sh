
#To understand the the data::
#cat tweetdata.json.clean | tr ',' '\n' | awk 'BEGIN{i=0}{arr[i]=$0;i++;}END{for (i=2;i<NR;i+=3) c+=arr[i]; for(i=2;i<NR;i+=3)  print arr[i-2],",", arr[i-1], ","arr[i], ",",arr[i]}' | tr '\n' ',' > data.json

cat tweetdata.json.clean | tr ',' '\n' | awk 'BEGIN{i=0}{arr[i]=$0;i++;}END{for (i=2;i<NR;i+=3) c+=arr[i]; for(i=2;i<NR;i+=3)  print arr[i-2],",", arr[i-1], ","arr[i]i/c, ",",arr[i]}' | tr '\n' ',' > data.json


