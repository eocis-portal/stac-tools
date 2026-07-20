import math
import os
import datetime

def date_extract(filepath, ds):
    # extract the date from the filename
    # example filename EOCIS-CHUK-L2_LST-MERGED-20201231-v1.0.nc
    filename = os.path.split(filepath)[-1]
    parts = filename.split("-")
    start_date = datetime.datetime.strptime(parts[4],"%Y%m%d").replace(tzinfo=datetime.timezone.utc).replace(hour=0,minute=0,second=0)
    mid_date = datetime.datetime.strptime(parts[4], "%Y%m%d").replace(tzinfo=datetime.timezone.utc).replace(hour=12,
                                                                                                              minute=0,
                                                                                                              second=0)
    end_date = datetime.datetime.strptime(parts[4], "%Y%m%d").replace(tzinfo=datetime.timezone.utc).replace(hour=23, minute=59, second=59)
    return (start_date, mid_date,end_date)
