__author__ = 'LUOAL2'


import MySQLdb

DB_ARG_HOST = 'localhost'
DB_ARG_PORT = 3306
DB_ARG_INSTANCE = 'pythondb'
DB_ARG_USER = 'root'
DB_ARG_PASSWORD = 'adminpass'

class database_wrapper:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

def connect(arg_host, arg_port, arg_instance, arg_user, arg_password):
    conn = MySQLdb.connect(host=arg_host, user=arg_user, passwd=arg_password, db=arg_instance, port=arg_port)
    cur = conn.cursor()
    db_wrapper = database_wrapper(conn, cur)
    return db_wrapper

def commit_and_close(db_wrapper):
    db_wrapper.conn.commit()
    db_wrapper.cur.close()
    db_wrapper.conn.close()

def search_file_rally_mapping(project_name, branch_name, rally_type):
    select_file_rally_row = []
    try:
        c_db_wrapper = connect(DB_ARG_HOST, DB_ARG_PORT, DB_ARG_INSTANCE, DB_ARG_USER, DB_ARG_PASSWORD)

        args = []
        args.append(rally_type)
        args.append(project_name)
        args.append(branch_name)
        c_db_wrapper.cur.execute('''select src.SRC_FILE_NAME, rally.RALLY_UNIT_NUMBER
                                    from rally_unit rally, src_file src
                                    where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID
                                        and rally.RALLY_UNIT_TYPE = %s
                                        and exists (select *
                                                    from GIT_COMMIT git
                                                    where git.GIT_COMMIT_ID = src.GIT_COMMIT_ID
                                                    and git.GIT_COMMIT_SYSTEM_NAME = %s
                                                    and git.GIT_COMMIT_BRANCH_NAME = %s)
                                    order by src.SRC_FILE_NAME desc''', args)
        select_file_rally_row = c_db_wrapper.cur.fetchall()

    finally:
        commit_and_close(c_db_wrapper)

    # for row in select_file_rally_row:
    #     print row[0], "\t", row[1]

    return select_file_rally_row

def search_count_of_rally_by_file_names(project_name, branch_name, rally_type):
    select_file_rally_count_rows = []
    try:
        c_db_wrapper = connect(DB_ARG_HOST, DB_ARG_PORT, DB_ARG_INSTANCE, DB_ARG_USER, DB_ARG_PASSWORD)

        args = []
        args.append(rally_type)
        args.append(project_name)
        args.append(branch_name)
        c_db_wrapper.cur.execute('''select src.SRC_FILE_NAME, count(distinct(rally.RALLY_UNIT_ID)) as rally_count
                                    from rally_unit rally, src_file src
                                    where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID
                                    and rally.RALLY_UNIT_TYPE = %s
                                    and exists (select *
                                                from GIT_COMMIT git
                                                where git.GIT_COMMIT_ID = src.GIT_COMMIT_ID
                                                and git.GIT_COMMIT_SYSTEM_NAME = %s
                                                and git.GIT_COMMIT_BRANCH_NAME = %s)
                                    group by src.SRC_FILE_NAME
                                    order by rally_count desc''', args)
        select_file_rally_count_rows = c_db_wrapper.cur.fetchall()
    finally:
        commit_and_close(c_db_wrapper)

    # for row in select_file_rally_count_rows:
    #     print row[0], "\t", row[1]

    return select_file_rally_count_rows

def searhc_rally_file_mapping(project_name, branch_name, rally_type):
    select_rally_file_row = []
    try:
        c_db_wrapper = connect(DB_ARG_HOST, DB_ARG_PORT, DB_ARG_INSTANCE, DB_ARG_USER, DB_ARG_PASSWORD)

        args = []
        args.append(rally_type)
        args.append(project_name)
        args.append(branch_name)
        c_db_wrapper.cur.execute('''select rally.RALLY_UNIT_NUMBER, src.SRC_FILE_NAME
                                    from rally_unit rally, src_file src
                                    where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID
                                    and rally.RALLY_UNIT_TYPE = %s
                                    and exists (select *
                                                from GIT_COMMIT git
                                                where git.GIT_COMMIT_ID = src.GIT_COMMIT_ID
                                                and git.GIT_COMMIT_SYSTEM_NAME = %s
                                                and git.GIT_COMMIT_BRANCH_NAME = %s)
                                    order by rally.RALLY_UNIT_NUMBER desc''', args)
        select_rally_file_row = c_db_wrapper.cur.fetchall()

    finally:
        commit_and_close(c_db_wrapper)

    # for row in select_rally_file_row:
    #     print row[0], "\t", row[1]

    return select_rally_file_row

def search_count_of_file_by_rally_number(project_name, branch_name, rally_type):
    select_file_rally_count_rows = []
    try:
        c_db_wrapper = connect(DB_ARG_HOST, DB_ARG_PORT, DB_ARG_INSTANCE, DB_ARG_USER, DB_ARG_PASSWORD)

        args = []
        args.append(rally_type)
        args.append(project_name)
        args.append(branch_name)
        c_db_wrapper.cur.execute('''select rally.RALLY_UNIT_NUMBER, count(distinct(src.SRC_FILE_ID)) as count_src
                                    from rally_unit rally, src_file src
                                    where src.GIT_COMMIT_ID = rally.GIT_COMMIT_ID
                                    and rally.RALLY_UNIT_TYPE = %s
                                    and exists (select *
                                                from GIT_COMMIT git
                                                where git.GIT_COMMIT_ID = src.GIT_COMMIT_ID
                                                and git.GIT_COMMIT_SYSTEM_NAME = %s
                                                and git.GIT_COMMIT_BRANCH_NAME = %s)
                                    group by rally.RALLY_UNIT_NUMBER
                                    order by count_src desc''', args)
        select_file_rally_count_rows = c_db_wrapper.cur.fetchall()
    finally:
        commit_and_close(c_db_wrapper)

    # for row in select_file_rally_count_rows:
    #     print row[0], "\t", row[1]

    return select_file_rally_count_rows


def template(project_name, branch_name, rally_type):
    template_return = []
    try:
        c_db_wrapper = connect(DB_ARG_HOST, DB_ARG_PORT, DB_ARG_INSTANCE, DB_ARG_USER, DB_ARG_PASSWORD)

        args = []
        args.append(rally_type)
        args.append(project_name)
        args.append(branch_name)
        c_db_wrapper.cur.execute('''template_sql''', args)
        template_return = c_db_wrapper.cur.fetchall()
    finally:
        commit_and_close(c_db_wrapper)

    for row in template_return:
        print row[0], '\t', row[1]

    return template_return