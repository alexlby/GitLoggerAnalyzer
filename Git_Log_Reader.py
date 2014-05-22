# -*- coding: utf-8 -*-
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

########################################################################


def convert_git_log_file_2_git_commits(file_name):
    import codecs
    import re

    git_commits = []

    pattern_st = re.compile(r'[Ss][Tt]\d{3,5}')
    pattern_ta = re.compile(r'[Tt][Aa]\d{3,5}')
    pattern_de = re.compile(r'[Dd][Ee]\d{3,5}')

    with codecs.open(file_name, 'rt',  'utf-8') as file:
        all_lines = file.readlines()
        for line in all_lines:
            if "commit" in line and line.find('commit') <= 1: # filter the case of 'commit' in raw commit message
                current_commit_line = line

                commit_hash_line = current_commit_line.split(' ')        # e.g.: commit e53556fb6b28b9a4714886124cb4781cf0e5dae8
                commit_hash = commit_hash_line[1].strip()                # so get item 1, its the hash id of this commit

                author_id_line = all_lines[all_lines.index(line)+1]      # go to next line
                author_id = author_id_line.split(' ')[1].strip()

                commit_date_line = all_lines[all_lines.index(line)+2]
                commit_date = commit_date_line[5:].strip()      # e.g. : Date:   Wed Dec 25 10:05:12 2013 +0800 , so need get substring [5:]

                commit_message_line = all_lines[all_lines.index(line)+4]
                commit_message = commit_message_line.strip()

                st_ids_in_this_commit = []
                ta_ids_in_this_commit = []
                de_ids_in_this_commit = []

                # Start handling ST/DE/TA reg_expression matching
                for st in pattern_st.finditer(commit_message):
                    st_ids_in_this_commit.append(st.group())
                for ta in pattern_ta.finditer(commit_message):
                    ta_ids_in_this_commit.append(ta.group())
                for de in pattern_de.finditer(commit_message):
                    de_ids_in_this_commit.append(de.group())

                print "commit message = ",  commit_message
                if len(st_ids_in_this_commit) == 0 and len(de_ids_in_this_commit) == 0 and len(ta_ids_in_this_commit) == 0:
                    continue    # if no rally id, do nothing

                # Start handle changed files
                current_changed_files = []
                start_index_of_change_files_in_this_commit_block = all_lines.index(line) + 6
                count_of_change_files_in_this_commit_block = 0
                line_pr = all_lines[start_index_of_change_files_in_this_commit_block]
                while not ("commit" in line_pr and line_pr.find('commit') == 0):
                    line_pr_index = start_index_of_change_files_in_this_commit_block + count_of_change_files_in_this_commit_block
                    if (line_pr_index < len(all_lines)):
                        line_pr = all_lines[line_pr_index]
                    else:
                        break
                    count_of_change_files_in_this_commit_block += 1

                for currentPr in range(start_index_of_change_files_in_this_commit_block, line_pr_index - 1):
                    current_changed_file = all_lines[currentPr].strip()
                    current_changed_files.append(current_changed_file)

                git_commit = GitCommit(commit_hash, author_id, commit_date, commit_message, st_ids_in_this_commit, ta_ids_in_this_commit, de_ids_in_this_commit, current_changed_files)
                git_commit.show_self()
                git_commits.append(git_commit)
            file.close()
    return git_commits

######################################################################


def insert_git_commits_2_mysql(system_name, branch_name, git_commits):
    import MySQLdb
    try:
        #conn=MySQLdb.connect(host='localhost',user='root', passwd='adminpass',db='localtestdb',port=3306)
        conn = MySQLdb.connect(host='localhost', user='root', passwd='adminpass', db='pythondb', port=3306)   # in office PC, it's 'pythondb'
        cur = conn.cursor()

        cur.execute('select seq.SEQ_NUMBER_VALUE from SEQ_NUMBER seq where seq.SEQ_NUMBER_TYPE = \'GIT_COMMIT\'')
        select_commit_seq = cur.fetchone()[0]
        cur.execute('select seq.SEQ_NUMBER_VALUE from SEQ_NUMBER seq where seq.SEQ_NUMBER_TYPE = \'RALLY_UNIT\'')
        select_rally_unit_seq = cur.fetchone()[0]
        cur.execute('select seq.SEQ_NUMBER_VALUE from SEQ_NUMBER seq where seq.SEQ_NUMBER_TYPE = \'SRC_FILE\'')
        select_file_seq = cur.fetchone()[0]

        for commit in git_commits:
            #commit.show_self()

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

##        select_count = cur.execute('select * from git_commit')
##        select_rows = cur.fetchall()
##        print(select_count)
##        for row in select_rows:
##            print (row)
    finally:
        conn.commit()
        cur.close()
        conn.close()

########################################################################


def main():
    print ("reader start!")
    file_name = "Resources/develop_rel_1_7_0.txt"
    git_commits = convert_git_log_file_2_git_commits(file_name)
    insert_git_commits_2_mysql('SPS', 'develop_rel_1.7.0', git_commits)
    print ("reader end!")

if __name__=='__main__':
    main()

