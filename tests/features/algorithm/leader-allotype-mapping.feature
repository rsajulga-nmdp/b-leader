Feature: Determine HLA-B Leader Allotype
    
    Leader allotypes are derived from HLA-B allotypes. This is based on a mapping table, where HLA-B allotypes
    of the same family usually have the same leader type. For unmapped allotypes, an X wildcard is used
    as a placeholder.

    This mapping table is hard coded into the bLeader package.

    Scenario Outline: Translating HLA-B allotypes to leader allotypes.

        Given the HLA-B allotype as <B Allotype>
        When translated to a leader allotype
        Then the leader allotype is <Leader>
        And any potential allotypes are listed as <First Known Allotypes>
        And any exceptions are listed as <Exceptions>
        And any unknowns are listed as <Unknowns>

        Examples: Examples
            | B Allotype                  | Leader |   Exceptions      | First Known Allotypes                       | Unknowns |
            | B*07:02:01:01               |   M    |       None        | B*07:02:01:01                               | None     |
            | B*07:02:01                  |   M    |       None        | B*07:02:01:01, B*07:02:01:02, B*07:02:01:03 | None     |
            | B*07:XX                     |   M    | B*07:65, B*07:271, B*07:371, B*07:390 | B*07:02:01:01, B*07:02:01:02, B*07:02:01:03 | B*07:02:05, B*07:02:07, B*07:02:08 |
            | B*08:BETY                   |   M    |       None        | B*08:02, B*08:20:01, B*08:23                            | B*08:03, B*08:04:01, B*08:04:02 |
            | B*53:XX                     |   T    |       None        | B*53:01:01:01, B*53:01:01:02, B*53:01:01:03 | B*53:01:02, B*53:01:04, B*53:01:07 |
            | B*53:XR                     |   T    |       None        | B*53:01:01:01, B*53:01:01:02, B*53:01:01:03 | B*53:01:02, B*53:01:04, B*53:01:07 |
            | B*07:170                    |   M    |       None        | None                                        | B*07:170 |
            | B*40:64:01G                 |   T    |       None        | B*40:64:01:01, B*40:64:01:02                | None |
            | B*07:02:01:01/B*07:02:01:02 |   M    |       None        | B*07:02:01:01, B*07:02:01:02                | None |
            | B*07:02:01:01/07:02:01:02   |   M    |       None        | B*07:02:01:01, B*07:02:01:02                | None |
            | B*07:02:01:01/02            |   M    |       None        | B*07:02:01:01, B*07:02:01:02                | None |
            | B*27:05/37            |   T    |       None        | B*27:05:02:01, B*27:05:02:02, B*27:05:02:03    | B*27:05:06, B*27:05:08, B*27:05:09 |
            | B*99                        |   X    |       None        | None                                        | B*99     |