# Allow "from hapiplot import hapiplot"
from hapiplot.hapiplot import hapiplot

# This is needed because setopts reads all rcParams and adds passed rcParams.
# The default rcParams include those that are depricated and so a warning is
# generated when these rcParams are used with a context manager.
import warnings

# TODO: Only filter warnings about these specific rcParams.
#ignores = ['datapath','savefig.frameon', 'text.latex.unicode', 'verbose.fileo', 'verbose.level', 'datapath']
warnings.filterwarnings(action='ignore', category=UserWarning)

__version__ = '0.0.1b4'