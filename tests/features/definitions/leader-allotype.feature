Feature: Define Leader Allotype
    For the B-leader microservice, a **leader allotype** is a classification 
    of the cleaved leader peptide from the first exon of HLA-B. They are classified 
    based on the amino acid at position -21, which can either be a methionine (M)
    or threonine (T) due to rs1050458C/T dimorphism.
    
    Scenario Outline: Mapped Allele Leader Assignment
        Certain B-allele leader types are known. Valid allotypes are either M or T.

        Given that the leader allotype name is <Leader Type>
        When evaluating the validity of the leader allotype name
        Then the leader allotype name is found to be <Validity>

        Examples: Valid Examples
            | Leader Type | Validity |
            |      M      |  valid   |
            |      T      |  valid   |
            |      X      |  valid   |

        # Examples: Invalid Examples
        #     | Leader Type | Validity |
        #     |      MM     | invalid  |
        #     |      Y      | invalid  |
        #     |      N      | invalid  |