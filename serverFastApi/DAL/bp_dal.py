from contextlib import closing

from .db_core import DB_core
from models.Bp import BpDto

class bp_DAL:

  @classmethod
  def add_bp(cls, bp):
    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        INSERT INTO bp 
            (userId, sys, dia, position, arm, activity, notes, recordDateTime )
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)""", (bp.userId, bp.sys, bp.dia, bp.position, bp.arm, bp.activity, bp.notes, bp.recordDateTime,))
      con.commit()

      c.execute("""
        SELECT 
          bpId, userId, sys, dia, position, arm, activity, notes, recordDateTime
        FROM 
          bp 
        WHERE 
          UserId=?
        ORDER BY 
          bpId DESC LIMIT 1""", (bp.userId,))      
      row = c.fetchone()

    if row:
      dto = cls.getDtoFromRow(row)
      return dto
    else:
        return None

  @classmethod
  def update_bp(cls, bp):
    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        UPDATE 
          bp 
        SET 
          sys=?,
          dia=?,
          position=?,
          activity=?,
          notes=?,
          recordDateTime=?
        WHERE
          bpId=?""", (bp.sys, bp.dia, bp.position, bp.activity, bp.notes, bp.recordDateTime, bp.bpId,))
      con.commit()
    return bp   

  @classmethod
  def delete_bp(cls, bpId):
    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        DELETE FROM
          bp
        WHERE
          bpId=?""", (bpId,))
      con.commit()
    return None

  @classmethod
  def get_bp_by_user(cls, userId):
    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        SELECT 
          bpId, userId, sys, dia, position, arm, activity, notes, recordDateTime
        FROM 
          bp 
        WHERE 
          UserId=?
        ORDER BY 
          datetime(recordDateTime) DESC""", (userId,))
      rows = c.fetchall()

    items = []
    for row in rows:   
      dto = cls.getDtoFromRow(row)
      items.append(dto)
    return items 

  @classmethod
  def getDtoFromRow(cls, row):
    current_row_data = {
      "bpId": row["bpId"], 
      "userId": row["userId"], 
      "sys": row["sys"], 
      "dia": row["dia"], 
      "position": row["position"], 
      "arm": row["arm"],
      "activity": row["activity"],
      "notes": row["notes"], 
      "recordDateTime": row["recordDateTime"]
    }
    return BpDto.parse_obj(current_row_data)
  