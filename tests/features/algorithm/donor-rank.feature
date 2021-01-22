Feature: Rank donors for best transplant outcomes
    
    Ranking donors is based on the match quality between the patient's and
    donors' HLA-B genotypes and leader genotypes.

    HLA-B genotype ranking utilizes the match grades as follows:

    AA > PA > LA > MA > PP > LP > MP > LL > ML > MM

    Leader genotype ranking is based on the patient's genotype (MT, TT, or MM):
    - MT patients have two leader-matched donor choices (MMT and TTM, 
    with preference on the former, since M allotypes inhibit NK pathways).
    - TT patients have a leader-matched choice (TTT) which is preferred over
    the other choice (TMT), which is leader-mismatched.
    - MM patients (the least
    common genotype) unfortunately do not have enough transplant data for any
    valid recommendations.

    Donors are ranked initially through HLA-B match grades.
    Then, donors at each match grade are sorted based on leader match status.

    Scenario: Patient leader genotype is TT and is a deviant HLA-B allele
        Deviant HLA-B alleles in this context are alleles that have a
        leader allotype that differs from the common leader allotype in
        the allele family.

        Given the patient genotype is "B*07:65+B*40:02"
        And a list of donor genotypes
            | HLA-B Genotype  | Leader Genotype | Match Grade |
            | B*07+B*40:02    |       MT        |     PA      |
            | B*07:04+B*40:02 |       MT        |     LA      |
            | B*14:01+B*40:02 |       MT        |     MA      |
            | B*07:65+B*40:02 |       TT        |     AA      |
            | B*40:04+B*07    |       TM        |     LP      |
            | B*35:01+B*07    |       TM        |     MP      |
            | B*07:04+B*40:04 |       MT        |     LL      |
            | B*14:01+B*40:04 |       MT        |     ML      |
            | B*14:01+B*35:01 |       MT        |     MM      |
        When the donors are ranked
        Then the ranks are computed to be "1,2,3,4,5,6,7,8,9", respectively

    Scenario: Patient leader genotype is MT