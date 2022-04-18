msg = '/exit/*';
# msg = msg.encode()
# len_msg = b"%03d" % (len(msg),)
# msg = len_msg + msg
# print(msg)
# if(msg == b'exit'): 
#             flag = False
#             print('flag menjadi: ', flag)

# print("Enter the String: ")
# text = "F:\Doc\ITS\SMT 5\z_IPYNB_Program\ProgJar"

# word = text.split("\\")[-1]

# print(word)

# f = open("etc/passwd", "rb")
# b = f.read()
# print(len(b))
# f.close()

b = open("etc/passwd", "rb").read()
f = open("passwd3", "wb+")
f.write(b)
f.close()

f = open("etc/passwd", "rb")
b = f.read()
print(len(b))
print(b)
f.close()

# b = open("etc/passwd", "rb").read()
# print(len(b))
# c = bytes(b, "ascii")
# print(c)