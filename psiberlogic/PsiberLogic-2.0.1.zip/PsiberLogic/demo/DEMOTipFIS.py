# -*- coding: utf-8 -*-
"""
TipFIS is an example usage of the PsiberLogic package.  It determines the tip percentage
of a meal given the quality of the food and the service.

Copyright (C) 2015  Psibernetix Inc.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

Created by:  Dr. Nick Ernest, Psibernetix Inc. CEO

Dates:      Action taken:
7/15/2015   Created.
"""
import numpy as NumPy
import PsiberLogic

# time is only imported for testing
import timeit

def TipFISMake():
    """
    Inputs(2): Food, Service
    Output(1): Tip
    """

    # Initialize output variable.
    Tip = NumPy.linspace(0., 1., 101)
    # Controller
    FIS = PsiberLogic.Controller(Tip, PsiberLogic.Centroid)

    # Food Membership Functions (input)
    FoodBad = PsiberLogic.DecreasingRamp(0, .5)
    FoodMed = PsiberLogic.Triangle(0, .5, 1)
    FoodGood = PsiberLogic.IncreasingRamp(.5, 1)

    # Service Membership Functions (input)
    ServiceBad = PsiberLogic.DecreasingRamp(0, .5)
    ServiceMed = PsiberLogic.Triangle(0, .5, 1)
    ServiceGood = PsiberLogic.IncreasingRamp(.5, 1)

    # Tip Membership Functions (output)
    TipBad = PsiberLogic.DecreasingRamp(0, .5)
    TipMed = PsiberLogic.Triangle(0, .5, 1)
    TipGood = PsiberLogic.IncreasingRamp(.5, 1)

    # Create lists of Membership Functions for the creation of rules
    FoodList = [FoodBad, FoodMed, FoodGood]
    ServiceList = [ServiceBad, ServiceMed, ServiceGood]
    TipList = [TipBad, TipMed, TipGood]

    # Create rules (9 in total for this example)
    # First example rule: If Food is Bad and Service is Bad, Tip is Bad
    FIS.AddRule(((FoodList[0], ServiceList[0]), TipList[0]))
    FIS.AddRule(((FoodList[0], ServiceList[1]), TipList[0]))
    FIS.AddRule(((FoodList[0], ServiceList[2]), TipList[1]))
    FIS.AddRule(((FoodList[1], ServiceList[0]), TipList[0]))
    FIS.AddRule(((FoodList[1], ServiceList[1]), TipList[1]))
    FIS.AddRule(((FoodList[1], ServiceList[2]), TipList[1]))
    FIS.AddRule(((FoodList[2], ServiceList[0]), TipList[1]))
    FIS.AddRule(((FoodList[2], ServiceList[1]), TipList[2]))
    FIS.AddRule(((FoodList[2], ServiceList[2]), TipList[2]))

    return FIS

# This section is for testing this function
if __name__ == '__main__':
    # Create the TipFIS by calling the above
    TipFIS = TipFISMake()
    # Set a value for denormalizing the output from TipFIS
    MaximumTip = 0.3
    print(type(TipFIS))

    # The food and service inputs between 0 and 1
    NormalizedInputs = (0.1, 0.9)

    # Crisp output of the FIS
    CristOutput = TipFIS(NormalizedInputs)
    print("Crisp Output: ", CristOutput)

    # Actual tip percentage
    DenormalizedTip = CristOutput * MaximumTip
    print("Tip Value: ", DenormalizedTip * 100, "%")

    t0 = timeit.default_timer()
    TimeTrials = 10000
    for TimeTrial in range(TimeTrials):
        CristOutput = TipFIS(NormalizedInputs)

    t1 = timeit.default_timer()

    print("Took ", (t1-t0), " seconds to complete ", TimeTrials, " calls")
    print("Averaged to be ", (t1-t0)/TimeTrials, " seconds per call")
