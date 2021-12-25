import os
import sqlite3

async def find_channel(channel : int):
    if os.path.exists("channels_data.db"):
        conn = sqlite3.connect("channels_data.db", isolation_level=None)
        cur = conn.cursor()
        cur.execute("SELECT * FROM channels_data WHERE id=:Id", {"Id": channel})
        channelData = cur.fetchone()
        conn.close()
            
        return channelData

async def get_channels_list():
    if os.path.exists("channels_data.db"):
        conn = sqlite3.connect("channels_data.db", isolation_level=None)
        cur = conn.cursor()
        cur.execute("SELECT * FROM channels_data")

        rows = cur.fetchall()

        return rows

async def set_channel(channel_id : int, onOff : str, everyone_ping : str):
    conn = sqlite3.connect("channels_data.db", isolation_level=None)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS channels_data (id integer PRIMARY KEY, onoff text, everyone text)")
    # check channel data
    c.execute("SELECT * FROM channels_data WHERE id=:id", {"id": str(channel_id)})
    a = c.fetchone()
    if a is None:
        # add channel data
        c.execute(f"INSERT INTO channels_data VALUES({channel_id}, '{onOff}', '{everyone_ping}')")
    else:
        # modify channel data
        c.execute("UPDATE channels_data SET onoff=:onOff WHERE id=:Id", {"onOff": onOff, 'Id': channel_id})
        c.execute("UPDATE channels_data SET everyone=:everyone_ping WHERE id=:Id", {"everyone_ping": everyone_ping, 'Id': channel_id})
    conn.close()