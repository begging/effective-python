'''
A function returning a list
Problems
 1. 'append' method deemphasizes the value being added to the list (index+1).
 2. it requires all results to be stored in the list before being returned.
'''
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result


'''
A function returning a generator
'''
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index+1

result = list(index_words_iter('some text'))
print(result)
