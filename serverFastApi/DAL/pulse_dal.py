from contextlib import closing

from .db_core import DB_core
from models.Pulse import PulseDto

class pulse_DAL:

  @classmethod
  def add_pulse(cls, pulse):
    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        INSERT INTO pulse 
            (userId, pulse, activity, notes, recordDateTime )
        VALUES
            (?, ?, ?, ?, ?)""", (pulse.userId, pulse.pulse, pulse.activity, pulse.notes, pulse.recordDateTime,))
      con.commit()

      c.execute("""
        SELECT 
          pulseId, userId, pulse, activity, notes, recordDateTime
        FROM 
          pulse 
        WHERE 
          UserId=?
        ORDER BY 
          pulseId DESC LIMIT 1""", (pulse.userId,))      
      row = c.fetchone()

    if row:
      current_row_data = {
        "pulseId": row["pulseId"], 
        "userId": row["userId"], 
        "pulse": row["pulse"], 
        "activity": row["activity"],
        "notes": row["notes"], 
        "recordDateTime": row["recordDateTime"]
      }
      return PulseDto.parse_obj(current_row_data)
    else:
        return None

  @classmethod
  def update_pulse(cls, pulse):
    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        UPDATE 
          pulse 
        SET 
          pulse=?,
          activity=?,
          notes=?,
          recordDateTime=?
        WHERE
          pulseId=?""", (pulse.pulse, pulse.activity, pulse.notes, pulse.recordDateTime, pulse.pulseId,))
      con.commit()
    return pulse   

  @classmethod
  def delete_pulse(cls, pulseId):
    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        DELETE FROM
          pulse
        WHERE
          pulseId=?""", (pulseId,))
      con.commit()
    return None

  @classmethod
  def get_pulse_stats_by_user(cls, userId):
    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        SELECT 
          pulseId, userId, pulse, activity, notes, recordDateTime
        FROM
          pulse
        WHERE
          userId=?
        ORDER BY datetime(recordDateTime) DESC""", (userId,))
      rows = c.fetchall()

    pulseStats = []
    for row in rows:   
      current_row_data = {
        "pulseId": row["pulseId"], 
        "userId": row["userId"], 
        "pulse": row["pulse"], 
        "activity": row["activity"],
        "notes": row["notes"], 
        "recordDateTime": row["recordDateTime"]
      }
      pulseStats.append(PulseDto.parse_obj(current_row_data))

    print("")
    print("")
    print(pulseStats)
    print("")
    print("")

    return pulseStats  
