#Web-server for TOPCONS2

##Description:
    This is the web-server implementation of the TOPCONS2 workflow.
    The web-server is developed with Django 1.6.4

    TOPCONS2 is an updated version of the widely used TOPCONS for predicting
    membrane protein topologies using consensus prediction.
    It is faster yet more accurate than the old TOPCONS according to our solid
    benchmarking. Moreover, it predicts not only the trans-membrane helices,
    but also the location of signal peptide

    This software is open source and licensed under the GPL license

##Author
Nanjiang Shu

Short-term bioinformatics support at NBIS

Email: nanjiang.shu@scilifelab.se

## Reference
Tsirigos, K.D.*, Peters, C.*, Shu, N.*, Kall, L., Elofsson, A., 2015. The TOPCONS
web server for consensus prediction of membrane protein topology and signal
peptides. Nucleic Acids Res. 43, W401-W407 (*Co-first authors)

## Installation

1. Install dependencies for the web server
    * Apache
    * mod\_wsgi

2. Install the virtual environments by 

    $ bash setup_virtualenv.sh

3. Create the django database db.sqlite3

4. Run 

    $ bash init.sh

    to initialize the working folder

5. In the folder `proj`, create a softlink of the setting script.

    For development version

        $ ln -s dev_settings.py settings.py

    For release version

        $ ln -s pro_settings.py settings.py

    Note: for the release version, you need to create a file with secret key
    and stored at `/etc/django_pro_secret_key.txt`

6.  On the computational node. run 

    $ virtualenv env --system-site-packages

    to make sure that python can use all other system-wide installed packages

