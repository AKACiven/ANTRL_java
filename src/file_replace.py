def file_replace(file_name, rep_word, new_word):
    f_read = open(file_name)
    content = []
    count = 0

    for each_line in f_read:
        if rep_word in each_line:
            count += each_line.count(rep_word)
            each_line = each_line.replace(rep_word, new_word)
        content.append(each_line)
        f_write = open(file_name, 'w')
        f_write.writelines(content)
        f_write.close()
    f_read.close()

if __name__ == '__main__':
    file_replace("../logs/basic/basic_var.jan", "\'", "\"")