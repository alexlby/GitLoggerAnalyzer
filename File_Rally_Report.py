__author__ = 'LUOAL2'

import Reports_Common_Dao

def output_2_xls(project_name, branch_name):
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
    file_defect_rows = Reports_Common_Dao.search_file_rally_mapping(project_name, branch_name, "D")
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
    file_story_rows = Reports_Common_Dao.search_file_rally_mapping(project_name, branch_name, "S")
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
    file_defect_count_rows = Reports_Common_Dao.search_count_of_file_by_rally_number(project_name, branch_name, "D")
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
    file_story_count_rows = Reports_Common_Dao.search_count_of_file_by_rally_number(project_name, branch_name, "S")
    for row in file_story_count_rows:
        if (len(row[0]) == 0):
            continue
        sheet_file_story_count.write(file_story_count_row_index, 0, row[0], style)
        sheet_file_story_count.write(file_story_count_row_index, 1, row[1], style)
        file_story_count_row_index += 1
    sheet_file_story_count.col(0).set_width(30000)
    sheet_file_story_count.col(1).set_width(4000)

    output_workbook.save('dist/File_Rally.xls')

def generate_bar_chart(project_name, branch_name):

    import pycha
    import pycha.bar
    from Generate_Chart import Generate_Chart

    charGen = Generate_Chart()
    # show top 20 select_file_defect_count_rows chart
    select_file_defect_count_rows = Reports_Common_Dao.search_count_of_rally_by_file_names(project_name, branch_name, "D")
    charGen.barChart(select_file_defect_count_rows[0:20], "dist/file_defect_count.png", "File - Related Defects Count Chart", "Related Defects Count", "File Name", pycha.bar.VerticalBarChart, "blue")

    # show top 20 select_file_story_count_rows chart
    select_file_story_count_rows = Reports_Common_Dao.search_count_of_rally_by_file_names(project_name, branch_name, "S")
    charGen.barChart(select_file_story_count_rows[0:20], "dist/file_story_count.png", "File - Related Stories Count Chart", "Related Stories Count", "File Name", pycha.bar.VerticalBarChart, "green")


def main(project_name, branch_name):

    output_2_xls(project_name, branch_name)
    generate_bar_chart(project_name, branch_name)

if __name__ == '__main__':
    # import sys
    # main(sys.argv[-2], sys.argv[-1])
    main("SPS", "develop_rel_1.7.0")