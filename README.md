# sitesync
This tool performs a sync of a site heirachy to CMX/DNA Spaces.

## Getting stated
First (optional) step, create a vitualenv. This makes it less likely to clash with other python libraries in future.
Once the virtualenv is created, need to activate it.
```buildoutcfg
python3 -m venv env3
source env3/bin/activate
```

Next clone the code.

```buildoutcfg
git clone https://github.com/aradford123/sitesync.git
```

Then install the  requirements (after upgrading pip). 
Older versions of pip may not install the requirements correctly.
```buildoutcfg
pip install -U pip
pip install -r requirements.txt
```

Edit the dnac_vars file to add your DNAC and credential.  You can also use environment variables.

## Running the program
The program requires a valid site path in the hierachy.  Global will do the entire tree.

```
$ ./site_sync.py --sitename Global/AUS 
Task completed:Success - elapsed time:34sec

```

There are two optional arguments -v for loggin and --timeout for the timeout to wait for the task (default is 100 seconds).  Don't set this too low as the program will stop polling the task.

```
$ ./site_sync.py --sitename Global/AUS --timeout 2
Task b2e5f45d-0cba-44fb-85aa-d5cd89710fc2 did not complete within the specified timeout (2 seconds)
```
