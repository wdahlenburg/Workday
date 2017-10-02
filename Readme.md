# Capital One/Workday User Enumeration
This is a simple information leak I discovered on Capital One's career application through Workday.

The issue was with Workday's password reset API endpoint. It produces an information leak that allows any user to determine who is registered on their system. This information could be used by competitors of Capital One to recruit for potential employees. There are various reasons a person would want to know if someone applied, so I will leave that up to you.

The error goes as follows for the password reset:

An account that exists in Capital One's database will recieve the message:
~~~
{"message":"An email with reset instructions has been sent","showResendVerification":false,"type":"SUCCESS"}
~~~

An account that does not exist will recieve the message: 
~~~
{"message":"Failed to initiate password reset, please contact administrator","showResendVerification":false,"type":"ERROR"}
~~~

The information it gives to an attacker is that by sending a password reset link one can tell if a user is potentially applying for a job at a specific company.

I wrote up a simple PoC to display this flaw. All that is needed is a list of email addresses to run through the API.

The input format looks like:

~~~
john@example.com
mary@example.com
robert@example.com
...
~~~

To run: `python cap_one_user_enum.py input_list.txt output_file.txt`

All of the users that are found in the database will be stored in the output file. 

To prevent this from happening, Workday needs to change their API so that it doesn't inform the user whether the account exists. A response that looks like this for all scenarios would work:
~~~
{"message":"A password reset link will be sent out","showResendVerification":false}
~~~

Workday doesn't need to send the emails to applicants not in the database, but they just need to send one generic message to everyone for the password reset.  

#### Disclaimer
A password reset email will be sent to a user if they are in the database. This is noisy. 
This user enumeration is not specific to Capital One. It affects any company using myworkdayjobs.com for an application site. The cool part is the database of user's is unique to each company, so an attacker could find out what other companies you are interested in through Workday.

#### Steps Towards Mitigation

Mon Sep 11 20:29:32 2017 -0400 As soon as I found out about this issue I contacted Workday with the email in vulnerabilityReport.txt

Thu Sep 14 14:35:19 2017 -0400 I contacted them two days later on [Twitter](https://twitter.com/wDahlenb/status/908308301015863301) and did not hear back. I called Workday around 2:30 PM that day and no one was able to take my call. 

Fri Sep 22 11:56:00 2017 -0400 I contacted a recruiter for Capital One and asked them to help me get in contact with Workday. He forwarded my message on to one of their internal contacts.

Mon Oct 02 17:15:00 2017 -0400 PoC and writeup released to general public due to inaction.