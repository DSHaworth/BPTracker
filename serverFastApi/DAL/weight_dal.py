from contextlib import closing

from .db_core import DB_core
from models.Weight import WeightDto

class weight_DAL:

  @classmethod
  def add_weight(cls, weight):
    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        INSERT INTO weight 
            (userId, weight, notes, recordDateTime )
        VALUES
            (?, ?, ?, ?)""", (weight.userId, weight.weight, weight.notes, weight.recordDateTime,))
      con.commit()
    return weight   

  @classmethod
  def get_weights_by_user(cls, userId):

    con = DB_core.connect()
    with closing(con.cursor()) as c:
      c.execute("""
        SELECT 
          weightId, userId, weight, notes, recordDateTime
        FROM
          weight
        WHERE
          userId=?
        ORDER BY datetime(recordDateTime) DESC""", (userId,))
      rows = c.fetchall()

    weights = []
    for row in rows:   
      current_row_data = {
        "weightId": row["weightId"], 
        "userId": row["userId"], 
        "weight": row["weight"], 
        "notes": row["notes"], 
        "recordDateTime": row["recordDateTime"]
      }
      weights.append(WeightDto.parse_obj(current_row_data))
    return weights  
