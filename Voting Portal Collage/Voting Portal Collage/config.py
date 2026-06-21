class Config:
    # MAIL CONFIGURATION
    SYSTEM_MAIL="borsevr13@gmail.com"
    SYSTEM_MAIL_PASSWORD="onrx iwzs aaay iyua"
    SYSTEM_MAIL_PORT=587
    SYSTEM_MAIL_SERVER="smtp.gmail.com"
    SYSTEM_MAIL_USE_TLS=True
    SYSTEM_MAIL_USE_SSL=False
    SYSTEM_MAIL_DEFAULT_SENDER = "borsevr13@gmail.com"

    # BLOCKCHAIN CONFIGURATION
    BLOCKCHAIN_URL =  "http://127.0.0.1:7545"
    BLOCKCHAIN_CONTRACT_ADDRESS = "0x38FaF11C24c4A38d188d39046955Acc83f8Fd89f"

    # EMAIL BODY 
    APPROVED_CANDIDATE = """
Dear Candidate,

Congratulations! Your application to stand as a candidate in the upcoming college election has been approved.
You are now officially listed as a candidate for the position you applied for. Please ensure you follow all election guidelines and represent yourself with integrity and respect throughout the campaign period.
If you have any queries or need further information regarding the election process, feel free to reach out to the election committee.
Wishing you all the best for your campaign!


Best regards,
The College Election Committee
                    """ 
    
    REJECTED_CANDIDATE = """
Dear Candidate,

Thank you for applying to be a candidate in the upcoming college election.
After careful review, we regret to inform you that your application has not been approved. This decision may be based on eligibility criteria or other requirements outlined in the election guidelines.
We appreciate your interest in participating and encourage you to stay engaged in the election process through voting and other college activities.
If you have any questions or would like feedback on your application, feel free to contact the election committee.

                    
Best regards,
The College Election Committee
                    """ 

