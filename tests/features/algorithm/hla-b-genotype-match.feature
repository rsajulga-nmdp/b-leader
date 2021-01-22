Feature: Define HLA-B Genotype Match
    For the B-leader microservice, HLA-B genotype matching is important to differentiate
    between cases that need leader peptide consideration the most.
    
    A genotype match is defined by its HLA allotype match grades as follows:
        AA - A genotype match occurs if both allotype pairs are allele matches.
        MA - A single mismatch constitutes one allele match and one mismatch.
        MM - A double mismatch occurs when both allotype pairs are mismatches.
        PA/PP/LP/MP - A potential single/double genotype match occurs when at least one pair has a potential match.
        LA/LP/LL/ML - An allele single/double genotype mismatch occurs when at least one pair has an allele mismatch.
        
    Since genotype matches and double mismatches have relatively well-defined patient 
    outcomes, leader peptide consideration is most impactful in single mismatch cases (MA).
    This is also possible through potential genotype 
    This is because low-risk and high-risk matches can be differentiated using leader peptide
    criteria.

    To prepare for leader matching, single mismatch cases (MA/AM) are arranged to highlight
    the unshared allotype first (MA).
    
    Scenario Outline: HLA-B Genotype Matches

        Given two HLA-B genotype names as <Genotype One> and <Genotype Two>
        When sorting the order of the genotypes
        And evaluating the match grades between the two genotypes and flipping as needed
        Then the genotypes are found to be <Sort One> and <Sort Two>, respectively
        And the match grades are found to be <Match Grades>
        And the matched genotypes are found to be <Matched One> and <Matched Two>
        And the genotypes were matched as <Flip One> and <Flip Two>, respectively

        Examples: Genotype Match
            |  Genotype One   |  Genotype Two   | Sort One | Sort Two | Match Grades |   Matched One   |   Matched Two   | Flip One  | Flip Two  |
            | B*08:01+B*40:02 | B*08:01+B*40:02 | unsorted | unsorted |      AA      | B*08:01+B*40:02 | B*08:01+B*40:02 | unflipped | unflipped |
            | B*08:01+B*40:02 | B*40:02+B*08:01 | unsorted | sorted   |      AA      | B*08:01+B*40:02 | B*08:01+B*40:02 | unflipped | unflipped |
            | B*40:02+B*08:01 | B*40:02+B*08:01 | sorted   | sorted   |      AA      | B*08:01+B*40:02 | B*08:01+B*40:02 | unflipped | unflipped |
        
        Examples: Single Mismatch
            |  Genotype One    |  Genotype Two    | Sort One | Sort Two | Match Grades |   Matched One    |   Matched Two    | Flip One  | Flip Two  |
            | B*07:01+B*40:01  | B*08:01+B*40:01  | unsorted | unsorted |      MA      | B*07:01+B*40:01  | B*08:01+B*40:01  | unflipped | unflipped |
            | B*47:02+B*08:112 | B*07:01+B*08:112 | sorted   | unsorted |      MA      | B*47:02+B*08:112 | B*07:01+B*08:112 | flipped   | unflipped |
            | B*40:02+B*07:02  | B*35:01+B*07:02  | sorted   | sorted   |      MA      | B*40:02+B*07:02  | B*35:01+B*07:02  | flipped   | flipped   |

        Examples: Double Mismatch
            |  Genotype One   |  Genotype Two   | Sort One | Sort Two | Match Grades |   Matched One   |   Matched Two   | Flip One  | Flip Two  |
            | B*42:01+B*52:04 | B*07:01+B*34:01 | unsorted | unsorted |      MM      | B*42:01+B*52:04 | B*07:01+B*34:01 | unflipped | unflipped |
            | B*52:04+B*42:01 | B*07:01+B*34:01 | sorted   | unsorted |      MM      | B*42:01+B*52:04 | B*07:01+B*34:01 | unflipped | unflipped |

        Examples: Potential Single/Double Genotype Match
            | Genotype One |  Genotype Two   | Sort One | Sort Two | Match Grades | Matched One  |   Matched Two   | Flip One  | Flip Two  |
            | B*07:02:01G+B*58:01:01G  | B*07:02:01G+B*08:01 | unsorted   | unsorted   |      MP      | B*58:01:01G+B*07:02:01G  | B*08:01+B*07:02:01G | flipped | flipped |
            | B*42:01+B*15 | B*42:01+B*15:01 | sorted   | sorted   |      PA      | B*15+B*42:01 | B*15:01+B*42:01 | unflipped | unflipped |
            | B*07+B*07    | B*07+B*07       | unsorted | unsorted |      PP      | B*07+B*07    | B*07+B*07       | unflipped | unflipped |
            | B*14:03+B*07 | B*07:01+B*14:01 | sorted   | unsorted |      LP      | B*14:03+B*07 | B*14:01+B*07:01 | flipped   | flipped   |
            | B*15+B*07    | B*42+B*15       | sorted   | sorted   |      MP      | B*07+B*15    | B*42+B*15       | unflipped | flipped   |

        Examples: Single/Double Allele Genotype Mismatch
            |  Genotype One   |  Genotype Two   | Sort One | Sort Two | Match Grades |   Matched One   |   Matched Two   | Flip One  | Flip Two  |
            | B*08:01+B*52:04 | B*08:04+B*52:04 | unsorted | unsorted |      LA      | B*08:01+B*52:04 | B*08:04+B*52:04 | unflipped | unflipped |
            | B*14:01+B*07:01 | B*14:03+B*07    | sorted   | sorted   |      LP      | B*14:01+B*07:01 | B*14:03+B*07    | flipped   | flipped   |
            | B*14:01+B*07:01 | B*14:03+B*07:12 | sorted   | sorted   |      LL      | B*07:01+B*14:01 | B*07:12+B*14:03 | unflipped | unflipped |
            | B*42:01+B*08:01 | B*40:01+B*08:03 | sorted   | sorted   |      ML      | B*42:01+B*08:01 | B*40:01+B*08:03 | flipped   | flipped   |