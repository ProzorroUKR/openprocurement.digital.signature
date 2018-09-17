## openprocurement.digital.signature
#### Description
Digital signature service - for imposition an electronic digital signature on documents.

#### Installation
* clone repository
* python bootstrap.py
* ./bin/buildout -N

#### Requirements

* python 2.7.13
* setuptools 18.3.2

#### Virtualenv requirements

#####LD_LIBRARY_PATH  
######*Example:* 
*echo 'export LD_LIBRARY_PATH=/<project_path>/openprocurement/digital/signature/components/EUSignCP/interface/x64/_EUSignCP.so:/path/to/lib:/<project_path>/openprocurement/digital/signature/components/EUSignCP/Modules/64:$LD_LIBRARY_PATH' >> .env/bin/activate*

#####MALLOC_CHECK_
######*Example:*
*export MALLOC_CHECK_=0*

####Run tests
*./bin/nosetests openprocurement/digital/signature/tests/*

