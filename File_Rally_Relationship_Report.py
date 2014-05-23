__author__ = 'LUOAL2'


def find_git_commit_from_mysql():
    import MySQLdb

    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='adminpass', db='pythondb', port=3306)
        cur = conn.cursor()

        cur.execute('select src.SRC_FILE_NAME, rally.RALLY_UNIT_NUMBER from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' order by src.SRC_FILE_NAME desc')
        select_file_defect_row = cur.fetchall()

        cur.execute('select src.SRC_FILE_NAME, rally.RALLY_UNIT_NUMBER from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' order by src.SRC_FILE_NAME desc')
        select_file_story_row = cur.fetchall()

        cur.execute('select src.SRC_FILE_NAME, count(distinct(rally.RALLY_UNIT_ID)) as rally_count from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' group by src.SRC_FILE_NAME order by rally_count desc')
        select_file_defect_count_rows = cur.fetchall()

        cur.execute('select src.SRC_FILE_NAME, count(distinct(rally.RALLY_UNIT_ID)) as rally_count from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' group by src.SRC_FILE_NAME order by rally_count desc')
        select_file_story_count_rows = cur.fetchall()

        for row in select_file_defect_count_rows:
            print 'Defect --> \t', row[0], '\t', row[1]
        for row in select_file_story_count_rows:
            print 'Story --> \t', row[0], '\t', row[1]

        output_2_xls(select_file_defect_row, select_file_story_row, select_file_defect_count_rows, select_file_story_count_rows)

    finally:
        conn.commit()
        cur.close()
        conn.close()

def output_2_xls(file_defect_rows, file_story_rows, file_defect_count_rows, file_story_count_rows):
    import xlwt

    output_workbook = xlwt.Workbook()

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Calibri'
    style.font = font


    sheet_file_defect = output_workbook.add_sheet('file - defect')
    sheet_file_defect.write(0, 0, "File Name", style)
    sheet_file_defect.write(0, 1, "Defect ID", style)
    file_defect_row_index = 1
    for row in file_defect_rows:
        if (len(row[0]) == 0):
            continue
        sheet_file_defect.write(file_defect_row_index, 0, row[0], style)
        sheet_file_defect.write(file_defect_row_index, 1, row[1], style)
        file_defect_row_index += 1
    sheet_file_defect.col(0).set_width(30000)
    sheet_file_defect.col(1).set_width(4000)

    sheet_file_story = output_workbook.add_sheet('file - story')
    sheet_file_story.write(0, 0, "File Name", style)
    sheet_file_story.write(0, 1, "Story ID", style)
    file_story_row_index = 1
    for row in file_story_rows:
        if (len(row[0]) == 0):
            continue
        sheet_file_story.write(file_story_row_index, 0, row[0], style)
        sheet_file_story.write(file_story_row_index, 1, row[1], style)
        file_story_row_index += 1
    sheet_file_story.col(0).set_width(30000)
    sheet_file_story.col(1).set_width(4000)

    sheet_file_defect_count = output_workbook.add_sheet('file - defect count')
    sheet_file_defect_count.write(0, 0, "File Name", style)
    sheet_file_defect_count.write(0, 1, "Defect Count", style)
    file_defect_count_row_index = 1
    for row in file_defect_count_rows:
        if (len(row[0]) == 0):
            continue
        sheet_file_defect_count.write(file_defect_count_row_index, 0, row[0], style)
        sheet_file_defect_count.write(file_defect_count_row_index, 1, row[1], style)
        file_defect_count_row_index += 1
    sheet_file_defect_count.col(0).set_width(30000)
    sheet_file_defect_count.col(1).set_width(4000)

    sheet_file_story_count = output_workbook.add_sheet('file - story count')
    sheet_file_story_count.write(0, 0, "File Name", style)
    sheet_file_story_count.write(0, 1, "Story Count", style)
    file_story_count_row_index = 1
    for row in file_story_count_rows:
        if (len(row[0]) == 0):
            continue
        sheet_file_story_count.write(file_story_count_row_index, 0, row[0], style)
        sheet_file_story_count.write(file_story_count_row_index, 1, row[1], style)
        file_story_count_row_index += 1
    sheet_file_story_count.col(0).set_width(30000)
    sheet_file_story_count.col(1).set_width(4000)

    output_workbook.save('dist/File_Rally.xls')

def main():
    print ("Reporter start!")
    find_git_commit_from_mysql()
    print ("Reporter end!")

if __name__ == '__main__':
    main()