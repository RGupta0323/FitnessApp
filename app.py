#!/usr/bin/env python3

import aws_cdk as cdk

from fitness_app.fitness_app_stack import FitnessAppStack


app = cdk.App()
FitnessAppStack(app, "fitness-app")

app.synth()
