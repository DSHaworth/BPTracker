from contextlib import closing
from db_core import DB_core
from models import BPStat

class DAL_bpstat:

    @classmethod
    def add_bpstat(cls, bpstat):
        con = DB_core.connect()
        with closing(con.cursor()) as c:
            c.execute("""
                INSERT INTO bpstats 
                    (userId, sys, dia, position, activity, notes, recordDateTime )
                VALUES
                    (?, ?, ?, ?, ?, ?)""", (bpstat.userId, bpstat.sys, bpstat.dia, bpstat.position, bpstat.activity, bpstat.notes, bpstat.recordDateTime,))
            con.commit()
        return bpstat    