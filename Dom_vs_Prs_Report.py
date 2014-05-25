__author__ = 'luobiyuan'

def generate_report():
    import MySQLdb

    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='adminpass', db='pythondb', port=3306)
        cur = conn.cursor()

        cur.execute('select src.SRC_FILE_NAME, rally.RALLY_UNIT_NUMBER from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' and (src.SRC_FILE_NAME like \'%%SS_WebServer%%\' or src.SRC_FILE_NAME like \'%%.js%%\') order by src.SRC_FILE_NAME desc')
        select_file_defect_in_prs_row = cur.fetchall()

        cur.execute('select src.SRC_FILE_NAME, rally.RALLY_UNIT_NUMBER from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' and (src.SRC_FILE_NAME like \'%%SS_WebServer%%\' or src.SRC_FILE_NAME like \'%%.js%%\') order by src.SRC_FILE_NAME desc')
        select_file_story_in_prs_row = cur.fetchall()


        count = 0
        for row in select_file_defect_in_prs_row:
            print row[0], "\t --> \t", row[1]
            count += 1
        print "total record = ", count

        # output_2_xls(select_file_defect_row, select_file_story_row, select_file_defect_count_rows, select_file_story_count_rows)

    finally:
        conn.commit()
        cur.close()
        conn.close()

def main():
    print ("Reporter start!")
    generate_report()
    print ("Reporter end!")

if __name__ == '__main__':
    main()