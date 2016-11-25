""" The data is available from Geonet, the official source of New
Zealand earthquake hazard data:

http://wfs.geonet.org.nz/geonet/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonet:quake_search_v1&outputFormat=csv

Geonet Data policy
==================

All data and images are made available free of charge through the
GeoNet project to facilitate research into hazards and assessment of
risk. GeoNet is sponsored by the New Zealand Government through its
agencies: Earthquake Commission (EQC), GNS Science and Land
Information New Zealand (LINZ). The use of data or images is subject
to the following conditions:

Users are requested to acknowledge the GeoNet project sponsors as the
source of the data or images. (Suggested text: We acknowledge the New
Zealand GeoNet project and its sponsors EQC, GNS Science and LINZ, for
providing data/images used in this study.)

The GeoNet project sponsors accept no liability for any loss or
damage, direct or indirect, resulting from the use of the data or
images provided.  The GeoNet project sponsors do not make any
representation in respect of the information's accuracy, completeness
or fitness for any particular purpose.

"""

URL = "http://wfs.geonet.org.nz/geonet/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonet:quake_search_v1&outputFormat=csv"

from pathlib import Path
import requests
import karmapi
import pandas

def get(path):

    path = Path(path)

    r = requests.get(URL)

    path.write_bytes(r.content)

def datefix(df):

    tt = df.origintime.apply(lambda x: x[:19])

    df.index = pandas.to_datetime(tt)

    return df

    

    
