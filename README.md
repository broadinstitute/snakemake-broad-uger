Snakemake profile for Broad Institute UGER cluster
==================================================

[Snakemake][snakemake] is a Pythonic workflow description language, that is 
easily configurable to run in all sorts of environments. Since version 4.1, 
Snakemake contains a feature called 'profiles', for easy exchange of 
configuration presets for running in a certain environment. This repository 
contains a snakemake profile to run your workflow on the Broad's UGER cluster.

[snakemake]: https://snakemake.readthedocs.io/

Installation
------------

### Preparing a conda environment

The recommended way to use this Snakemake profile is to create a separate conda 
environment for your project. This environment will contain a separate Python 
installation specifically for your project, where you control which packages 
are installed. In the example below we will create an environment named 
`snakemake` (with the `-n` switch), but you can name it anything you want. 
Furthermore, Snakemake requires Python>=3.5, so we install Python 3 along with 
two additional packages: Snakemake itself and the package `cookiecutter` (used 
to install this profile).


```bash
use .anaconda3-5.0.1

# Create new conda environment with up to date snakemake
conda create -n snakemake python=3
source activate snakemake

pip install snakemake cookiecutter

# (Optional) You can now install additional dependencies specific to your 
# project
conda install numpy scipy ...
```

**NB:** Conda creates the environment by default in your home directory. At 
Broad, your home directory is limited to 5GB so this may fill up quickly. It's 
probably a good idea to store the Conda environment in some other place. This 
can be done by replacing `-n snakemake` with `--prefix 
/path/where/env/will/be/stored`, and also specify the path to your conda 
environment when issuing the `source activate` command.

### Install the Snakemake profile

Change to the directory containing your `Snakefile` and issue the following 
command:

```bash
cookiecutter gh:broadinstitute/snakemake-broad-uger
```

This command will ask a few questions: 

1. You can optionally specify a different profile name than the default
   (`broad-uger`).
2. Whether to use the `--immediate-submit` option of Snakemake. Currently not 
   recommended, until [this fix][bug] is included in a release.
3. Last but not least, specify the name (when using `-n` above) or the path 
   (when using `--prefix` above) to the conda environment you want to use.

[bug]:https://bitbucket.org/snakemake/snakemake/issues/753/using-immediate-submit-jobscripts-get


### Using the Snakemake profile

We're ready to go! To use this profile invoke Snakemake as follows:

```bash
snakemake --profile broad-uger ...
```

If you're not using `--immediate-submit`, the Snakemake master process must be 
alive for the whole duration of your workflow (i.e. until all jobs have 
finished). My recommendation would be to start the Snakemake process on one of 
the login nodes, in a `screen` session. This makes sure the Snakemake master 
process doesn't get killed when you lose your SSH connection.

Example:

```bash
# Start screen session with snakemake in the background
screen -dmS snakemake snakemake --profile broad-uger ...

# View output:
screen -x snakemake
```

The Snakemake master process is light weight so it shouldn't be a problem to 
run this on the login node.

Resource specification
----------------------

This profile determines the runtime, memory and amount of cores as follows:

* **Runtime**: specify in your `--cluster-config` file, with key `runtime`
* **Memory**: Specify in your rule under `resources` with key `mem_mb`. Can be 
  overridden by specifying a value in your `--cluster-config` file.
* **Cores/CPUs**: specify using `threads` per rule.
* **UGER project**: specify in `--cluster-config` file with key `project`

Read more about:

* [Snakemake cluster configuration][snakemake-config]
* [Specifying threads and other resources][snakemake-resources]

[snakemake-config]:http://snakemake.readthedocs.io/en/latest/snakefiles/configuration.html
[snakemake-resources]:http://snakemake.readthedocs.io/en/latest/snakefiles/rules.html#threads

Acknowledgements
----------------

The cluster submission and jobscripts are partly taken/inspired by the 
corresponding files in the [broadinstitute/viral-ngs][viral-ngs] repository.

[viral-ngs]: https://github.com/broadinstitute/viral-ngs/tree/master/pipes
