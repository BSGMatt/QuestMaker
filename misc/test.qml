#INT    int_test 10
#STR stringTest "This is a string."
    #BOOL boolTest TRUE
        #INT moreTesting -1
#INT testingone     10

#STR speakerName "Ronny"
#STR playerName "Johnny"

!TEST_LABEL
    [DISP_TEXT:"$speakerName", "Hello, $playerName! I'm $speakerName"]


#CALL_FUNCTION
    CALL()

    syntax: CALL(label, ret_var)

