__author__ = 'luobiyuan'


def generate_report():
    import MySQLdb

    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='adminpass', db='pythondb', port=3306)
        cur = conn.cursor()

        # for Excel
        cur.execute('select src.SRC_FILE_NAME, rally.RALLY_UNIT_NUMBER from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' and (src.SRC_FILE_NAME like \'%%SS_WebServer%%\' or src.SRC_FILE_NAME like \'%%SPPM_WebServer%%\') order by src.SRC_FILE_NAME desc')
        select_file_defect_in_prs_row = cur.fetchall()

        cur.execute('select src.SRC_FILE_NAME, rally.RALLY_UNIT_NUMBER from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' and (src.SRC_FILE_NAME like \'%%SS_AEServer%%\' or src.SRC_FILE_NAME like \'%%SPPM_AEServer%%\') order by src.SRC_FILE_NAME desc')
        select_file_defect_in_dom_row = cur.fetchall()

        cur.execute('select src.SRC_FILE_NAME, rally.RALLY_UNIT_NUMBER from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' and (src.SRC_FILE_NAME like \'%%SS_WebServer%%\' or src.SRC_FILE_NAME like \'%%SPPM_WebServer%%\') order by src.SRC_FILE_NAME desc')
        select_file_story_in_prs_row = cur.fetchall()

        cur.execute('select src.SRC_FILE_NAME, rally.RALLY_UNIT_NUMBER from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' and (src.SRC_FILE_NAME like \'%%SS_AEServer%%\' or src.SRC_FILE_NAME like \'%%SPPM_AEServer%%\') order by src.SRC_FILE_NAME desc')
        select_file_story_in_dom_row = cur.fetchall()



        # for Pie Chart
        cur.execute('select count(distinct(rally.RALLY_UNIT_NUMBER)) from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' and (src.SRC_FILE_NAME like \'%%SS_AEServer%%\')');
        select_count_dom_sps_defects = cur.fetchone()[0]
        cur.execute('select count(distinct(rally.RALLY_UNIT_NUMBER)) from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' and (src.SRC_FILE_NAME like \'%%SPPM_AEServer%%\')');
        select_count_dom_sppm_defects = cur.fetchone()[0]

        cur.execute('select count(distinct(rally.RALLY_UNIT_NUMBER)) from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' and (src.SRC_FILE_NAME like \'%%SS_WebServer%%\')');
        select_count_prs_sps_defects = cur.fetchone()[0]
        cur.execute('select count(distinct(rally.RALLY_UNIT_NUMBER)) from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'D\' and (src.SRC_FILE_NAME like \'%%SPPM_WebServer%%\')');
        select_count_prs_sppm_defects = cur.fetchone()[0]

        pie_defects = []
        pie_defects.append(["WLS_DOM_SPS", select_count_dom_sps_defects])
        pie_defects.append(["WLS_DOM_SPPM", select_count_dom_sppm_defects])
        pie_defects.append(["WLS_PRS_SPS", select_count_prs_sps_defects])
        pie_defects.append(["WLS_PRS_SPPM", select_count_prs_sppm_defects])


        cur.execute('select count(distinct(rally.RALLY_UNIT_ID)) from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' and (src.SRC_FILE_NAME like \'%%SS_AEServer%%\')');
        select_count_dom_sps_stories = cur.fetchone()[0]
        cur.execute('select count(distinct(rally.RALLY_UNIT_ID)) from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' and (src.SRC_FILE_NAME like \'%%SPPM_AEServer%%\')');
        select_count_dom_sppm_stories = cur.fetchone()[0]

        cur.execute('select count(distinct(rally.RALLY_UNIT_ID)) from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' and (src.SRC_FILE_NAME like \'%%SS_WebServer%%\')');
        select_count_prs_sps_stories = cur.fetchone()[0]
        cur.execute('select count(distinct(rally.RALLY_UNIT_ID)) from rally_unit rally, src_file src where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID and rally.RALLY_UNIT_TYPE = \'S\' and (src.SRC_FILE_NAME like \'%%SPPM_WebServer%%\')');
        select_count_prs_sppm_stories = cur.fetchone()[0]

        pie_stories = []
        pie_stories.append(["WLS_DOM_SPS", select_count_dom_sps_stories])
        pie_stories.append(["WLS_DOM_SPPM", select_count_dom_sppm_stories])
        pie_stories.append(["WLS_PRS_SPS", select_count_prs_sps_stories])
        pie_stories.append(["WLS_PRS_SPPM", select_count_prs_sppm_stories])

        generate_pie_chart(pie_defects, pie_stories)

        output_2_xls(select_file_defect_in_prs_row, select_file_story_in_prs_row, select_file_defect_in_dom_row, select_file_story_in_dom_row)

    finally:
        conn.commit()
        cur.close()
        conn.close()


def output_2_xls(file_defect_in_prs_rows, file_story_in_prs_rows, file_defect_in_dom_rows, file_story_in_dom_rows):
    import xlwt

    output_workbook = xlwt.Workbook()

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Calibri'
    style.font = font


    sheet_file_defect_in_prs = output_workbook.add_sheet('File - Defect - in PRS')
    sheet_file_defect_in_prs.write(0, 0, "File Name", style)
    sheet_file_defect_in_prs.write(0, 1, "Defect ID", style)
    file_defect_in_prs_row_index = 1
    for row in file_defect_in_prs_rows:
        if (len(row[0]) == 0):
            continue
        sheet_file_defect_in_prs.write(file_defect_in_prs_row_index, 0, row[0], style)
        sheet_file_defect_in_prs.write(file_defect_in_prs_row_index, 1, row[1], style)
        file_defect_in_prs_row_index += 1
    sheet_file_defect_in_prs.col(0).set_width(30000)
    sheet_file_defect_in_prs.col(1).set_width(4000)

    sheet_file_story_in_prs = output_workbook.add_sheet('File - Story - in PRS')
    sheet_file_story_in_prs.write(0, 0, "File Name", style)
    sheet_file_story_in_prs.write(0, 1, "Story ID", style)
    file_story_in_prs_row_index = 1
    for row in file_story_in_prs_rows:
        if (len(row[0]) == 0):
            continue
        sheet_file_story_in_prs.write(file_story_in_prs_row_index, 0, row[0], style)
        sheet_file_story_in_prs.write(file_story_in_prs_row_index, 1, row[1], style)
        file_story_in_prs_row_index += 1
    sheet_file_story_in_prs.col(0).set_width(30000)
    sheet_file_story_in_prs.col(1).set_width(4000)

    sheet_file_defect_in_dom = output_workbook.add_sheet('File - Defect - in DOM')
    sheet_file_defect_in_dom.write(0, 0, "File Name", style)
    sheet_file_defect_in_dom.write(0, 1, "Defect ID", style)
    file_defect_in_dom_row_index = 1
    for row in file_defect_in_dom_rows:
        if (len(row[0]) == 0):
            continue
        sheet_file_defect_in_dom.write(file_defect_in_dom_row_index, 0, row[0], style)
        sheet_file_defect_in_dom.write(file_defect_in_dom_row_index, 1, row[1], style)
        file_defect_in_dom_row_index += 1
    sheet_file_defect_in_dom.col(0).set_width(30000)
    sheet_file_defect_in_dom.col(1).set_width(4000)

    sheet_file_story_in_dom = output_workbook.add_sheet('File - Story - in DOM')
    sheet_file_story_in_dom.write(0, 0, "File Name", style)
    sheet_file_story_in_dom.write(0, 1, "Story ID", style)
    file_story_in_dom_row_index = 1
    for row in file_story_in_dom_rows:
        if (len(row[0]) == 0):
            continue
        sheet_file_story_in_dom.write(file_story_in_dom_row_index, 0, row[0], style)
        sheet_file_story_in_dom.write(file_story_in_dom_row_index, 1, row[1], style)
        file_story_in_dom_row_index += 1
    sheet_file_story_in_dom.col(0).set_width(30000)
    sheet_file_story_in_dom.col(1).set_width(4000)

    output_workbook.save('dist/WLS_Rally.xls')


def generate_pie_chart(pie_defects, pie_stories):
    from Generate_Chart import Generate_Chart

    charGen = Generate_Chart()
    charGen.pieChart(pie_defects, "dist/pie_defects.png", "Defects in Different WLS Chart", "blue")
    charGen.pieChart(pie_stories, "dist/pie_stories.png", "Stories in Different WLS Chart", "green")

def main():
    print ("Reporter start!")
    generate_report()
    print ("Reporter end!")

if __name__ == '__main__':
    main()