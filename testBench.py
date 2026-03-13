#!/usr/bin/env python3

from main import *
from peg_solitaire import *
from peg_duotaire import *
from peg_board import *
from search4e import *
from games4e import *
import time
import subprocess

def testBench():
    pcInfo = subprocess.run(["lscpu"], capture_output=True, text=True)
    print(f"CPU Info:")
    model_name = ""
    for line in pcInfo.stdout.splitlines():
        if "Model name:" in line:
            model_name = line.split(":")[1].strip()
            break
    print(f"\tModel Name: {model_name}\n")
    print("Testing Peg Solitaire...\n")

    for i in range(1, 5):

        print(f"Running {search_names.get(i)}...")

        times = []
        for _ in range(5):
            time = play_peg_solitaire(i, True)
            times.append(time)

        avg_time = sum(times) / len(times)
        print(f"Average Time: {avg_time:.2f}")
        print("\n")
    