from attacut import tokenize, Tokenizer

words = tokenize("มือ")
# word_list = []
# for i in (words):
#     word_list.append(i)
# print(word_list)
if len(words) == 1:
    word_list = f'(\'{words[0]}\')'
test = tuple(word_list)
pose_dict = {}
frame_dict = {}


find_word = f'SELECT w.Word, f.*  FROM [dbo].[FullPose] f JOIN [dbo].[Word] w ON f.Word_ID = w.Word_ID WHERE w.Word IN {word_list} order by w.Word asc , f.Frame asc'
word_list = tuple(words)
for name in word_list:
    pose_dict[name] = []
    frame_dict[name] = [] 
print(find_word)
print(pose_dict)
# print(test[0]) 
# print(tuple(word_list))

# print(words[0])
# print(tuple(words)) 
# word_list = f'(\'{words[0]}\')'
# print(len(words))
# print(word_list)
# placeholder= '?' 
# placeholders = ', '.join(placeholder for unused in words)
# print(placeholders)
# print(str(words))