import os 

from hapiclient import hapi
from hapiplot import hapiplot

from imgcheck import imgcheck

logging = True
returnimage = True

def test_2_0():
    # All TestData2.0 parameters
    
    server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset    = 'dataset1'
    start      = '1970-01-01Z'
    stop       = '1970-01-01T00:00:11Z'
    opts       = {'logging': logging, 'usecache': False}
    
    meta = hapi(server, dataset, **opts)

    for i in range(0,len(meta['parameters'])):
        parameter  = meta['parameters'][i]['name']
        data, metax = hapi(server, dataset, parameter, start, stop, **opts)

        if False and i > 0: # Time parameter alone when i = 0. No fill allowed for time parameter.
            # Change fill value to be same as second element of parameter array.
            metax["parameters"][1]['fill'] = data[parameter].take(1).astype('U')

        popts = {'useimagecache': False, 'logging': logging, 'returnimage': True}

        metap = hapiplot(data, metax, **popts)

        idx = 1
        if i == 0: # Time parameter
            idx = 0

        img2 = metap['parameters'][idx]['hapiplot']['image']

        dir_path = os.path.dirname(os.path.realpath(__file__))

        ref_file = os.path.join(dir_path, "imgs", "2.0", parameter + ".ref.png")

        imgcheck(ref_file, img2, show_diff=False, generate_ref_files=False)


def test_2_1():
    # All TestData2.1 parameters

    server     = 'http://hapi-server.org/servers-dev/TestData2.1/hapi'
    dataset    = 'dataset1'
    start      = '1970-01-01Z'
    stop       = '1970-01-01T00:00:11Z'
    opts       = {'logging': logging, 'usecache': False}

    meta = hapi(server, dataset, **opts)
    for i in range(0,len(meta['parameters'])):
        parameter  = meta['parameters'][i]['name']
        data, metax = hapi(server, dataset, parameter, start, stop, **opts)
        if False and i > 0: # Time parameter alone when i = 0. No fill allowed for time parameter.
            # Change fill value to be same as second element of parameter array.
            metax["parameters"][1]['fill'] = data[parameter].take(1).astype('U')

        popts = {'useimagecache': False, 'logging': logging, 'returnimage': returnimage}

        if parameter == 'matrix':
            # The string 
            #   '$\Delta T_{xy}=1$'
            # causes the error
            #    Unknown symbol: \Delta, found '\'  (at char 0), (line:1, col:1)
            # only when FigCanvasAgg is the back-end an using Matplotlib 3.2.2 and 3.4.2
            # The string
            #   '$\Delta$ $T_{xy}=1$'
            # does not cause an error. Seems to be a bug in Matplotlib.
            metax['parameters'][1]['label'][0][1] = r'$\Delta$ $T_{xy}=1$'

        metap = hapiplot(data, metax, **popts)

        if returnimage == False:
            continue

        idx = 1
        if i == 0: # Time parameter
            idx = 0

        img2 = metap['parameters'][idx]['hapiplot']['image']

        dir_path = os.path.dirname(os.path.realpath(__file__))

        ref_file = os.path.join(dir_path, "imgs", "2.1", parameter + ".ref.png")

        imgcheck(ref_file, img2, show_diff=False, generate_ref_files=False)

def test_saveimage():
    # Returned image should be same when saveimage is True or False

    server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset    = 'dataset1'
    start      = '1970-01-01Z'
    stop       = '1970-01-01T00:00:11Z'
    parameters = 'scalar'
    opts       = {'logging': False, 'usecache': True}
    data, meta = hapi(server, dataset, parameters, start, stop, **opts)

    popts = {
                 'usecache': True,
                 'useimagecache': False,
                 'logging': True,
                 'saveimage': False,
                 'returnimage': True
             }

    meta = hapiplot(data, meta, **popts)
    img1 = meta['parameters'][1]['hapiplot']['image']
    #Image.open(io.BytesIO(img1)).show()

    popts['saveimage'] = True
    meta = hapiplot(data, meta, **popts)
    img2 = meta['parameters'][1]['hapiplot']['image']
    #Image.open(io.BytesIO(img1)).show()

    if img1 != img2:
        print('Images do not match')
        return False

    return True


if __name__ == '__main__':
    test_2_0()
    test_2_1()
    test_saveimage()