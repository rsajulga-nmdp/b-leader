Feature: Determine HLA-B Leader Match Status
    
    To characterize the status of the leader types within an HLA-B mismatch,
    Petersdorf et al. 2019 defined a three-letter code: match status.
    Generated from genotypes with one shared allotype and one unshared allotype.
    The first letter represents the leader allotype of the patient on the unshared allotype.
    The second letter represents the leader allotype of the donor on the unshared allotype.
    The last letter represents the leader allotype of both patient and donor on the shared allotype.

    Scenario Outline: Obtaining the match status between two genotypes

        Given the HLA-B genotypes as <Genotype 1> and <Genotype 2>
        When the match status between them is computed
        Then the match status is found to be <Match Status>

        Examples: Ambiguity on "shared" allotype
            | Genotype 1   | Genotype 2      | Match Status |
            | B*07:XX+B*40:02 | B*07:65+B*40:02 |     MTT      |
            | B*40:02+B*07:XX | B*40:01+B*07:65 |     TTX      |
        
        Examples: Genotype match (AA)
            | Genotype 1      | Genotype 2      | Match Status |
            | B*08:01+B*40:02 | B*08:01+B*40:02 |   invalid    |
        
        Examples: Single mismatch (MA)
            | Genotype 1       | Genotype 2       | Match Status |
            | B*07:01+B*40:01  | B*08:01+B*40:01  |     MMT      |
            | B*47:02+B*08:112 | B*07:01+B*08:112 |     TMM      |
            | B*40:02+B*07:02  | B*35:01+B*07:02  |     TTM      |
            | B*07:02+B*07:02  | B*35:01+B*07:02  |     MTM      |
            | B*18:04+B*52:01/07 | B*18:01/18:17N+B*52:01  |     TTT      |
            | B*18:01:01:02+B*58:01:01 | B*18:01:01:02+B*18:01:01:02 | TTT |

        Examples: Double Mismatch
            | Genotype 1      | Genotype 2      | Match Status |
            | B*42:01+B*52:04 | B*07:01+B*34:01 |   invalid    |
            | B*42:01+B*52:04 | B*07:01+B*34:01 |   invalid    |
        
        Examples: Potential Single/Double Genotype Match
            | Match Code | Genotype 1   | Genotype 2      | Match Status |
            |     PA     | B*15+B*42:01 | B*15:01+B*42:01 |     TTM      |
            |     PP     | B*07+B*07    | B*07+B*07       |   invalid    |
            |     LP     | B*14:03+B*07 | B*14:01+B*07:02 |     MMM      |
            |     MP     | B*07+B*15    | B*42+B*15       |     MMT      |
            |     AP     | B*27:05/37+B*44:05/55 | B*27:05/37+B*44:02/55 | TTT |

        Examples: Single/Double Allele Genotype Mismatch
            | Match Code  | Genotype 1      | Genotype 2      | Match Status |
            |      LA     | B*08:01+B*52:04 | B*08:04+B*52:04 |     MMT      |
            |      LP     | B*14:01+B*07:02 | B*14:03+B*07    |     MMM      |
            |      LL     | B*07:01+B*14:01 | B*07:12+B*14:03 |   invalid    |
            |      ML     | B*42:01+B*08:01 | B*40:01+B*08:03 |   invalid    |

        Examples: Misc.
            | Match Code  | Genotype 1      | Genotype 2         | Match Status |
            |      LA     | B*15:23+B*35:01 | B*15:18+B*35:01/42 |     TTT      |
    
    Scenario: Obtaining the match statuses between a patient's genotype and multiple donors' genotypes

        Given the patient's HLA-B genotype is 'B*07:65+B*40:02'
        And the donors' HLA-B genotypes
            | HLA-B Genotype   |
            | B*07:01+B*40:02  |
            | B*52:04+B*40:02  |
            | B*42:01+B*40:02  |
            | B*08:112+B*40:02 |
        When the match statuses are evaluated
        Then they are found to be "TMT,TTT,TMT,TMT"