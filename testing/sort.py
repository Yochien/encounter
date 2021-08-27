#user input
input = ["3", "1", "7", "1"]

#duplicate removal
def removeDuplicates(selector):
    selected = []
    for s in selector:
        if s not in selected:
            selected.append(s)
    return selected

def reverseSort(selected):
    sortedList = []
    for s in selected:
        item = int(s)
        sortedList.append(item)
    sortedList.sort(reverse = True)
    return sortedList

print(input)
print(removeDuplicates(input))
print(sorted(removeDuplicates(input)))
print(reverseSort(removeDuplicates(input)))