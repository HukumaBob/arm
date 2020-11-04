# Python3 code to demonstrate working of 
# Substring Key match in dictionary 
# Using items() + list comprehension 

# initializing dictionary 
test_dict = {'All': 1, 'have': 2, 'good': 3, 'food': 4, 'mood': {'zood': 1, 'b': 2}}

# initializing search key string 
search_key = 'ood'

# printing original dictionary 
print("The original dictionary is : " + str(test_dict))

# Using items() + list comprehension 
# Substring Key match in dictionary 
res = [val for key, val in test_dict.items() if (search_key in key and isinstance(val, dict))]

# printing result  
print("Values for substring keys : " + str(res)) 