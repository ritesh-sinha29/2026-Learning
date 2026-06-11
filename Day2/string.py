name="Ritesh"    #string methods (Strings are immutable and lists are mutable)
print(name.isnumeric())
print(name.isalpha())
print(name.title())
print(name.swapcase())
print(name.upper())
print(name.lower())  
print(name.find("i"))
print(name.find("p"))
print(name.replace("i", "o"))
name1= "ritesh"
print(name.startswith("R"))
print(name1.startswith("r")) 
print(name.endswith("h"))
print(name1.endswith("H")) 
print(name.split()) 
print(name.join(name1))  
print(name.count("i")) 
print(name.count("R")) 
print(name.count("p")) 

#slice operator
#--------slice is used to break string

print(name[0:4])    # : is used to separate start and end index(4-1)