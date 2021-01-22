Feature: Define Leader Genotype
    For the B-leader microservice, a **leader genotype** is a pair of leader allotypes.
    This is represented via a two-character code consisting of M's and T's.
    
    Scenario Outline: Leader genotype name

        Given that the leader genotype name is <Leader Genotype>
        When evaluating the validity of the leader genotype name
        Then the leader genotype name is found to be <Validity>

        Examples: Valid Genotypes
            | Leader Genotype | Validity |
            |       MT        |   valid  |
            |       MM        |   valid  |
            |       TM        |   valid  |

        Examples: Invalid Genotypes
            | Leader Genotype | Validity |
            |       M+T       |  invalid |
            |       LL        |  invalid |
            |       K+L       |  invalid |