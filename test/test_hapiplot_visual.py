import numpy as np

#tests = [10]
tests = range(0,9)
#tests = [10]
tests = range(1,2)
#tests = [8]
tests = [8]
tests = [9]

from hapiclient import hapi
from hapiplot import hapiplot

for tn in tests:

    if tn == 1 or tn == 2:
        # Compare png with GUI plot
        import io
        from PIL import Image

        title      = 'GUI and PNG should match visually'
        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        parameters = 'scalar'
        opts       = {'logging': False, 'usecache': False}
        popts      = {'useimagecache': False,
                      'logging': True,
                      'title': title,
                      'returnimage': True}

        if tn == 1:
            # returnimage=True for scalar parameter - compare with GUI plot
            parameters = 'scalar'
            data, meta = hapi(server, dataset, parameters, start, stop, **opts)
            meta = hapiplot(data, meta, **popts)
            img = meta['parameters'][1]['hapiplot']['image']
            Image.open(io.BytesIO(img)).show()

        if tn == 2:
            # returnimage=True for heatmap parameter - compare with GUI plot
            parameters = 'spectra'
            data, meta = hapi(server, dataset, parameters, start, stop, **opts)
            meta = hapiplot(data, meta, **popts)
            img = meta['parameters'][1]['hapiplot']['image']
            Image.open(io.BytesIO(img)).show()

        popts['title'] = title
        popts['returnimage'] = False
        hapiplot(data, meta, **popts)

    if tn == 3:
        # Transparency
        import io
        from PIL import Image

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
                    'saveimage': True,
                    'returnimage': True,
                    'title': 'Second image should have transparent background'
                 }

        meta = hapiplot(data, meta, **popts)
        img1 = meta['parameters'][1]['hapiplot']['image']
        Image.open(io.BytesIO(img1)).show()

        popts['rcParams'] = {'savefig.transparent': True}
        meta = hapiplot(data, meta, **popts)
        img2 = meta['parameters'][1]['hapiplot']['image']
        Image.open(io.BytesIO(img2)).show()

    if tn == 4:
        # Rc params
        import io
        from PIL import Image

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
                    'saveimage': True,
                    'returnimage': True,
                    'title': 'Both plots should have black bg and yellow text',
                    'rcParams': {
                        'savefig.transparent': False,
                        'figure.facecolor': 'black',
                        'savefig.facecolor': 'black',
                        'text.color': 'yellow',
                        'xtick.color': 'yellow',
                        'ytick.color': 'yellow',
                        'axes.labelcolor': 'yellow'
                    }
                 }

        meta = hapiplot(data, meta, **popts)
        img = meta['parameters'][1]['hapiplot']['image']
        Image.open(io.BytesIO(img)).show()

        popts['returnimage'] = False
        hapiplot(data, meta, **popts)

    if tn == 5:
        # Style and rc parameters before and after + tight layout

        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        parameters = 'vector'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        opts       = {'logging': True, 'usecache': False}

        #https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html
        #https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
        import matplotlib
        rclib =  matplotlib.style.library
        print('Style options available:')
        for key in rclib:
            print(key)

        popts = {
                    'logging': True,
                    'saveimage': False,
                    'style': 'classic',
                    'title': 'Tight layout test. Figures should match.'
                }

        data, meta = hapi(server, dataset, parameters, start, stop, **opts)

        if not matplotlib.get_backend() in matplotlib.rcsetup.interactive_bk:
            %matplotlib qt
            
        if matplotlib.get_backend() in matplotlib.rcsetup.interactive_bk:
            # Set labels and make tight layout after call to hapiplot
            meta = hapiplot(data, meta, **popts)
            fig = meta['parameters'][1]['hapiplot']['figure']
            fig.axes[0].set_ylabel('y label\nsub y label\nsub sub ylabel 2')
            fig.tight_layout()
            fig.show()
            # Two calls to fig.tight_layout() may be needed b/c of bug in PyQt:
            # https://github.com/matplotlib/matplotlib/issues/10361

            # Set labels and make tight in call to hapiplot
            popts['_rcParams'] = {'figure.bbox': 'tight'}
            popts['ylabel'] = 'y label\nsub y label\nsub sub ylabel 2'
            meta = hapiplot(data, meta, **popts)
        else:
            print("Skipping test because matplotlib backend is not interactive.")


    if tn == 6:

        # Spectra w/ only bin centers and different timeStampLocations
        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        parameters = 'spectra'
        opts       = {'logging': True, 'usecache': True}
        data, meta = hapi(server, dataset, parameters, start, stop, **opts)

        popts = {'logging': True}

        data['spectra'][3,3] = -1e31 # Add a fill value

        # Default
        popts['title'] = 'Default'
        hapiplot(data, meta, **popts)

        # Should be same as previous plot
        popts['title'] = 'Should be same as default plot.'
        meta['timeStampLocation'] = 'center'
        hapiplot(data, meta, **popts)

        popts['title'] = 'NaN patch should be between 00:03 and 00:04'
        meta['timeStampLocation'] = 'begin'
        hapiplot(data, meta, **popts)

        popts['title'] = 'NaN patch should be between 00:02 and 00:03'
        meta['timeStampLocation'] = 'end'
        hapiplot(data, meta, **popts)

    if tn == 7:

        # Spectra w/ only bin centers and different timeStampLocations
        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        parameters = 'spectra'
        opts       = {'logging': True, 'usecache': True}
        data, meta = hapi(server, dataset, parameters, start, stop, **opts)

        popts = {'logging': True}

        # Remove 6th time value so cadence is not uniform
        # Missing time value is at 00:00:06. Note that data at this time
        # takes on the value of data at 00:00:05. If we knew the bin,
        # width was uniform, values at 00:00:06 could be set as NaN.
        # heatmap does not assume the bin width is uniform. Some software
        # will assume bin width is uniform and equal to the difference
        # between timestamps.
        data = np.delete(data, 6, 0)

        for i in range(9):
            data['spectra'][i,i] = -1e31 # Add a fill value

        popts['title'] = 'Bins centered on timestamp; no value at 00:06'
        meta['timeStampLocation'] = 'center'
        hapiplot(data, meta, **popts)

        popts['title'] = 'Bins start on timestamp; no value at 00:06'
        meta['timeStampLocation'] = 'begin'
        hapiplot(data, meta, **popts)

        popts['title'] = 'Bins end on timestamp; no value at 00:06'
        popts['title'] = 'Should match previous'
        meta['timeStampLocation'] = 'end'
        hapiplot(data, meta, **popts)

