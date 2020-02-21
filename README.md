# Xports

## Description

Xports is a command line tool to write an archive from a server (default to the Knight lab's barnacke)
containing files in a given folder with given extensions.
    

## Installation

```
git clone https://github.com/FranckLejzerowicz/Xports.git
cd Xports
pip install -e .
```

```
pip install --upgrade git+https://github.com/FranckLejzerowicz/Xports.git
```

*_Note that pip should be for python3_

## Input

A path to a folder containing files you need to get copied from into a complex directories arborescence (option `-i`),
and the extension(s) of these files in order to select them (option `-e`). 

## Outputs
 
A tar.gz archive file containing all the files in the given input folder which name ends with the given extension(s).
It is assorted with a print of a suggested `scp` command to run to download the archive from a distant server. 

## Example
 
For the test folder of this package, which has this structure:
```
.
└── level_1
    ├── QZA_1.qza
    ├── QZA_2.qza
    ├── level_2.1
    │   ├── NOT_QZV_2.1.qza
    │   ├── level_3.1
    │   │   ├── QZV_3.1.1.qzv
    │   │   └── QZV_3.1.2.qzv
    │   └── level_3.2
    │       ├── NOT_QZV_3.2.qza
    │       └── QZV_3.2.qzv
    ├── level_2.2
    │   ├── NOT_QZV_2.2.qza
    │   └── QZV_2.2.qzv
    └── level_2.3
        ├── NOT_QZV_2.3.1.qza
        └── NOT_QZV_2.3.2.qza
```
and this command:

`Xports -i Xports/tests -o Xports/tests/my-archive.tar.gz -e qzv`

One will obtain an archive containing these files:

```
.
├── level_2.1
│   ├── level_3.1
│   │   ├── QZV_3.1.1.qzv
│   │   └── QZV_3.1.2.qzv
│   └── level_3.2
│       └── QZV_3.2.qzv
└── level_2.2
    └── QZV_2.2.qzv
```

And this help print:
```
Moving 4 files with extentions ".qzv" to Xports/tests/exports_2020-02-20-16-23-21
Creating archive Xports/tests/output.tar.gz:
tar czf Xports/tests/output.tar.gz -C Xports/tests/exports_2020-02-20-16-23-21 .
Removing folder Xports/tests/exports_2020-02-20-16-23-21
Done! To copy this archive from this server to your home, copy(-edit)-paste this:

scp franck@distant.server.com:/Programs/Xports/Xports/tests/output.tar.gz .
```

## Usage

```
Usage: Xports [OPTIONS]

Options:
  -i, --i-folder TEXT   Folder to walk through to find files for export.
                        [required]
  -e, --p-exts TEXT     Files extensions to select (default = qzv).  [default:
                        qzv]
  -o, --o-archive TEXT  Output archive file.  [required]
  --version             Show the version and exit.
  --help                Show this message and exit.
```

### Bug Reports

contact `flejzerowicz@health.ucsd.edu`