with open('source_file','rb') as source_file:
    with open('target_file.txt','w+b') as dest_file:
    contents = source_file.read()
    dest_file.write(contents.decode('utf-16').encode('utf-8'))
