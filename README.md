Snakemake profile for Broad Institute UGER cluster
==================================================

Snakemake is a Pythonic workflow description language, that is easily 
configurable to run in all sorts of environments. Since version 4.1, snakemake 
contains a feature called 'profiles', for each exchange of configuration 
presets for running in a certain environment. This repository contains a 
snakemake profile to run your workflow on the Broad's UGER cluster.

Installation
------------

Naturally, you'll have to be on the Broad cluster for this to work. The UGER 
cluster has a dotkit for loading Anaconda3 (`use Anaconda3`), and it even 
includes snakemake by default. This version of snakemake, however, is quite old 
(3.x). We'll need a separate conda environment for the new snakemake version.

```bash
use Anaconda3

# Create new conda environment with up to date snakemake
conda create -n snakemake python=3 snakemake cookiecutter
source activate snakemake
```

Change to your desired directory and install the snakemake profile:

```bash
cookiecutter gh:broadinstitute/snakemake-broad-uger
```

For explanation of the options see below. To run your workflow with this 
profile run snakemake as follows:

```bash
snakemake --profile broad-uger ...
```

Resource specification
----------------------

This profile determines the runtime, memory and amount of cores as follows:

* **Runtime**: specify in your `--cluster-config` file, with key `runtime`
* **Memory**: Specify in your rule under `resources` with key `mem_mb`. Can be 
  overridden by specifying a value in your `--cluster-config` file.
* **Cores/CPUs**: specify using `threads` per rule.

Additional options
------------------

When creating the profile using cookiecutter, it asks a few questions. You can 
give a different profile name than the default "broad-uger". Furthermore, it 
allows you to configure the following things:

* **immediate_submit**: Use Snakemake's `--immediate-submit` feature. This 
  means that the Snakemake master process will not wait until jobs are finished 
  and will submit all tasks directly to the cluster (and specify dependencies 
  where needed). This is useful if you don't want to run a long running process 
  on your cluster's head node.
* **global_conda_env**: We use a special conda environment to be able to use 
  the most current version of snakemake. You may want to run your workflow in a 
  different conda environment. By specifying the name of an existing conda 
  environment (or its path), this conda environment will be activated before 
  each task is run on a compute node.


Acknowledgements
----------------

The cluster submission and jobscripts are partly taken/inspired by the 
corresponding files in the [broadinstitute/viral-ngs][viral-ngs] repository.


[cookiecutter]: https://github.com/audreyr/cookiecutter
[viral-ngs]: https://github.com/broadinstitute/viral-ngs/tree/master/pipes
