#!/usr/bin/env python3

import sys
import subprocess

jobid = sys.argv[1]

try:
    proc = subprocess.run(["qstat", "-j", jobid], encoding='utf-8',
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if proc.returncode == 0:
        state = ""
        for line in proc.stdout.split('\n'):
            if line.startswith("job_state"):
                parts = line.split(":")
                state = parts[1].strip()

        if "E" in state:
            print("failed")
        else:
            print("running")
    else:
        proc = subprocess.run(["qacct", "-j", jobid], encoding='utf-8',
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if proc.returncode == 0:
            job_props = {}
            for line in proc.stdout.split('\n'):
                parts = line.split(maxsplit=1)
                if len(parts) <= 1:
                    continue

                key, value = parts
                job_props[key.strip()] = value.strip()

            if (job_props.get("failed", "1") == "0" and
                    job_props.get("exit_status", "1") == "0"):
                print("success")
            else:
                print("failed")
        else:
            # If not found with qstat or qacct, it's probably in some sort of
            # transistion phase (from running to finished), so let's not
            # confuse snakemake to think it may have failed.
            print("running")
except KeyboardInterrupt:
    pass

