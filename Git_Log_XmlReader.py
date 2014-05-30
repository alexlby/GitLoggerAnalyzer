__author__ = 'LUOAL2'
# -*- coding: utf-8 -*-

# for below git log format:
# git log --pretty=format:"<entry><commit_hash>%H</commit_hash><author>%an</author><commit_date>%ci</commit_date><message_body>%s</message_body></entry>" --after={2014-04-19} --before={2014-05-18} --no-merges --name-only develop_rel_1.7.0 >> develop_rel_1_7_0_xml.txt

class GitCommit:
    def __init__(self, git_commit_hash, author_id, commit_date, commit_message, rally_sts, rally_tas, rally_des, changed_files):
        self.commit_hash = git_commit_hash
        self.author_id = author_id
        self.commit_date = commit_date
        self.commit_message = commit_message
        self.rally_sts = rally_sts
        self.rally_tas = rally_tas
        self.rally_des = rally_des
        self.changed_files = changed_files

    def show_self(self):
            print '============================================'
            print 'commit hash = ', self.commit_hash
            print 'commit author = ', self.author_id
            print 'commit date = ', self.commit_date
            print 'commit message = ', self.commit_message
            print 'rally units as below: '
            for rally_st in self.rally_sts:
                print '-->', rally_st
            for rally_ta in self.rally_tas:
                print '-->', rally_ta
            for rally_de in self.rally_des:
                print '-->', rally_de
            print 'below files were changed in this commit: '
            for changed_files in self.changed_files:
                print '---->', changed_files
            print '============================================'

def convert_git_log_file_2_git_commits(file_name):
    import codecs
    import re
    import xml.dom.minidom

    git_commits = []

    pattern_st = re.compile(r'[Ss][Tt]\d{3,6}')
    pattern_ta = re.compile(r'[Tt][Aa]\d{3,6}')
    pattern_de = re.compile(r'[Dd][Ee]\d{3,6}')

    with codecs.open(file_name, 'rt',  'utf-8') as file:
        all_lines = file.readlines()
        line_index = 0
        while (line_index < len(all_lines)):
            if (len(all_lines[line_index].strip()) > 1):
                if ("<entry><commit_hash>" in all_lines[line_index]):

                    file_names = []

                    # prepare the raw line
                    data = all_lines[line_index].strip()
                    data = data.replace(u'\u3010', '[').replace(u'\u3011', ']') #.replace("【", "[").replace("】", "]")
                    data = data.replace("&", "&amp;").replace("\"", "&quot;")
                    print "current line = ", data
                    xml_dom = xml.dom.minidom.parseString(data)

                    commit_hash_nodes = xml_dom.getElementsByTagName("commit_hash")
                    commit_hash = commit_hash_nodes[0].childNodes[0].nodeValue

                    author_nodes = xml_dom.getElementsByTagName("author")
                    author = author_nodes[0].childNodes[0].nodeValue

                    commit_date_nodes = xml_dom.getElementsByTagName("commit_date")
                    commit_date = commit_date_nodes[0].childNodes[0].nodeValue

                    message_body_nodes = xml_dom.getElementsByTagName("message_body")
                    message_body = message_body_nodes[0].childNodes[0].nodeValue

                    st_ids_in_this_commit = []
                    ta_ids_in_this_commit = []
                    de_ids_in_this_commit = []

                    # Start handling ST/DE/TA reg_expression matching
                    for st in pattern_st.finditer(message_body):
                        st_ids_in_this_commit.append(st.group())
                    for ta in pattern_ta.finditer(message_body):
                        ta_ids_in_this_commit.append(ta.group())
                    for de in pattern_de.finditer(message_body):
                        de_ids_in_this_commit.append(de.group())

                    if len(st_ids_in_this_commit) == 0 and len(de_ids_in_this_commit) == 0 and len(ta_ids_in_this_commit) == 0:
                        line_index += 1
                        continue    # if no rally id, do nothing

                    line_index += 1
                    while (line_index < len(all_lines) and len(all_lines[line_index]) > 1):
                        file_names.append(all_lines[line_index].strip())
                        line_index += 1


                    git_commit = GitCommit(commit_hash, author, commit_date, message_body, st_ids_in_this_commit, ta_ids_in_this_commit, de_ids_in_this_commit, file_names)
                    git_commit.show_self()
                    git_commits.append(git_commit)
                line_index += 1
            else:
                line_index += 1
    file.close()
    return git_commits

