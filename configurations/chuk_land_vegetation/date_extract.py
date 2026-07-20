import math
import os
import datetime

def date_extract(filepath, ds):
    # extract the date from the filename as the land vegetation files have unreliable dates
    # example filename EOCIS-XXXX-L2-CHUK-LEAF-GAP-FILLED-100m-20201216-20201231-V1.nc where XXXX=FAPAR or LAI
    filename = os.path.split(filepath)[-1]
    parts = filename.split("-")
    start_date = datetime.datetime.strptime(parts[8],"%Y%m%d").replace(tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime.strptime(parts[9], "%Y%m%d").replace(tzinfo=datetime.timezone.utc)
    duration = (end_date - start_date).total_seconds()/86400
    mid_duration_days = math.floor(duration/2)
    mid_date = start_date + datetime.timedelta(days=mid_duration_days)
    return (start_date, mid_date,end_date)
