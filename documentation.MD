# QR Format
Use a hash function to encode the data of the user. This also help not to store any information in the sqlite db. 
What should be encoded:
- Names
- Last names
- Some ID
This all can be mixed into a string and hashed, the hash can then be recreated to fetch information of any individual by the organizer if for any reason necesary. Any database leaks won't expose user information as the hashes alone can not be reversed to get the strings.