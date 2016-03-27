# Scripts to generate proper workflow @ titan

```
usage: ./generate_workflow.py <opts>

GENERATE WORKFLOW @ TITAN

optional arguments:
  -h, --help            show this help message and exit

REQUIRED ARGUMENTS:
  --framework [caffe, theano, ...]
                        which framework will be used (default: None)
  --command [./scriptName.py [options]]
                        main command with options (default: None)

WORKING DIRS SETTINGS:
  --framework_dir [PATH]
                        path to store framework (default: $PROJWORK/hep105/software/)
  --software_dir [PATH]
                        path to store software (default: $MEMBERWORK/hep105/software/)
  --data_dir [PATH]     path to store data (default: $PROJWORK/hep105/data/)
  --log_dir [PATH]      path to store logs (default: $MEMBERWORK/hep105/logs/)
  --output_dir [PATH]   path to store output (default: $MEMBERWORK/hep105/output/)

INPUT FILES / SOFTWARE:
  --input_data [file1 file2 ...]
                        list of files to get from /proj/hep105/data (default:
                        )
  --software_list [/path1/software.list]
                        path to a file contains all required software
                        (default: /data/Dokumenty/ornl_workflow/software.list)

EXTRA OPTIONS:
  --tag [tag]           tag used for logs and output files names (default:
                        $USER_YYYY-MM-DD)
  --force_framework     get framework even if it exists already (default:
                        false)
  --force_data          get data files even if they exist already (default:
                        false)
  --no_archive          do not save files in HPSS after job is done
```

## REQUIRED ARGUMENTS

* `--framework` [`theano` or `caffe` (not there yet)] - define the list of external software required to run a job (see `utils.py::software_list`)

* `--command` [./myScript --option1...] - command to run through `aprun`

## DEFAULT FOLDERS

* Framework software and data are stored in $PROJWORK area (shared by whole group). They are copied only if not exist or forced to be updated.

* Software, logs, and output are stored in $MEMBERWORK area.

## INPUT data

* User can define necessary input files to be copied to `--data_dir` using `--input_data "file1 file2 ..."`. Files are assumed to be in HPSS project archive (`/proj/hep105/data/`)

## SOFTWARE

* User should modify `software.list` file, which contains a list of files for his software.

## ARCHIVE

* By default, everything from `--software_dir`, `--output_dir`, and `--log_dir` is saved to HPSS user archive (`/home/$USER/job_tag`). Once can disable archiving using `--no_archive`.
