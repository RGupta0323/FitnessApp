#!/usr/bin/env python3

import aws_cdk as cdk

from infra.fitness_app_stack import FitnessAppStack


app = cdk.App()

# Dev (Test) Stack
FitnessAppStack(app, "fitness-app-dev-stack")

# Non-Prod (Pilot) Stack
FitnessAppStack(app, "fitness-app-nonprod-stack")

# Prod (Prod) Stack
FitnessAppStack(app, "fitness-app-prod-stack")

app.synth()
