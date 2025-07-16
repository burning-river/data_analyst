#!/usr/bin/env python
import sys
import os
import warnings

from datetime import datetime

from analyst.crew import Analyst

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
os.makedirs('output', exist_ok=True)
os.makedirs('output/templates', exist_ok=True)
os.makedirs('output/static', exist_ok=True)

requirements = """
A data analysis platform that can analyze data and provide insights.
The platform should allow a user to upload a csv data file.
The platform should read the data from the csv file.
The platform should provide the size of the data in rows and columns.
The platform should provide the data types of the columns.
The platform should provide the number of missing values in each column of the data.
For every numeric column, the platform should provide the mean, median, mode, standard deviation, and range.
For every categorical column, the platform should provide the mode, and the number of unique values.
"""
module_name = "analyst.py"
class_name = "Analyst"

def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }
    
    try:
        Analyst().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }
    try:
        Analyst().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Analyst().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "requirements": requirements,
        'module_name': module_name,
        'class_name': class_name
    }
    
    try:
        Analyst().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
