Feature: Define HLA-B Genotype
    For the B-leader microservice, genotypes are defined as a pair of B-alleles.
    In the GL String format, the alleles are separated by `+` (unphased) and `~` (phased).
    The allotypes within the genotype should be ordered based on the numeric code,
    where the smaller number precedes the larger one.

    Scenario Outline: Genotype validation, sorting, and allotype retrieval

        Given that the genotype name is <Genotype>
        When evaluating the validity of the genotype name
        And retrieving the individual allotypes
        Then the sorted genotype name is found to be <Sorted Genotype>
        And the allotypes are <First Allotype> and <Second Allotype>

        Examples: Valid Genotypes
            | Genotype              | Sorted Genotype       | First Allotype | Second Allotype |
            | B*35+B*40             | B*35+B*40             |     B*35       |     B*40        |
            | B*35+B*35:01          | B*35:01+B*35          |     B*35:01    |     B*35        |
            | B*35:01+B*35:01:01    | B*35:01:01+B*35:01    |     B*35:01:01 |     B*35:01     |
            | B*40:02+B*07:01       | B*07:01+B*40:02       |     B*07:01    |     B*40:02     |
            | B*112~B*12            | B*12~B*112            |     B*12       |     B*112       |
            | B*40:02+B*40:01       | B*40:01+B*40:02       |     B*40:01    |     B*40:02     |
            | B*40:01:02+B*40:01:01 | B*40:01:01+B*40:01:02 |    B*40:01:01  |    B*40:01:02   |

        Examples: Invalid Genotypes
            | Genotype        | Sorted Genotype | First Allotype | Second Allotype |
            | B*35+B*40+B*01  |     invalid     |   unavailable  |    unavailable  |
            | B*08:01^B*02:01 |     invalid     |   unavailable  |    unavailable  |
            | B*8:01^C*02:01  |     invalid     |   unavailable  |    unavailable  |

    Scenario: Genotype flipping during genotype matching

        Given that the sorted genotype name is "B*40:01+B*40:02"
        When flipped to align with another genotype during matching
        Then the genotype is found to be "flipped"
        And the flipped genotype name is found to be "B*40:02+B*40:01"