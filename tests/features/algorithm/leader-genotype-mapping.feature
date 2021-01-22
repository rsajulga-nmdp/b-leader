Feature: Determine HLA-B Leader Genotype
    
    Leader genotypes are derived from HLA-B genotypes. This is based on a mapping table, where HLA-B allotypes
    of the same family usually have the same leader type. For unmapped allotypes, an X wildcard is used
    as a placeholder.

    This mapping table is hard coded into the bLeader package.

    Scenario Outline: Translating HLA-B genotypes to leader genotypes.

        Given the HLA-B genotype as <B Genotype>
        When translated to a leader genotype
        Then the leader genotype is <Leaders>

        Examples: Examples
            | B Genotype      | Leaders |
            | B*52:04+B*15:01 |   TT    |
            | B*08+B*07       |   MM    |
            | B*35+B*99       |   TX    |
            | B*99+B*99       |   XX    |