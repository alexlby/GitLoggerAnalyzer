__author__ = 'luobiyuan'

import Reports_Common_Dao


def output_2_xls(project_name, branch_name):
    import xlwt

    output_workbook = xlwt.Workbook()

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Calibri'
    style.font = font

    defect_rows = Reports_Common_Dao.searhc_rally_file_mapping(project_name, branch_name, 'D')
    sheet_defect = output_workbook.add_sheet('defect - source file' + '(' + str(len(defect_rows)) + ')')
    if len(defect_rows) > 0:
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

    defect_file_count_rows = Reports_Common_Dao.search_count_of_file_by_rally_number(project_name, branch_name, 'D')
    sheet_defect_file_count = output_workbook.add_sheet('defect - file count' + '(' + str(len(defect_file_count_rows)) + ')')
    if len(defect_file_count_rows) > 0:
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

    story_rows = Reports_Common_Dao.searhc_rally_file_mapping(project_name, branch_name, 'S')
    sheet_story = output_workbook.add_sheet('story - source file' + '(' + str(len(story_rows)) + ')')
    if len(story_rows) > 0:
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

    story_file_count_rows = Reports_Common_Dao.search_count_of_file_by_rally_number(project_name, branch_name, 'S')
    sheet_story_file_count = output_workbook.add_sheet('story - file count' + '(' + str(len(story_file_count_rows)) + ')')
    if len(story_file_count_rows) > 0:
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

def generate_bar_chart(project_name, branch_name):

    import pycha
    import pycha.bar
    from Generate_Chart import Generate_Chart

    charGen = Generate_Chart()

    # show top 20 defect_file_count chart
    select_defect_file_count_rows = Reports_Common_Dao.search_count_of_rally_by_file_names(project_name, branch_name, 'D')
    if len(select_defect_file_count_rows) > 0:
        if len(select_defect_file_count_rows) > 20:
            charGen.barChart(select_defect_file_count_rows[1:21], "dist/defect_file_count.png", "Defect - Changed File Count Chart", "Changed File Count", "Defect ID", pycha.bar.HorizontalBarChart, "blue")
        else:
            charGen.barChart(select_defect_file_count_rows[1:], "dist/defect_file_count.png", "Defect - Changed File Count Chart", "Changed File Count", "Defect ID", pycha.bar.HorizontalBarChart, "blue")

    # show top 20 story_file_count chart
    select_story_file_count_rows = Reports_Common_Dao.search_count_of_rally_by_file_names(project_name, branch_name, 'S')
    if len(select_story_file_count_rows) > 0:
        if len(select_story_file_count_rows) > 20:
            charGen.barChart(select_story_file_count_rows[0:20], "dist/story_file_count.png", "Story - Changed File Count Chart", "Changed File Count", "Story ID", pycha.bar.HorizontalBarChart, "green")
        else:
            charGen.barChart(select_story_file_count_rows[0:], "dist/story_file_count.png", "Story - Changed File Count Chart", "Changed File Count", "Story ID", pycha.bar.HorizontalBarChart, "green")


def main(project_name, branch_name):

    output_2_xls(project_name, branch_name)
    generate_bar_chart(project_name, branch_name)

if __name__ == '__main__':
    # import sys
    # main(sys.argv[-2], sys.argv[-1])
    main("SPS", "develop_rel_1.7.0")