from database.DB_connect import DBConnect
from model.track import Track


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select g.Name 
                    from genre g 
                    order by g.Name """
        cursor.execute(query)
        for row in cursor:
            results.append(row['Name'])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getMaxMinByGenre(genre):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select MIN(t.Milliseconds)/1000 as min, max(t.Milliseconds)/1000 as max
                    from genre g , track t 
                    where g.GenreId = t.GenreId 
                    and g.Name  = %s """
        cursor.execute(query, (genre,))
        for row in cursor:
            results.append((row['min'], row['max']))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllTracks(genre, min, max):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.*, count(distinct p.PlaylistId ) as NumP
                    from track t , genre g , playlisttrack p 
                    where t.GenreId = g.GenreId
                    and t.TrackId = p.TrackId 
                    and g.Name = %s
                    and t.Milliseconds/1000 between %s and %s
                    group by t.TrackId"""
        cursor.execute(query, (genre,min, max))
        for row in cursor:
            results.append(Track(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(genre, min, max, idMapT):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """with track_playlist as (
                    select t.TrackId as idT, count(distinct p.PlaylistId ) as numP
                from track t , genre g , playlisttrack p 
                where t.GenreId = g.GenreId 
                and t.TrackId = p.TrackId 
                and g.Name = %s
                and t.Milliseconds/1000 between %s and %s
                group by t.TrackId )
                select t1.idt as id1 , t2.idt as id2
                from track_playlist t1
                join track_playlist t2 on t1.nump = t2.nump 
                where t1.idt < t2.idt """
        cursor.execute(query, (genre, min, max))
        for row in cursor:
            results.append((idMapT[row['id1']], idMapT[row['id2']]))
        cursor.close()
        conn.close()
        return results