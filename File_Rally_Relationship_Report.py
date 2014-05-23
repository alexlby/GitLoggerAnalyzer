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
            print 'Defect --> \t', row[0], '\t', row[1]
        for row in select_story_rows:
            print 'Story --> \t', row[0], '\t', row[1]

        output_2_xls(select_defect_rows, select_story_rows)

    finally:
        conn.commit()
        cur.close()
        conn.close()

def output_2_xls(defect_rows, story_rows):
    import xlwt

    output_workbook = xlwt.Workbook()

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Calibri'
    style.font = font

    sheet_defect = output_workbook.add_sheet('defect')
    sheet_defect.write(0, 0, "File Name", style)
    sheet_defect.write(0, 1, "Git Commit Count", style)
    defect_row_index = 1
    for row in defect_rows:
        if (len(row[0]) == 0):
            continue
        sheet_defect.write(defect_row_index, 0, row[0], style)
        sheet_defect.write(defect_row_index, 1, row[1], style)
        defect_row_index += 1
    sheet_defect.col(0).set_width(30000)
    sheet_defect.col(1).set_width(4000)

    sheet_story = output_workbook.add_sheet('story')
    sheet_story.write(0, 0, "File Name", style)
    sheet_story.write(0, 1, "Git Commit Count", style)
    story_row_index = 1
    for row in story_rows:
        if (len(row[0]) == 0):
            continue
        sheet_story.write(story_row_index, 0, row[0], style)
        sheet_story.write(story_row_index, 1, row[1], style)
        story_row_index += 1
    sheet_story.col(0).set_width(30000)
    sheet_story.col(1).set_width(4000)

    output_workbook.save('dist/sha.xls')

def main():
    print ("Reporter start!")
    find_git_commit_from_mysql()
    print ("Reporter end!")

if __name__ == '__main__':
    main()