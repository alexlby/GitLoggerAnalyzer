__author__ = 'LUOAL2'


def find_git_commit_from_mysql():
    import MySQLdb

    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='adminpass', db='pythondb', port=3306)
        cur = conn.cursor()

        cur.execute('select src.SRC_FILE_NAME, count(distinct(rally.RALLY_UNIT_ID)) as rally_count from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' group by src.SRC_FILE_NAME order by rally_count desc')
        select_defect_rows = cur.fetchall()

        cur.execute('select src.SRC_FILE_NAME, count(distinct(rally.RALLY_UNIT_ID)) as rally_count from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' group by src.SRC_FILE_NAME order by rally_count desc')
        select_story_rows = cur.fetchall()

        for row in select_defect_rows:
            print 'Defect -->', row[0], '   ', row[1]
        for row in select_story_rows:
            print 'Story -->', row[0], '    ', row[1]
    finally:
        conn.commit()
        cur.close()
        conn.close()


def main():
    print ("Reporter start!")
    find_git_commit_from_mysql()
    print ("Reporter end!")

if __name__ == '__main__':
    main()