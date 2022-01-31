import hashlib
import requests
import sys

#This send the password to the Api at pwned password and request Data, the query caharacter consists of the first 5 characters of the hashcode of the password inorder to have privacy
#this function returns a list of password with the same first 5 character of SHA-1 hash code as that of the password given 
def request_api_data(query_char):
    url= 'https://api.pwnedpasswords.com/range/' + query_char
    res= requests.get(url)
    if res.status_code !=200:
        raise RuntimeError(f'Error Fetching: {res.status_code}, check the api and try again')
    return res

def get_password_leaks_count (hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h ==hash_to_check:
            return count
    return 0
        

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count=pwned_api_check(password)
        if count:
            print(f"{password} was found {count} times.... please change password")
        else:
            print(f'{password} was not found, you are good to go!')
    return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
