# Copyright (c) 2015. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class MutantProteinSequence(object):
    """
    Transcript effects can be used to determine the mutant protein sequence(s)
    arising from a variant. Since multiple effects may result in the same
    sequence (or sequence fragment in a region of interest), we can use
    MutantProteinSequence objects to keep track of each unique sequence (and the
    collection of Effects which gave rise to it).
    """

    def __init__(
            self,
            sequence,
            mutation_start_offset,
            mutation_end_offset,
            effects):
        """
        sequence : str
            Amino acid sequence

        mutation_start_offset : int
            Position before first mutated residue in the sequence
            (half-open/interbase coordinates)

        mutation_end_offset : int
            Position after last mutated residue in the sequence
            (half-open/interbase coordinates)

        effects : list of Effect objects
            The same sequence may come from multiple transcript effects
            across multiple transcripts.
        """
        self.sequence = sequence
        self.mutation_start_offset = mutation_start_offset
        self.mutation_end_offset = mutation_end_offset
        self.effects = effects
