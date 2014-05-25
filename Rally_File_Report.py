__author__ = 'luobiyuan'

def generate_report():
   import MySQLdb

   try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='adminpass', db='pythondb', port=3306)
        cur = conn.cursor()

        cur.execute('select rally.RALLY_UNIT_NUMBER, src.SRC_FILE_NAME from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' order by rally.RALLY_UNIT_NUMBER desc')
        select_defect_rows = cur.fetchall()

        cur.execute('select rally.RALLY_UNIT_NUMBER, src.SRC_FILE_NAME from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' order by rally.RALLY_UNIT_NUMBER desc')
        select_story_rows = cur.fetchall()

        defect_count = 0
        for row in select_defect_rows:
            print 'Defect --> \t', row[0], '\t', row[1]
            defect_count += 1

        story_count = 0
        for row in select_story_rows:
            print 'Story --> \t', row[0], '\t', row[1]
            story_count += 1

        print 'Total Defect Count = ', defect_count
        print 'Total Story Count = ', story_count



        cur.execute('select rally.RALLY_UNIT_NUMBER, count(distinct(src.SRC_FILE_ID)) as count_src from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' group by rally.RALLY_UNIT_NUMBER order by count_src desc')
        select_defect_file_count_rows = cur.fetchall()
        for row in select_defect_file_count_rows:
            print 'Defect --> \t', row[0], '\t', row[1]

        cur.execute('select rally.RALLY_UNIT_NUMBER, count(distinct(src.SRC_FILE_ID)) as count_src from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' group by rally.RALLY_UNIT_NUMBER order by count_src desc')
        select_story_file_count_rows = cur.fetchall()
        for row in select_story_file_count_rows:
            print 'Story --> \t', row[0], '\t', row[1]

        output_2_xls(select_defect_rows, select_story_rows, select_defect_file_count_rows, select_story_file_count_rows)
   finally:
        conn.commit()
        cur.close()
        conn.close()

def output_2_xls(defect_rows, story_rows, defect_file_count_rows, story_file_count_rows):
    import xlwt

    output_workbook = xlwt.Workbook()

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Calibri'
    style.font = font

    sheet_defect = output_workbook.add_sheet('defect - source file')
    sheet_defect.write(0, 0, "Defect ID", style)
    sheet_defect.write(0, 1, "Source File Name", style)
    defect_row_index = 1
    for row in defect_rows:
        if (len(row[0]) == 0):
            continue
        sheet_defect.write(defect_row_index, 0, row[0], style)
        sheet_defect.write(defect_row_index, 1, row[1], style)
        defect_row_index += 1
    sheet_defect.col(0).set_width(4000)
    sheet_defect.col(1).set_width(30000)


    sheet_defect_file_count = output_workbook.add_sheet('defect - file count')
    sheet_defect_file_count.write(0, 0, "Defect ID", style)
    sheet_defect_file_count.write(0, 1, "Source File Count", style)
    defect_file_count_row_index = 1
    for row in defect_file_count_rows:
        if (len(row[0]) == 0):
            continue
        sheet_defect_file_count.write(defect_file_count_row_index, 0, row[0], style)
        sheet_defect_file_count.write(defect_file_count_row_index, 1, row[1], style)
        defect_file_count_row_index += 1
    sheet_defect_file_count.col(0).set_width(4000)
    sheet_defect_file_count.col(1).set_width(4000)

    sheet_story = output_workbook.add_sheet('story - source file')
    sheet_story.write(0, 0, "Story ID", style)
    sheet_story.write(0, 1, "Source File Name", style)
    story_row_index = 1
    for row in story_rows:
        if (len(row[0]) == 0):
            continue
        sheet_story.write(story_row_index, 0, row[0], style)
        sheet_story.write(story_row_index, 1, row[1], style)
        story_row_index += 1
    sheet_story.col(0).set_width(4000)
    sheet_story.col(1).set_width(30000)


    sheet_story_file_count = output_workbook.add_sheet('story - file count')
    sheet_story_file_count.write(0, 0, "Story ID", style)
    sheet_story_file_count.write(0, 1, "Source File Count", style)
    story_file_count_row_index = 1
    for row in story_file_count_rows:
        if (len(row[0]) == 0):
            continue
        sheet_story_file_count.write(story_file_count_row_index, 0, row[0], style)
        sheet_story_file_count.write(story_file_count_row_index, 1, row[1], style)
        story_file_count_row_index += 1
    sheet_story_file_count.col(0).set_width(4000)
    sheet_story_file_count.col(1).set_width(4000)

    output_workbook.save('dist/Rally_File.xls')


def main():
    print ("Reporter start!")
    generate_report()
    print ("Reporter end!")

if __name__ == '__main__':
    main()