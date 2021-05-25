from hapiclient import hapi
from hapiplot import hapiplot


if True:
    server     = 'http://hapi-server.org/servers-dev/TestData2.1/hapi'
    dataset    = 'dataset1'
    parameter  = 'matrix'
    start      = '1970-01-01Z'
    stop       = '1970-01-01T00:00:11Z'
    opts       = {'logging': True, 'usecache': False}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts      = {'logging': True, 'returnimage': True, 'usecache': False}
    hapiplot(data, meta, **popts)

if False:
    server     = 'http://hapi-server.org/servers/SSCWeb/hapi'
    dataset    = 'rbspa'
    start      = '2012-08-31T00:00:00.000Z'
    stop       = '2012-08-31T23:59:59.999Z'
    parameters = 'Time'
    opts       = {'logging': True, 'usecache': True}    
    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    hapiplot(data, meta, **opts)

if False:
    # CDAWeb data - Magnitude and BGSEc from dataset AC_H0_MFI
    server     = 'https://cdaweb.gsfc.nasa.gov/hapi'
    dataset    = 'AC_H0_MFI'
    start      = '1997-12-10T00:00:00'
    stop       = '1997-12-11T10:00:00'
    parameters = 'Magnitude,BGSEc'
    opts       = {'logging': True, 'usecache': True}    
    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    hapiplot(data, meta, **opts)
    
    opts['returnimage'] = True
    meta = hapiplot(data, meta, **opts)
    fig = meta['parameters'][1]['hapiplot']['figure']