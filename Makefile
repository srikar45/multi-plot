# Default Python version to use for tests
PYTHON=python3.6
PYTHON_VER=$(subst python,,$(PYTHON))

# Python versions to test
# TODO: Use tox.
PYTHONVERS=python3.8 python3.7 python3.6

# VERSION is updated in "make version-update" step and derived
# from CHANGES.txt. Do not edit.
VERSION=0.0.1b1
SHELL:= /bin/bash

LONG_TESTS=false

# Location to install Anaconda. Important: This directory is removed when
# make test is executed.
CONDA=./anaconda3

# ifeq ($(shell uname -s),MINGW64_NT-10.0-18362)
ifeq ($(TRAVIS_OS_NAME),windows)
  # CONDA=/c/tools/anaconda3
	CONDA=/c/tools/miniconda3
endif


CONDA_ACTIVATE=source $(CONDA)/etc/profile.d/conda.sh; conda activate

# ifeq ($(shell uname -s),MINGW64_NT-10.0-18362)
ifeq ($(TRAVIS_OS_NAME),windows)
	CONDA_ACTIVATE=source $(CONDA)/Scripts/activate; conda activate
endif

# Development:
# Test repository code:
#   make repository-test     # Test using $(PYTHON)
#   make repository-test-all # Test on all versions in $(PYTHONVERS)
#
# Making a local package:
# 1. Update CHANGES.txt to have a new version line
# 2. make package
# 3. make package-test-all
#
# Upload package to pypi.org test starting with uploaded package:
# 1. make release
# 2. Wait ~5 minutes and execute
# 3. make release-test-all
#    (Will fail until new version is available at pypi.org for pip install.
#     Sometimes takes ~5 minutes even though web page is immediately
#     updated.)
# 4. After package is finalized, create new version number in CHANGES.txt ending
#    with "b0" in setup.py and then run
#       make version-update
# 	git commit -a -m "Update version for next release"
#    This will update the version information in the repository to indicate it
#    is now in a pre-release state.

URL=https://upload.pypi.org/
REP=pypi

pythonw=$(PYTHON)

# ifeq ($(shell uname -s),MINGW64_NT-10.0-18362)
ifeq ($(TRAVIS_OS_NAME),windows)
	pythonw=python
endif

ifeq ($(UNAME_S),Darwin)
	# Use pythonw instead of python. On OS-X, this prevents "need to install
	# python as a framework" error. The following finds the path to the binary
	# of $(PYTHON) and replaces it with pythonw, e.g., 
	# /opt/anaconda3/envs/python3.6/bin/python3.6
	# -> 
	# /opt/anaconda3/envs/python3.6/bin/pythonw
	a=$(shell source activate $(PYTHON); which $(PYTHON))
	pythonw=$(subst bin/$(PYTHON),bin/pythonw,$(a))
endif

################################################################################
# Test contents in repository using different python versions
test:
	make repository-test-all

repository-test-all:
	- rm -rf $(CONDA)
	@ for version in $(PYTHONVERS) ; do \
		make repository-test PYTHON=$$version ; \
	done

# These require visual inspection.
repository-test:
	@make clean
	- conda remove --name $(PYTHON) --all -y
	make condaenv PYTHON=$(PYTHON)
	$(CONDA_ACTIVATE) $(PYTHON); $(PYTHON) setup.py develop | grep "Best"
	$(CONDA_ACTIVATE) $(PYTHON); pip install pytest pillow; pip install .
	$(CONDA_ACTIVATE) $(PYTHON); python -m pytest -rx -rP -v test/test_hapiplot.py

repository-test-other:
	# Run using pythonw instead of python only so plot windows always work
	# for programs called from command line. This is needed for (at least)
	# OS-X, Python 3.5, and matplotlib instaled from pip.
	$(CONDA_ACTIVATE) $(PYTHON); $(pythonw) hapiplot_demo.py
	$(CONDA_ACTIVATE) $(PYTHON); $(pythonw) test/test_hapiplot_visual.py

	#$(CONDA_ACTIVATE) $(PYTHON); $(PYTHON) hapiclient/autoplot/autoplot_test.py
	#$(CONDA_ACTIVATE) $(PYTHON); $(PYTHON) hapiclient/gallery/gallery_test.py
	#jupyter-notebook ../client-python-notebooks/hapi_demo.ipynb
################################################################################

################################################################################
# Anaconda
CONDA_PKG=Miniconda3-latest-Linux-x86_64.sh
ifeq ($(shell uname -s),Darwin)
	CONDA_PKG=Miniconda3-latest-MacOSX-x86_64.sh
endif


