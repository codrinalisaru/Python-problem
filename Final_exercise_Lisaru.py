import re

# 1. Open and read the information from Database.txt

input = open('Database.txt', 'r')
fileContent = input.read()
input.close()


# 2. Create 5 lists for each basic function (the prefix of the Parameter_name value indicates the basic function PpDae – DAE (DriverActivityEstimation), Ada – ADA (ActionDecisionAsil), PpRpa – RPA (ReferencePointAdjustment), PpLv – LV (LaneVerification), Asq – ASQ (ActionSuppressionQM)), where the list elements are the lines from the text file (e.g [„string line1“, „string lineX“])

lines = fileContent.split('\n')

DAEList = []
ADAList = []
RPAList = []
LVList = []
ASQList = []

for line in lines:
    if 'PpDae' in line:
        DAEList.append(line)
    elif 'Ada' in line:
        ADAList.append(line)
    elif 'PpRpa' in line:
        RPAList.append(line)
    elif 'PpLv' in line:
        LVList.append(line)
    elif 'Asq' in line:
        ASQList.append(line)

print(*DAEList, sep='\n')
print(*ADAList, sep='\n')
print(*RPAList, sep='\n')
print(*LVList, sep='\n')
print(*ASQList, sep='\n')


# 3. Define a function to create a list of dictionaries where the key and value pairs are obtain from the equality (there should be 6 pairs) (e.g. [{key1:value1, key2:value3}, {key1:value2, key2:value4}])

def parameterStringsToDictionaries(stringLines):

    keys = []
    values = []
    listOfDictionaries = []

    for line in stringLines:
        withoutBrackets = line.replace('<', '').replace('/>', '')
        words = re.split(r'" |="|"', withoutBrackets)
        words.pop()

        for index, word in enumerate(words):
            if (index % 2 == 0):
                keys.append(word)
            else:
                values.append(word)

        singleDictionary = dict(zip(keys, values))
        listOfDictionaries.append(singleDictionary)

    return listOfDictionaries


# 4. With the defined function create a single dictionary having the keys the names of the
# basic functions and the value the list of dictionaries (previously obtained) (e.g. {RPA:[{}, {}], DAE:[{}, {}]})

basicFunctionNames = ['PpDae', 'Ada', 'PpRpa', 'PpLv', 'Asq']
basicFunctionLists = [DAEList, ADAList, RPAList, LVList, ASQList]
basicFunctionDictionaries = []

for basicFunctionList in basicFunctionLists:
    basicFunctionDictionaries.append(
        parameterStringsToDictionaries(basicFunctionList))

basicFunctions = dict(zip(basicFunctionNames, basicFunctionDictionaries))

#print(basicFunctions)


# 5. Using the obtained dictionary, print the Parameter_name value where the key „value“ has array (the type is defined as: type=„type[]“)

PpDaeParameters = basicFunctions["PpDae"]
AdaParameters = basicFunctions["Ada"]
PpRpaParameters = basicFunctions["PpRpa"]
PpLvParameters = basicFunctions["PpLv"]
AsqParameters = basicFunctions["Asq"]


def hasArrayType(parameter):
    return "[]" in parameter["type"]


def filterArrayTypeParameters(parameters):
    arrayParameters = []
    for parameter in parameters:
        if hasArrayType(parameter):
            arrayParameters.append(parameter)
    return arrayParameters


print("\n\nAll parameter names for type=„type[]“:\n")
for parameter in filterArrayTypeParameters(PpDaeParameters):
    print(parameter["Parameter_name"])
for parameter in filterArrayTypeParameters(AdaParameters):
    print(parameter["Parameter_name"])
for parameter in filterArrayTypeParameters(PpRpaParameters):
    print(parameter["Parameter_name"])
for parameter in filterArrayTypeParameters(PpLvParameters):
    print(parameter["Parameter_name"])
for parameter in filterArrayTypeParameters(AsqParameters):
    print(parameter["Parameter_name"])


# 6. Using the obtained dictionary, print the Parameter_name where the key „lib:fusi “ is 1

def isFusi(parameter):
    return (parameter["lib:fusi"] == "1")


def filterFusiParameters(parameters):
    fusiParameters = []
    for parameter in parameters:
        if isFusi(parameter):
            fusiParameters.append(parameter)
    return fusiParameters


print("\n\nAll parameter names for lib:fusi=1 :\n")
for parameters in basicFunctions.values():
    fusiParameters = filterFusiParameters(parameters)
    for parameter in fusiParameters:
        print(parameter["Parameter_name"])


# 7. Using the obtained dictionary, for the parameters of type tUInt16, replace the „dd:MaxRange“ value which is
# different than the maximum value allowed by the data type (65 535)


def isUInt16(parameter):
    return (parameter["type"] == "tUInt16")


def filterUInt16Parameters(parameters):
    UInt16Parameters = []
    for parameter in parameters:
        if isUInt16(parameter):
            UInt16Parameters.append(parameter)
    return UInt16Parameters


print("\n\nAll tUInt16 parameters with different dd:MaxRange:\n")
for parameters in basicFunctions.values():
    UInt16Parameters = filterUInt16Parameters(parameters)
    for parameter in UInt16Parameters:
        if parameter["dd:MaxRange"] != "65535":
            print(parameter)
            parameter["dd:MaxRange"] = "65535"


# 8. Write the dictionary in a Output.txt file

output = open('Result.txt', 'w')
for parameters in basicFunctions.values():
    for parameter in parameters:
        output.write("<")
        for key in parameter.keys():
            output.write(key + '="' + parameter[key] + '" ')
        output.write("/>\n")


output.close()