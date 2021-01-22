Feature: Define HLA-B Allotype Match
    For the B-leader microservice, HLA-B allotype matching sets up important context
    for leader matching. This is because leader matching can vastly improve the 
    event-free survival of patients who cannot find a full match (both allotypes) on
    *HLA-B*. Here, we define varying levels of matching (which also consider the various
    typing resolutions) between two HLA-B allotypes.
    
    Scenario Outline: HLA-B Allotypes 

        Given that the two HLA-B allotypes are <Allotype One> and <Allotype Two>
        When evaluating the match grade between the two allotypes
        Then the match grade is found to be <Match Grade>

        Examples: Allele Matches
            | Allotype One | Allotype Two | Match Grade |
            |    B*52:04   |   B*52:04    |      A      |
            |    B*08:02   |   B*08:02    |      A      |
        
        Examples: Allele Mismatch
            | Allotype One | Allotype Two | Match Grade |
            |    B*07:02   |   B*07:01    |      L      |
            |    B*15:11   |   B*15:112   |      L      |

        Examples: Potential Matches
            | Allotype One | Allotype Two | Match Grade |
            |     B*15     |     B*15     |      P      |
            |     B*08     |     B*08:01  |      P      |
        
        Examples: Mismatch
            | Allotype One | Allotype Two | Match Grade |
            |    B*15:68   |   B*14:01    |      M      |