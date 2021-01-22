Feature: Define HLA-B Allotype
    An **Allotype** can also be referred to as an allele, which is an alternative version of a gene. 
    In the context of the B-leader microservice, only B-allotypes are considered.
    
    Scenario Outline: Allotype names and fields
        Valid Allotype Names start with B\*, followed by a list of
        numeric field IDs separated by colons.

        Given that the allotype name is <Allotype Name>
        When evaluating the validity of the allotype name
        And retrieving the field values
        Then the allotype name is found to be <Validity>
        And the field list should be <Fields>

        Examples: Valid Examples of B allotypes
            | Allotype Name | Validity |   Fields   |
            | B*07          |  valid   |     07     |
            | B*35          |  valid   |     35     |
            | B*40:05       |  valid   |   40, 05   |
            | B*07:112      |  valid   |   07, 112  |
            | B*07:68:03    |  valid   | 07, 68, 03 |

        Examples: Invalid Examples of B allotypes
            | Allotype Name | Validity | Fields  |
            | HLA-C*01:01   | invalid  | invalid |
            | 😄            | invalid  | invalid |
            | C*01:01       | invalid  | invalid |
            | B*07+B*08     | invalid  | invalid |

    Scenario Outline: Ambiguous Typing

        Given that the allotype name is <Allotype Name>
        When extracting the possible high-resolution alleles
        Then the first three alleles are found to be <Allele List>

        Examples: Examples of ambiguous typing
            | Allotype Name | Allele List                 |
            | B*08:BETY     | B*08:02,B*08:03,B*08:04:01  |
            | B*15:14:01G   | B*15:14,B*15:551            |
            | B*40:64:01G   | B*40:64:01:01,B*40:64:01:02 |
            | B*53:XX       | B*53:01:01:01,B*53:01:01:02,B*53:01:01:03 |
            | B*53:XR       | B*53:01:01:01,B*53:01:01:02,B*53:01:01:03 |