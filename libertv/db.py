from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel


class LiberDB:

    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName("localhost")
        self.db.setDatabaseName("libertv")
        self.db.setUserName("libertv")
        self.db.setPassword("libertv")
        self.db.setPort(5442)
        ok = self.db.open()

    def __del__(self):
        if self.db.open():
            self.db.close()

    def get_categories(self, parent_id=None, tags=None):
        # TODO: make it less stupid (it's more complicated than pyscopg2)
        query = QSqlQuery(self.db)
        sql = f"select id, position, name from libertv_categories"
        if parent_id:
            sql += f" where parent_id ={int(parent_id)}"
        sql += " order by position asc"
        query.exec(sql)
        results = []
        while query.next():
            results.append({
                "id": query.value(0),
                "name": query.value(2)
            })
        return results

    def get_series(self, category_id=None, parent_id=None, tags=None):
        # TODO: make it less stupid (it's more complicated than pyscopg2),
        #   sanitize and check parameters, etc. DRY!!
        query = QSqlQuery(self.db)
        sql = "select ls.id, ls.position, ls.name from libertv_series as ls"
        where = ""
        if parent_id:
            where += " where " if not where else " and "
            where += f" ls.parent_id ={int(parent_id)}"
        elif category_id:
            where += " where " if not where else " and "
            where += f" lsc.category_id={int(category_id)}"
            sql += " left join libertv_series_categories as lsc"
        elif tags:
            # TODO: different approaches: or, and
            where += " where " if not where else " and "
            where += f" tags_id in ({','.join(tags)})"
            sql += " left join libertv_series_tags as lsc"
        sql += where + " order by position asc"
        query.exec(sql)
        results = []
        while query.next():
            results.append({
                "id": query.value(0),
                "name": query.value(2)
            })
        return results

    def get_items(self, category_id=None, series_id=None, tags=None):
        # TODO: make it less stupid (it's more complicated than pyscopg2),
        #   sanitize and check parameters, etc. DRY!!
        query = QSqlQuery(self.db)
        sql = "select li.id, li.position, li.name from libertv_items as li"
        where = ""
        if category_id:
            where += " where " if not where else " and "
            where += f" lic.category_id={int(category_id)}"
            sql += " left join libertv_items_categories as lic"
        elif series_id:
            where += " where " if not where else " and "
            where += f" lis.series_id={int(series_id)}"
            sql += " left join libertv_items_series as lis"
        elif tags:
            # TODO: different approaches: or, and
            where += " where " if not where else " and "
            where += f" lit.tags_id in ({','.join(tags)})"
            sql += " left join libertv_items_tags as lit"
        sql += where + " order by li.position asc"
        query.exec(sql)
        results = []
        while query.next():
            results.append({
                "id": query.value(0),
                "name": query.value(2)
            })
        return results