condaenv:
# ifeq ($(shell uname -s),MINGW64_NT-10.0-18362)
ifeq ($(TRAVIS_OS_NAME),windows)
	cp $(CONDA)/Library/bin/libcrypto-1_1-x64.* $(CONDA)/DLLs/
	cp $(CONDA)/Library/bin/libssl-1_1-x64.* $(CONDA)/DLLs/
	$(CONDA)/Scripts/conda create -y --name $(PYTHON) python=$(PYTHON_VER)
else
	make $(CONDA)/envs/$(PYTHON) PYTHON=$(PYTHON)
endif

$(CONDA)/envs/$(PYTHON): ./anaconda3
	$(CONDA_ACTIVATE); \
		$(CONDA)/bin/conda create -y --name $(PYTHON) python=$(PYTHON_VER)

./anaconda3: /tmp/$(CONDA_PKG)
	bash /tmp/$(CONDA_PKG) -b -p $(CONDA)

/tmp/$(CONDA_PKG):
	curl https://repo.anaconda.com/miniconda/$(CONDA_PKG) > /tmp/$(CONDA_PKG) 
################################################################################

################################################################################
# Packaging
package:
	make clean
	make version-update
	python setup.py sdist

package-test-all:
	@ for version in $(PYTHONVERS) ; do \
		make repository-test-plots PYTHON=$$version ; \
	done

env-$(PYTHON):
	$(CONDA_ACTIVATE) $(PYTHON); \
		conda install -y virtualenv; \
		$(PYTHON) -m virtualenv env-$(PYTHON)

package-test:
	make package
	make env-$(PYTHON)
	cp hapiplot_demo.py /tmp # TODO: Explain why needed.
	source env-$(PYTHON)/bin/activate && \
		pip install pytest ipython && \
		pip uninstall -y hapiplot && \
		pip install -e ../client-python && \
		pip install dist/hapiplot-$(VERSION).tar.gz \
			--index-url $(URL)/simple  \
			--extra-index-url https://pypi.org/simple && \
		env-$(PYTHON)/bin/pytest -v test/test_hapiplot.py && \
		env-$(PYTHON)/bin/ipython /tmp/hapiplot_demo.py
################################################################################

################################################################################
release:
	make package
	make version-tag
	make release-upload

release-upload:
	pip install twine
	echo "rweigel, t1p"
	twine upload \
		-r $(REP) dist/hapiplot-$(VERSION).tar.gz \
		&& echo Uploaded to $(subst upload.,,$(URL))/project/hapiplot/

release-test-all:
	@ for version in $(PYTHONVERS) ; do \
		make release-test PYTHON=$$version ; \
	done

release-test:
	rm -rf env
	$(CONDA_ACTIVATE) $(PYTHON); pip install virtualenv; $(PYTHON) -m virtualenv env
	cp hapiplot_demo.py /tmp # TODO: Explain why needed.
	source env/bin/activate && \
		pip install pytest && \
		pip uninstall -y hapiplot && \
		pip install -e ../client-python && \\
		pip install 'hapiplot==$(VERSION)' \
			--index-url $(URL)/simple  \
			--extra-index-url https://pypi.org/simple && \
		env/bin/pytest -v test/hapiplot_test.py && \
		env/bin/pytest -v /tmp/hapiplot_demo.py
################################################################################

################################################################################
# Update version based on content of CHANGES.txt
version-update:
	python misc/version.py

version-tag:
	git commit -a -m "Last $(VERSION) commit"
	git push
	git tag -a v$(VERSION) -m "Version "$(VERSION)
	git push --tags
################################################################################

################################################################################
# Install package in local directory (symlinks made to local dir)
install-local:
#	python setup.py -e .
	$(CONDA_ACTIVATE) $(PYTHON); pip install --editable .

install:
	pip install 'hapiplot==$(VERSION)' --index-url $(URL)/simple
	conda list | grep hapiplot
	pip list | grep hapiplot
################################################################################

clean:
	- @find . -name __pycache__ | xargs rm -rf {}
	- @find . -name *.pyc | xargs rm -rf {}
	- @find . -name *.DS_Store | xargs rm -rf {}
	- @find . -type d -name __pycache__ | xargs rm -rf {}
	- @find . -name *.pyc | xargs rm -rf {}
	- @rm -f *~
	- @rm -f \#*\#
	- @rm -rf env
	- @rm -rf dist
	- @rm -f MANIFEST
	- @rm -rf .pytest_cache/
	- @rm -rf hapiclient.egg-info/
	- @rm -rf /c/tools/Anaconda3/envs/python3.6/Scripts/wheel.exe*
	- @rm -rf /c/tools/Anaconda3/envs/python3.6/vcruntime140.dll.*