def insert_git_commits_2_mysql(system_name, branch_name, git_commits):
    import MySQLdb
    try:

        conn = MySQLdb.connect(host='localhost', user='root', passwd='adminpass', db='pythondb', port=3306)   # in office PC, it's 'pythondb'
        cur = conn.cursor()

        cur.execute('select seq.SEQ_NUMBER_VALUE from SEQ_NUMBER seq where seq.SEQ_NUMBER_TYPE = \'GIT_COMMIT\'')
        select_commit_seq = cur.fetchone()[0]
        cur.execute('select seq.SEQ_NUMBER_VALUE from SEQ_NUMBER seq where seq.SEQ_NUMBER_TYPE = \'RALLY_UNIT\'')
        select_rally_unit_seq = cur.fetchone()[0]
        cur.execute('select seq.SEQ_NUMBER_VALUE from SEQ_NUMBER seq where seq.SEQ_NUMBER_TYPE = \'SRC_FILE\'')
        select_file_seq = cur.fetchone()[0]

        for commit in git_commits:

            select_commit_seq += 1

            commit_row = [system_name, branch_name, select_commit_seq, commit.commit_hash, commit.commit_date, commit.author_id, commit.commit_message]
            cur.execute('insert into GIT_COMMIT values(%s,%s,%s,%s,%s,%s,%s)', commit_row)

            for rally_st in commit.rally_sts:
                select_rally_unit_seq += 1
                rally_st_row = ['S', select_commit_seq, select_rally_unit_seq, rally_st]
                cur.execute('insert into RALLY_UNIT values(%s,%s,%s,%s)', rally_st_row)
            for rally_ta in commit.rally_tas:
                select_rally_unit_seq += 1
                rally_ta_row = ['T', select_commit_seq, select_rally_unit_seq, rally_ta]
                print select_commit_seq
                print select_rally_unit_seq
                print rally_ta
                cur.execute('insert into RALLY_UNIT values(%s,%s,%s,%s)', rally_ta_row)
            for rally_de in commit.rally_des:
                select_rally_unit_seq += 1
                rally_de_row = ['D', select_commit_seq, select_rally_unit_seq, rally_de]
                cur.execute('insert into RALLY_UNIT values(%s,%s,%s,%s)', rally_de_row)
            cur.execute('update SEQ_NUMBER seq set seq.SEQ_NUMBER_VALUE = %s where seq.SEQ_NUMBER_TYPE = \'RALLY_UNIT\'',  select_rally_unit_seq)

            for changed_file in commit.changed_files:
                select_file_seq += 1
                file_row = [select_file_seq, changed_file, select_commit_seq]
                cur.execute('insert into SRC_FILE values(%s,%s,%s)', file_row)
            cur.execute('update SEQ_NUMBER seq set seq.SEQ_NUMBER_VALUE = %s where seq.SEQ_NUMBER_TYPE = \'SRC_FILE\'',  select_file_seq)

        cur.execute('update SEQ_NUMBER seq set seq.SEQ_NUMBER_VALUE = %s where seq.SEQ_NUMBER_TYPE = \'GIT_COMMIT\'',  select_commit_seq)

    finally:
        conn.commit()
        cur.close()
        conn.close()

def main(argv):
    print ("reader start!")
    # file_name = "Resources/develop_rel_1_7_0_xml.txt"
    file_name = argv[-1]
    git_commits = convert_git_log_file_2_git_commits("./Resources/develop_rel_1_7_0_xml.txt")
    insert_git_commits_2_mysql('SPS', 'develop_rel_1.7.0', git_commits)
    print ("reader end!")

if __name__=='__main__':
    import sys
    main(sys.argv)